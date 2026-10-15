import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.app.services.ai_provider import ai_service
from backend.app.core.logging import logger

class AgentOutput(BaseModel):
    agent_name: str
    status: str  # SUCCESS, FAILED, AWAITING_APPROVAL
    summary: str
    data: Dict[str, Any]
    tokens_used: int = 0
    duration_ms: int = 0
    error: Optional[str] = None

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, system_prompt: str, authorized_tools: List[str] = None):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.authorized_tools = authorized_tools or []

    @abstractmethod
    async def execute(
        self,
        task_id: str,
        objective: str,
        context: Optional[str],
        working_memory: Dict[str, Any],
        **kwargs
    ) -> AgentOutput:
        pass

    async def call_ai(self, user_prompt: str, response_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await ai_service.generate_response(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
            response_schema=response_schema,
            agent_name=self.name
        )
