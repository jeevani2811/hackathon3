from typing import Optional, List
from pydantic import BaseModel

class SystemSettingsSchema(BaseModel):
    project_name: str
    version: str
    ai_provider: str
    gemini_configured: bool
    openai_configured: bool
    anthropic_configured: bool
    max_subtasks: int
    max_retries: int
    task_timeout_seconds: int
    auto_approve_safe_tools: bool
    available_providers: List[str]

class SystemSettingsUpdate(BaseModel):
    ai_provider: Optional[str] = None
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    max_subtasks: Optional[int] = None
    max_retries: Optional[int] = None
    auto_approve_safe_tools: Optional[bool] = None
