from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.schemas.settings import SystemSettingsSchema, SystemSettingsUpdate

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("", response_model=SystemSettingsSchema)
async def get_settings():
    return SystemSettingsSchema(
        project_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        ai_provider=settings.AI_PROVIDER,
        gemini_configured=bool(settings.GEMINI_API_KEY),
        openai_configured=bool(settings.OPENAI_API_KEY),
        anthropic_configured=bool(settings.ANTHROPIC_API_KEY),
        max_subtasks=settings.MAX_SUBTASKS,
        max_retries=settings.MAX_RETRIES,
        task_timeout_seconds=settings.TASK_TIMEOUT_SECONDS,
        auto_approve_safe_tools=settings.AUTO_APPROVE_SAFE_TOOLS,
        available_providers=["mock", "gemini", "openai", "anthropic"]
    )

@router.post("", response_model=SystemSettingsSchema)
async def update_settings(req: SystemSettingsUpdate):
    if req.ai_provider:
        settings.AI_PROVIDER = req.ai_provider
    if req.gemini_api_key is not None:
        settings.GEMINI_API_KEY = req.gemini_api_key
    if req.openai_api_key is not None:
        settings.OPENAI_API_KEY = req.openai_api_key
    if req.anthropic_api_key is not None:
        settings.ANTHROPIC_API_KEY = req.anthropic_api_key
    if req.max_subtasks is not None:
        settings.MAX_SUBTASKS = req.max_subtasks
    if req.max_retries is not None:
        settings.MAX_RETRIES = req.max_retries
    if req.auto_approve_safe_tools is not None:
        settings.AUTO_APPROVE_SAFE_TOOLS = req.auto_approve_safe_tools

    return await get_settings()
