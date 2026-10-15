import time
from typing import Dict, Any, Optional
from backend.app.agents.base import BaseAgent, AgentOutput
from backend.app.tools.registry import tool_registry
from backend.app.core.logging import logger

ANALYSIS_SYSTEM_PROMPT = """
You are the Chief Strategic Analyst Agent for OmniAgent.
Your objective is to evaluate qualitative and quantitative evidence collected by research and execution agents.
Identify vendor moats, construct a rigorous SWOT matrix, evaluate cost-latency tradeoffs, and formulate actionable enterprise recommendations.
"""

class AnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Analysis Agent",
            role="Cross-Evidence Synthesis & Strategic SWOT",
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            authorized_tools=["matrix_transformer"]
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
            # 1. Run matrix transformation
            matrix_res = await tool_registry.execute_tool(
                name="matrix_transformer",
                parameters={
                    "competitors": ["Pinecone", "Weaviate", "Qdrant"],
                    "evaluation_dimensions": [
                        "Query Latency (p99)",
                        "Scalability & Serverless",
                        "Cost Efficiency / TCO",
                        "Multi-Modal Support",
                        "Enterprise Compliance",
                        "Self-Hosting Flexibility"
                    ]
                },
                task_id=task_id,
                is_approved=True
            )

            # 2. Synthesize strategic analysis with AI
            prompt = (
                f"Objective: {objective}\n"
                f"Evidence: {working_memory.get('evidence', [])}\n"
                f"Financial Model: {working_memory.get('financial_data', {})}\n"
                f"Matrix: {matrix_res.get('result', {})}"
            )
            ai_res = await self.call_ai(prompt, response_schema={"type": "object"})
            
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="SUCCESS",
                summary="Completed multi-dimensional SWOT synthesis and competitive moat evaluation.",
                data={
                    "analysis": ai_res.get("content", {}),
                    "matrix": matrix_res.get("result", {}),
                    "tool_invocations": [matrix_res]
                },
                tokens_used=ai_res.get("tokens_used", 1400),
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Analysis Agent failed: {str(e)}", exc_info=True)
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="FAILED",
                summary=f"Analysis failed: {str(e)}",
                data={},
                duration_ms=duration_ms,
                error=str(e)
            )
