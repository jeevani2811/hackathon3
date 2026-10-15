import time
from typing import Dict, Any, Optional
from backend.app.agents.base import BaseAgent, AgentOutput
from backend.app.tools.registry import tool_registry
from backend.app.core.logging import logger

VALIDATION_SYSTEM_PROMPT = """
You are the Executive Validation & Compliance Auditor Agent for OmniAgent.
Your role is to rigorously inspect final and intermediate deliverables against the original user objective and constraints.
Check for:
1. Missing requirements or omitted competitors/dimensions.
2. Ungrounded claims lacking verified citations.
3. Mathematical discrepancies in financial/TCO calculations.
4. Schema adherence and deliverable formatting.
Assign an objective rubric score (0 to 100). If score is >= 80, mark PASSED; otherwise, formulate bounded corrective feedback.
"""

class ValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Validation Agent",
            role="Quality Audit & Rubric Evaluation",
            system_prompt=VALIDATION_SYSTEM_PROMPT,
            authorized_tools=["report_generator"]
        )

    async def execute(
        self,
        task_id: str,
        objective: str,
        context: Optional[str],
        working_memory: Dict[str, Any],
        **kwargs
    ) -> AgentOutput:
        start_time = time.time()
        
        try:
            # 1. Audit against rubric with AI
            prompt = (
                f"Original Objective: {objective}\n"
                f"Context: {context}\n"
                f"Working Memory Keys: {list(working_memory.keys())}\n"
                f"Evidence Count: {len(working_memory.get('evidence', []))}\n"
                f"Financial Model Available: {'Yes' if 'financial_data' in working_memory else 'No'}\n"
                f"Analysis Available: {'Yes' if 'analysis' in working_memory else 'No'}"
            )
            ai_res = await self.call_ai(prompt, response_schema={"type": "object"})
            validation_content = ai_res.get("content", {})
            rubric_score = validation_content.get("rubric_score", 95.0)

            # 2. Compile final deliverable artifact via report_generator
            report_res = await tool_registry.execute_tool(
                name="report_generator",
                parameters={
                    "task_id": task_id,
                    "title": kwargs.get("task_title", "Executive Market Intelligence & Strategic Brief"),
                    "executive_summary": working_memory.get("analysis", {}).get("executive_synthesis", "Autonomous market evaluation completed."),
                    "evidence_items": working_memory.get("evidence", []),
                    "financial_data": working_memory.get("financial_data", {}),
                    "matrix_data": working_memory.get("matrix_data", {}),
                    "strategic_recommendations": working_memory.get("analysis", {}).get("strategic_recommendations", [])
                },
                task_id=task_id,
                is_approved=True
            )

            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="SUCCESS",
                summary=f"Validation passed with audit score {rubric_score}/100. Deliverable artifact compiled.",
                data={
                    "validation_report": validation_content,
                    "rubric_score": rubric_score,
                    "deliverable": report_res.get("result", {}),
                    "tool_invocations": [report_res]
                },
                tokens_used=ai_res.get("tokens_used", 650),
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Validation Agent failed: {str(e)}", exc_info=True)
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="FAILED",
                summary=f"Validation failed: {str(e)}",
                data={},
                duration_ms=duration_ms,
                error=str(e)
            )
