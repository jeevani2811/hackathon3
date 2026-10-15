from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models import Plan
from backend.app.schemas.task import PlanSchema

router = APIRouter(prefix="/plans", tags=["Plans"])

@router.get("/{task_id}", response_model=PlanSchema)
async def get_plan_by_task(task_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(Plan).where(Plan.task_id == task_id).options(
            selectinload(Plan.subtasks)
        )
    )
    plan = res.scalars().first()
    if not plan:
        raise HTTPException(status_code=404, detail="Execution plan not found for this task.")
    return plan
