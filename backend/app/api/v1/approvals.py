from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models import ApprovalRequest
from backend.app.schemas.approval import ApprovalResponse, ApprovalDecision
from backend.app.orchestration.engine import orchestrator

router = APIRouter(prefix="/approvals", tags=["Human Approvals"])

@router.get("", response_model=List[ApprovalResponse])
async def list_approvals(
    task_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(ApprovalRequest).order_by(ApprovalRequest.requested_at.desc())
    if task_id:
        query = query.where(ApprovalRequest.task_id == task_id)
    if status:
        query = query.where(ApprovalRequest.status == status)
    
    res = await db.execute(query)
    return res.scalars().all()

@router.get("/{approval_id}", response_model=ApprovalResponse)
async def get_approval(approval_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Approval request not found.")
    return app

@router.post("/{approval_id}/decide", response_model=ApprovalResponse)
async def decide_approval(
    approval_id: str,
    body: ApprovalDecision,
    db: AsyncSession = Depends(get_db)
):
    try:
        await orchestrator.handle_approval_decision(
            approval_id=approval_id,
            decision=body.decision,
            notes=body.decision_notes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    res = await db.execute(select(ApprovalRequest).where(ApprovalRequest.id == approval_id))
    return res.scalars().first()
