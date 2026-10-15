import time
from typing import Dict, Any, Optional
from backend.app.agents.base import BaseAgent, AgentOutput
from backend.app.tools.registry import tool_registry
from backend.app.core.logging import logger

EXECUTION_SYSTEM_PROMPT = """
You are the Quantitative & Computational Execution Agent for OmniAgent.
You execute strictly bounded tools including deterministic financial calculators, matrix normalizers, deliverable compilers, and external catalog updates.
Always ensure parameters conform to input constraints before invoking tools.
"""

class ExecutionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Execution Agent",
            role="Deterministic Tool Execution & Computation",
            system_prompt=EXECUTION_SYSTEM_PROMPT,
            authorized_tools=["financial_calculator", "matrix_transformer", "report_generator", "database_update", "notification_webhook"]
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
        subtask_tools = kwargs.get("tools", ["financial_calculator"])
        is_approved = kwargs.get("is_approved", True)
        
        results = {}
        tool_invocations = []
        
        try:
            for tool_name in subtask_tools:
                params = {}
                if tool_name == "financial_calculator":
                    params = {
                        "monthly_queries_million": 12.0,
                        "storage_gb": 350.0,
                        "developer_count": 6,
                        "legacy_monthly_cost": 9200.0,
                        "hourly_engineer_rate": 125.0
                    }
                elif tool_name == "matrix_transformer":
                    params = {
                        "competitors": ["Pinecone", "Weaviate", "Qdrant"],
                        "evaluation_dimensions": [
                            "Query Latency (p99)",
                            "Scalability & Serverless",
                            "Cost Efficiency / TCO",
                            "Multi-Modal Support",
                            "Enterprise Compliance",
                            "Self-Hosting Flexibility"
                        ]
                    }
                elif tool_name == "report_generator":
                    params = {
                        "task_id": task_id,
                        "title": kwargs.get("task_title", "Enterprise Vector Database Strategy Brief"),
                        "executive_summary": working_memory.get("analysis", {}).get("executive_synthesis", "Strategic evaluation of enterprise vector databases."),
                        "evidence_items": working_memory.get("evidence", []),
                        "financial_data": working_memory.get("financial_data", {}),
                        "matrix_data": working_memory.get("matrix_data", {}),
                        "strategic_recommendations": working_memory.get("analysis", {}).get("strategic_recommendations", [])
                    }
                elif tool_name == "database_update":
                    params = {
                        "catalog_table": "enterprise_vendor_battlecards",
                        "record_key": "vector_dbs_2026",
                        "record_payload": {"status": "validated", "top_pick": "Qdrant_Cloud"},
                        "commit_reason": "Approved executive strategy deliverable write"
                    }
                elif tool_name == "notification_webhook":
                    params = {
                        "channel_or_endpoint": "#strategy-briefings",
                        "subject": "Executive Strategy Brief Complete",
                        "summary_markdown": "OmniAgent completed vector DB market analysis and financial TCO model.",
                        "priority": "high"
                    }

                res = await tool_registry.execute_tool(
                    name=tool_name,
                    parameters=params,
                    task_id=task_id,
                    is_approved=is_approved
                )
                tool_invocations.append(res)
                if not res["success"]:
                    raise RuntimeError(f"Tool {tool_name} error: {res['error']}")
                results[tool_name] = res["result"]

            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="SUCCESS",
                summary=f"Successfully executed tools: {', '.join(subtask_tools)}.",
                data={
                    "tool_results": results,
                    "tool_invocations": tool_invocations
                },
                tokens_used=400,
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Execution Agent failed: {str(e)}", exc_info=True)
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="FAILED",
                summary=f"Tool execution failed: {str(e)}",
                data={"tool_invocations": tool_invocations},
                duration_ms=duration_ms,
                error=str(e)
            )
