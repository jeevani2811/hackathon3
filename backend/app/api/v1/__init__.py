from fastapi import APIRouter
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.tasks import router as tasks_router
from backend.app.api.v1.plans import router as plans_router
from backend.app.api.v1.agents import router as agents_router
from backend.app.api.v1.approvals import router as approvals_router
from backend.app.api.v1.tools import router as tools_router
from backend.app.api.v1.events import router as events_router
from backend.app.api.v1.artifacts import router as artifacts_router
from backend.app.api.v1.settings import router as settings_router
from backend.app.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(tasks_router)
api_router.include_router(plans_router)
api_router.include_router(agents_router)
api_router.include_router(approvals_router)
api_router.include_router(tools_router)
api_router.include_router(events_router)
api_router.include_router(artifacts_router)
api_router.include_router(settings_router)
