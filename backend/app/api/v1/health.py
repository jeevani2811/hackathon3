import time
import psutil
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db
from backend.app.core.config import settings

router = APIRouter(prefix="/health", tags=["Operational Diagnostics"])

START_TIME = time.time()

@router.get("")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_ok = False
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    uptime_sec = int(time.time() - START_TIME)
    mem = psutil.virtual_memory()

    return {
        "status": "HEALTHY" if db_ok else "DEGRADED",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database_connected": db_ok,
        "uptime_seconds": uptime_sec,
        "ai_provider": settings.AI_PROVIDER,
        "system_metrics": {
            "ram_usage_pct": mem.percent,
            "cpu_count": psutil.cpu_count()
        }
    }
