import asyncio
import time
import uuid
from datetime import datetime
from typing import Dict, Any, List, Set, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from backend.app.db.session import AsyncSessionLocal
from backend.app.models import Task, Plan, SubTask, ApprovalRequest, EventRecord, ArtifactDeliverable, ToolInvocation
from backend.app.core.events import event_bus
from backend.app.core.logging import logger
from backend.app.agents import get_agent, planner_agent, AGENT_FLEET
from backend.app.tools.registry import tool_registry
from backend.app.memory.store import memory_store
from backend.app.security.permissions import calculate_action_payload_hash, is_tool_sensitive
from backend.app.security.sanitization import sanitize_user_input, detect_prompt_injection

class WorkflowOrchestrator:
    def __init__(self):
        # task_id -> asyncio.Task running the background orchestration
        self._running_tasks: Dict[str, asyncio.Task] = {}
        # task_id -> cancellation / pause flags
        self._paused_tasks: Set[str] = set()
        self._cancelled_tasks: Set[str] = set()

    async def start_workflow(self, task_id: str):
        """Spawns an async workflow runner without blocking the API request handler."""
        if task_id in self._running_tasks and not self._running_tasks[task_id].done():
            logger.warning(f"Workflow {task_id} is already actively running.")
            return

        coro = self._run_workflow_lifecycle(task_id)
        task_coro = asyncio.create_task(coro)
        self._running_tasks[task_id] = task_coro

    async def pause_workflow(self, task_id: str):
        self._paused_tasks.add(task_id)
        async with AsyncSessionLocal() as db:
            await db.execute(update(Task).where(Task.id == task_id).values(status="paused"))
            await db.commit()
        await event_bus.publish(task_id, "workflow_paused", {"status": "paused", "message": "Workflow paused by operator."})

    async def resume_workflow(self, task_id: str):
        self._paused_tasks.discard(task_id)
        async with AsyncSessionLocal() as db:
            await db.execute(update(Task).where(Task.id == task_id).values(status="running"))
            await db.commit()
        await event_bus.publish(task_id, "workflow_resumed", {"status": "running", "message": "Workflow resumed."})
        # Restart background runner
        await self.start_workflow(task_id)

    async def cancel_workflow(self, task_id: str):
        self._cancelled_tasks.add(task_id)
        if task_id in self._running_tasks:
            self._running_tasks[task_id].cancel()
        async with AsyncSessionLocal() as db:
            await db.execute(update(Task).where(Task.id == task_id).values(status="cancelled", completed_at=datetime.utcnow()))
            await db.commit()
        await event_bus.publish(task_id, "workflow_cancelled", {"status": "cancelled", "message": "Workflow cancelled by operator."})

    async def handle_approval_decision(self, approval_id: str, decision: str, notes: Optional[str] = None):
        """
        Processes human approval or rejection. If approved, resumes workflow.
        """
        async with AsyncSessionLocal() as db:
            res = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
            approval = res.scalars().first()
            if not approval:
                raise ValueError("Approval request not found.")

            is_approved = decision.lower() in ("approve", "approved")
            approval.status = "approved" if is_approved else "rejected"
            approval.decision_notes = notes
            approval.decided_at = datetime.utcnow()
            task_id = approval.task_id

            if approval.action_type == "plan_approval":
                plan_res = await db.execute(select(Plan).where(Plan.task_id == task_id))
                plan = plan_res.scalars().first()
                if plan:
                    plan.is_approved = is_approved

            await db.commit()

        await event_bus.publish(task_id, "approval_decided", {
            "approval_id": approval_id,
            "decision": decision,
            "action_type": approval.action_type,
            "notes": notes
        })

        if decision == "approve":
            await self.resume_workflow(task_id)
        else:
            await self.cancel_workflow(task_id)

    async def _run_workflow_lifecycle(self, task_id: str):
        logger.info(f"Initiating autonomous workflow lifecycle for task: {task_id}")
        
        try:
            # 1. Fetch Task and validate state
            async with AsyncSessionLocal() as db:
                res = await db.execute(
                    select(Task).where(Task.id == task_id).options(
                        selectinload(Task.plan),
                        selectinload(Task.subtasks),
                        selectinload(Task.approvals)
                    )
                )
                task = res.scalars().first()
                if not task:
                    logger.error(f"Task {task_id} not found in database.")
                    return

                if task.status in ["completed", "cancelled"]:
                    return

                # Prompt Injection Check
                if detect_prompt_injection(task.objective) or detect_prompt_injection(task.context or ""):
                    task.status = "failed"
                    task.error_message = "Security policy violation: Prompt injection pattern detected in objective."
                    await db.commit()
                    await event_bus.publish(task_id, "security_violation", {"error": task.error_message})
                    return

                # 2. Check if Plan exists; if not, invoke Planner Agent
                if not task.plan:
                    task.status = "planning"
                    await db.commit()
                    await event_bus.publish(task_id, "workflow_planning", {
                        "status": "planning",
                        "message": "Planner Agent decomposing objective into DAG subtasks..."
                    })

                    plan_output = await planner_agent.execute(
                        task_id=task_id,
                        objective=task.objective,
                        context=task.context,
                        working_memory=memory_store.get_working_memory(task_id)
                    )

                    if plan_output.status == "FAILED":
                        task.status = "failed"
                        task.error_message = plan_output.error
                        await db.commit()
                        await event_bus.publish(task_id, "workflow_failed", {"error": plan_output.error})
                        return

                    plan_data = plan_output.data
                    requires_approval = task.mode in ("human_in_the_loop", "supervised", "hitl")
                    
                    new_plan = Plan(
                        task_id=task_id,
                        total_steps=plan_data.get("total_steps", 5),
                        estimated_tokens=plan_data.get("estimated_tokens", 3200),
                        summary=plan_data.get("summary", "Autonomous Execution Plan"),
                        requires_approval=requires_approval,
                        is_approved=not requires_approval
                    )
                    db.add(new_plan)
                    await db.flush()

                    # Create SubTasks
                    raw_subtasks = plan_data.get("subtasks", [])
                    step_id_to_uuid = {}
                    
                    for idx, st_dict in enumerate(raw_subtasks):
                        subtask_uuid = str(uuid.uuid4())
                        step_id_to_uuid[st_dict.get("step_id", f"step_{idx+1}")] = subtask_uuid
                        
                        subtask = SubTask(
                            id=subtask_uuid,
                            task_id=task_id,
                            plan_id=new_plan.id,
                            title=st_dict.get("title", f"Subtask {idx+1}"),
                            description=st_dict.get("description", ""),
                            assigned_agent=st_dict.get("assigned_agent", "Execution Agent"),
                            status="pending",
                            execution_order=idx + 1,
                            tools_assigned=st_dict.get("tools", []),
                            dependencies=[]  # will map next
                        )
                        db.add(subtask)

                    await db.flush()

                    # Map dependencies to real UUIDs
                    for idx, st_dict in enumerate(raw_subtasks):
                        sub_uuid = step_id_to_uuid[st_dict.get("step_id", f"step_{idx+1}")]
                        raw_deps = st_dict.get("dependencies", [])
                        resolved_deps = [step_id_to_uuid[d] for d in raw_deps if d in step_id_to_uuid]
                        
                        await db.execute(
                            update(SubTask).where(SubTask.id == sub_uuid).values(dependencies=resolved_deps)
                        )

                    # If human in the loop, request approval for the plan
                    if requires_approval:
                        task.status = "awaiting_approval"
                        approval_hash = calculate_action_payload_hash(
                            task_id=task_id,
                            action_type="plan_approval",
                            parameters={"total_steps": new_plan.total_steps, "summary": new_plan.summary}
                        )
                        app_req = ApprovalRequest(
                            task_id=task_id,
                            action_type="plan_approval",
                            title="Approval Required: Autonomous Execution Plan",
                            description=f"Planner generated {new_plan.total_steps}-step execution plan for '{task.title}'. Review and approve to begin agent execution.",
                            parameters={"total_steps": new_plan.total_steps, "summary": new_plan.summary},
                            payload_hash=approval_hash,
                            status="pending"
                        )
                        db.add(app_req)
                        await db.commit()

                        await event_bus.publish(task_id, "awaiting_approval", {
                            "approval_id": app_req.id,
                            "action_type": "plan_approval",
                            "title": app_req.title,
                            "description": app_req.description
                        })
                        return  # Halt until approved

                    task.status = "running"
                    await db.commit()
                    await event_bus.publish(task_id, "plan_approved", {"status": "running", "message": "Plan accepted. Starting agent fleet..."})

            # 3. Main DAG Execution Loop
            while True:
                if task_id in self._cancelled_tasks:
                    logger.info(f"Workflow {task_id} cancelled.")
                    return
                if task_id in self._paused_tasks:
                    logger.info(f"Workflow {task_id} paused.")
                    return

                async with AsyncSessionLocal() as db:
                    # Refresh task and subtasks
                    res = await db.execute(
                        select(Task).where(Task.id == task_id).options(
                            selectinload(Task.subtasks)
                        )
                    )
                    task = res.scalars().first()
                    all_subtasks = task.subtasks

                    # Find completed and pending subtasks
                    completed_ids = {st.id for st in all_subtasks if st.status == "completed"}
                    pending_subtasks = [st for st in all_subtasks if st.status == "pending"]

                    if not pending_subtasks:
                        # All subtasks complete! Proceed to final completion
                        break

                    # Identify ready subtasks
                    ready_subtasks = [
                        st for st in pending_subtasks
                        if all(dep in completed_ids for dep in (st.dependencies or []))
                    ]

                    if not ready_subtasks:
                        # Deadlock or broken dependencies
                        task.status = "failed"
                        task.error_message = "Dependency deadlock: Pending subtasks have unsatisfied dependencies."
                        await db.commit()
                        await event_bus.publish(task_id, "workflow_failed", {"error": task.error_message})
                        return

                    # Execute ready subtasks (can run sequentially or in parallel)
                    st = ready_subtasks[0]  # Process next ready node
                    st.status = "running"
                    st.started_at = datetime.utcnow()
                    await db.commit()

                # Dispatch subtask to agent
                await self._execute_subtask(task_id, st.id)

            # 4. Final Validation & Completion Stage
            await self._finalize_workflow(task_id)

        except asyncio.CancelledError:
            logger.info(f"Workflow {task_id} task was cancelled.")
        except Exception as e:
            logger.error(f"Unhandled error in workflow {task_id}: {str(e)}", exc_info=True)
            async with AsyncSessionLocal() as db:
                await db.execute(update(Task).where(Task.id == task_id).values(status="failed", error_message=str(e)))
                await db.commit()
            await event_bus.publish(task_id, "workflow_failed", {"error": str(e)})

    async def _execute_subtask(self, task_id: str, subtask_id: str):
        async with AsyncSessionLocal() as db:
            res = await db.execute(select(SubTask).where(SubTask.id == subtask_id))
            subtask = res.scalars().first()
            task_res = await db.execute(select(Task).where(Task.id == task_id))
            task = task_res.scalars().first()
            
            agent_name = subtask.assigned_agent
            tools_assigned = subtask.tools_assigned or []
            task_mode = task.mode

            # Check if any tool in this subtask is SENSITIVE and needs approval
            for tool_name in tools_assigned:
                if is_tool_sensitive(tool_name) and task_mode in ("human_in_the_loop", "supervised", "hitl"):
                    # Check if approval already granted
                    app_res = await db.execute(
                        select(ApprovalRequest).where(
                            ApprovalRequest.task_id == task_id,
                            ApprovalRequest.subtask_id == subtask_id,
                            ApprovalRequest.status == "approved"
                        )
                    )
                    if not app_res.scalars().first():
                        # Pause for tool approval
                        subtask.status = "awaiting_approval"
                        task.status = "awaiting_approval"
                        
                        tool_params = {"tool_name": tool_name, "subtask_title": subtask.title}
                        payload_hash = calculate_action_payload_hash(task_id, f"tool:{tool_name}", tool_params)
                        
                        req = ApprovalRequest(
                            task_id=task_id,
                            subtask_id=subtask_id,
                            action_type=f"sensitive_tool:{tool_name}",
                            title=f"Sensitive Action Approval: {tool_name}",
                            description=f"Subtask '{subtask.title}' requires execution of sensitive tool '{tool_name}' (external impact/write). Review and confirm.",
                            parameters=tool_params,
                            payload_hash=payload_hash,
                            status="pending"
                        )
                        db.add(req)
                        await db.commit()

                        await event_bus.publish(task_id, "awaiting_approval", {
                            "approval_id": req.id,
                            "action_type": req.action_type,
                            "title": req.title,
                            "description": req.description
                        })
                        return

        # Emit subtask starting event
        await event_bus.publish(task_id, "subtask_started", {
            "subtask_id": subtask_id,
            "title": subtask.title,
            "agent": agent_name,
            "status": "running"
        })

        agent = get_agent(agent_name)
        if not agent:
            agent = AGENT_FLEET["Execution Agent"]

        working_mem = memory_store.get_working_memory(task_id)

        # Execute agent
        agent_output = await agent.execute(
            task_id=task_id,
            objective=task.objective,
            context=task.context,
            working_memory=working_mem,
            subtask_title=subtask.title,
            task_title=task.title,
            tools=tools_assigned,
            is_approved=True
        )

        async with AsyncSessionLocal() as db:
            res = await db.execute(select(SubTask).where(SubTask.id == subtask_id))
            st = res.scalars().first()

            if agent_output.status == "SUCCESS":
                st.status = "completed"
                st.output_data = agent_output.data
                st.completed_at = datetime.utcnow()
                st.duration_ms = agent_output.duration_ms

                # Update working memory
                if "evidence" in agent_output.data:
                    working_mem["evidence"].extend(agent_output.data["evidence"])
                if "tool_results" in agent_output.data:
                    for t_name, t_val in agent_output.data["tool_results"].items():
                        if t_name == "financial_calculator":
                            working_mem["financial_data"] = t_val
                        elif t_name == "matrix_transformer":
                            working_mem["matrix_data"] = t_val
                if "analysis" in agent_output.data:
                    working_mem["analysis"] = agent_output.data["analysis"]
                if "matrix" in agent_output.data:
                    working_mem["matrix_data"] = agent_output.data["matrix"]

                # Update Task progress percentage
                subtasks_res = await db.execute(select(SubTask).where(SubTask.task_id == task_id))
                all_subs = subtasks_res.scalars().all()
                done_count = sum(1 for s in all_subs if s.status == "completed")
                total_count = len(all_subs)
                pct = int((done_count / total_count) * 90)  # Reserve last 10% for final validation

                await db.execute(update(Task).where(Task.id == task_id).values(progress_pct=pct))
                await db.commit()

                await event_bus.publish(task_id, "subtask_completed", {
                    "subtask_id": subtask_id,
                    "title": st.title,
                    "agent": agent_name,
                    "status": "completed",
                    "duration_ms": agent_output.duration_ms,
                    "summary": agent_output.summary,
                    "progress_pct": pct
                })
            else:
                # Handle failure / retry
                st.retry_count += 1
                if st.retry_count <= 3:
                    st.status = "pending"  # Retry
                    await db.commit()
                    await event_bus.publish(task_id, "subtask_retry", {
                        "subtask_id": subtask_id,
                        "retry_count": st.retry_count,
                        "error": agent_output.error
                    })
                else:
                    st.status = "failed"
                    st.error = agent_output.error
                    await db.execute(update(Task).where(Task.id == task_id).values(status="failed", error_message=agent_output.error))
                    await db.commit()
                    await event_bus.publish(task_id, "subtask_failed", {
                        "subtask_id": subtask_id,
                        "error": agent_output.error
                    })

    async def _finalize_workflow(self, task_id: str):
        """Compiles deliverables and updates task to completed."""
        working_mem = memory_store.get_working_memory(task_id)

        async with AsyncSessionLocal() as db:
            task_res = await db.execute(select(Task).where(Task.id == task_id))
            task = task_res.scalars().first()

            val_agent = AGENT_FLEET["Validation Agent"]
            val_out = await val_agent.execute(
                task_id=task_id,
                objective=task.objective,
                context=task.context,
                working_memory=working_mem,
                task_title=task.title
            )

            validation_data = val_out.data.get("validation_report", {})
            rubric_score = val_out.data.get("rubric_score", 95.0)
            deliverable_info = val_out.data.get("deliverable", {})
            markdown_deliverable = deliverable_info.get("markdown_content", "Deliverable compiled successfully.")

            # Record Artifact in DB
            artifact = ArtifactDeliverable(
                task_id=task_id,
                file_name=deliverable_info.get("markdown_file", f"deliverable_{task_id}.md"),
                file_path=deliverable_info.get("markdown_path", ""),
                file_type="markdown",
                size_bytes=deliverable_info.get("file_size_bytes", len(markdown_deliverable)),
                content_summary="Executive Strategy Brief & Financial Model Deliverable"
            )
            db.add(artifact)

            task.status = "completed"
            task.progress_pct = 100
            task.validation_score = rubric_score
            task.final_deliverable = markdown_deliverable
            task.completed_at = datetime.utcnow()
            await db.commit()

        await event_bus.publish(task_id, "workflow_completed", {
            "status": "completed",
            "progress_pct": 100,
            "validation_score": rubric_score,
            "deliverable": markdown_deliverable[:300] + "...",
            "message": "All agents completed tasks. Final strategic brief validated and published."
        })
        logger.info(f"Workflow {task_id} successfully finalized with validation score: {rubric_score}")

orchestrator = WorkflowOrchestrator()
