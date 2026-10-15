from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models import Task, Plan, SubTask, ApprovalRequest, ArtifactDeliverable
from backend.app.schemas.task import TaskCreate, TaskDetail, TaskListResponse
from backend.app.orchestration.engine import orchestrator
from backend.app.security.auth import get_current_user_optional
from backend.app.security.sanitization import sanitize_user_input

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("", response_model=TaskDetail)
async def create_task(
    req: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_optional)
):
    cleaned_title = sanitize_user_input(req.title)
    cleaned_obj = sanitize_user_input(req.objective)
    cleaned_ctx = sanitize_user_input(req.context or "")

    new_task = Task(
        title=cleaned_title,
        objective=cleaned_obj,
        context=cleaned_ctx,
        priority=req.priority,
        mode=req.mode,
        status="pending",
        user_id=user.get("id") if user else None
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    # Launch autonomous orchestration in background
    background_tasks.add_task(orchestrator.start_workflow, new_task.id)

    # Return refreshed detail
    res = await db.execute(
        select(Task).where(Task.id == new_task.id).options(
            selectinload(Task.plan).selectinload(Plan.subtasks),
            selectinload(Task.subtasks),
            selectinload(Task.approvals)
        )
    )
    return res.scalars().first()

@router.get("", response_model=TaskListResponse)
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by task status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Keyword search in title or objective"),
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Task).options(
        selectinload(Task.plan).selectinload(Plan.subtasks),
        selectinload(Task.subtasks),
        selectinload(Task.approvals)
    ).order_by(desc(Task.created_at))

    if status:
        query = query.where(Task.status == status)
    if priority:
        query = query.where(Task.priority == priority)
    if search:
        query = query.where(Task.title.ilike(f"%{search}%") | Task.objective.ilike(f"%{search}%"))

    result = await db.execute(query.offset(skip).limit(limit))
    tasks = result.scalars().all()

    # Metrics
    all_res = await db.execute(select(Task.status))
    all_statuses = [s for (s,) in all_res.all()]
    total = len(all_statuses)
    active_count = sum(1 for s in all_statuses if s in ["pending", "planning", "running", "awaiting_approval"])
    completed_count = sum(1 for s in all_statuses if s == "completed")
    failed_count = sum(1 for s in all_statuses if s in ["failed", "cancelled"])

    return {
        "tasks": tasks,
        "total": total,
        "active_count": active_count,
        "completed_count": completed_count,
        "failed_count": failed_count
    }

@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(task_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(Task).where(Task.id == task_id).options(
            selectinload(Task.plan).selectinload(Plan.subtasks),
            selectinload(Task.subtasks),
            selectinload(Task.approvals),
            selectinload(Task.artifacts)
        )
    )
    task = res.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/pause")
async def pause_task(task_id: str):
    await orchestrator.pause_workflow(task_id)
    return {"status": "paused", "task_id": task_id}

@router.post("/{task_id}/resume")
async def resume_task(task_id: str):
    await orchestrator.resume_workflow(task_id)
    return {"status": "resumed", "task_id": task_id}

@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    await orchestrator.cancel_workflow(task_id)
    return {"status": "cancelled", "task_id": task_id}

@router.post("/{task_id}/retry")
async def retry_task(task_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Task).where(Task.id == task_id))
    task = res.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "pending"
    task.error_message = None
    task.progress_pct = 0
    await db.commit()

    background_tasks.add_task(orchestrator.start_workflow, task_id)
    return {"status": "retrying", "task_id": task_id}
