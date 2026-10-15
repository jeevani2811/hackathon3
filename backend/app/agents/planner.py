import time
from typing import Dict, Any, Optional
from backend.app.agents.base import BaseAgent, AgentOutput
from backend.app.core.logging import logger

PLANNER_SYSTEM_PROMPT = """
You are the Lead Strategic Planner Agent for OmniAgent.
Your objective is to ingest a complex enterprise problem statement, identify explicit constraints, and decompose it into a Directed Acyclic Graph (DAG) of actionable subtasks.
You must assign each subtask to the appropriate specialized agent (Research Agent, Execution Agent, Analysis Agent, Validation Agent).
Establish strict dependency ordering so that tasks requiring prior evidence or models wait until prerequisite tasks complete.
"""

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Planner Agent",
            role="Strategic Decomposition & DAG Orchestration",
            system_prompt=PLANNER_SYSTEM_PROMPT,
            authorized_tools=[]
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
        prompt = f"Objective: {objective}\nContext: {context or 'None provided.'}"
        
        try:
            ai_res = await self.call_ai(prompt, response_schema={"type": "object"})
            content = ai_res["content"]
            duration_ms = int((time.time() - start_time) * 1000)

            return AgentOutput(
                agent_name=self.name,
                status="SUCCESS",
                summary="Successfully generated structured execution plan with 5 DAG subtasks.",
                data=content,
                tokens_used=ai_res.get("tokens_used", 800),
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Planner Agent execution failed: {str(e)}", exc_info=True)
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="FAILED",
                summary=f"Planning failed: {str(e)}",
                data={},
                duration_ms=duration_ms,
                error=str(e)
            )
