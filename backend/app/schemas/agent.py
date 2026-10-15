from typing import List, Optional
from pydantic import BaseModel

class AgentInfo(BaseModel):
    id: str
    name: str
    role: str
    description: str
    system_prompt: str
    authorized_tools: List[str]
    status: str
    total_tasks_executed: int
    successful_tasks: int
    avg_duration_ms: float
