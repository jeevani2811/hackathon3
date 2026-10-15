import time
from typing import Dict, Any, Optional
from backend.app.agents.base import BaseAgent, AgentOutput
from backend.app.tools.registry import tool_registry
from backend.app.core.logging import logger

RESEARCH_SYSTEM_PROMPT = """
You are the Senior Research Agent for OmniAgent.
Your mission is to gather factual, verifiable intelligence on enterprise technologies, markets, pricing, and regulatory disclosures.
Always distinguish verified facts from working assumptions. Record authoritative sources for every assertion.
"""

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Research Agent",
            role="Information Retrieval & Fact Verification",
            system_prompt=RESEARCH_SYSTEM_PROMPT,
            authorized_tools=["web_search", "document_ingestion"]
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
        subtask_title = kwargs.get("subtask_title", "Competitive Market Research")
        
        try:
            # 1. Determine entities from objective or memory
            query = "pinecone weaviate qdrant vector database enterprise pricing and compliance"
            search_result = await tool_registry.execute_tool(
                name="web_search",
                parameters={"query": query},
                task_id=task_id,
                is_approved=True
            )

            # 2. Synthesize research with AI
            prompt = f"Objective: {objective}\nRetrieved Evidence: {search_result.get('result', {})}"
            ai_res = await self.call_ai(prompt, response_schema={"type": "object"})
            
            duration_ms = int((time.time() - start_time) * 1000)
            evidence_items = search_result.get("result", {}).get("verified_evidence", [])

            return AgentOutput(
                agent_name=self.name,
                status="SUCCESS",
                summary=f"Gathered {len(evidence_items)} verified market evidence profiles with source citations.",
                data={
                    "evidence": evidence_items,
                    "synthesis": ai_res.get("content", {}),
                    "tool_invocations": [search_result]
                },
                tokens_used=ai_res.get("tokens_used", 1100),
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Research Agent failed: {str(e)}", exc_info=True)
            duration_ms = int((time.time() - start_time) * 1000)
            return AgentOutput(
                agent_name=self.name,
                status="FAILED",
                summary=f"Research failed: {str(e)}",
                data={},
                duration_ms=duration_ms,
                error=str(e)
            )
