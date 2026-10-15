import os
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, ConfigDict

from backend.app.db.session import get_db
from backend.app.models import ArtifactDeliverable

router = APIRouter(prefix="/artifacts", tags=["Artifacts & Deliverables"])

class ArtifactItem(BaseModel):
    id: str
    task_id: str
    file_name: str
    file_type: str
    size_bytes: int
    content_summary: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

@router.get("", response_model=List[ArtifactItem])
@router.get("/", response_model=List[ArtifactItem])
async def list_artifacts(
    task_id: Optional[str] = Query(None, description="Optional Task ID to filter deliverables"),
    db: AsyncSession = Depends(get_db)
):
    query = select(ArtifactDeliverable)
    if task_id:
        query = query.where(ArtifactDeliverable.task_id == task_id)
    query = query.order_by(ArtifactDeliverable.created_at.desc())
    res = await db.execute(query)
    return res.scalars().all()

@router.get("/task/{task_id}", response_model=List[ArtifactItem])
async def list_task_artifacts(task_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(ArtifactDeliverable)
        .where(ArtifactDeliverable.task_id == task_id)
        .order_by(ArtifactDeliverable.created_at.desc())
    )
    return res.scalars().all()

@router.get("/{artifact_id}", response_model=ArtifactItem)
async def get_artifact_metadata(artifact_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ArtifactDeliverable).where(ArtifactDeliverable.id == artifact_id))
    artifact = res.scalars().first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found.")
    return artifact

@router.get("/{artifact_id}/content")
async def get_artifact_content(artifact_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ArtifactDeliverable).where(ArtifactDeliverable.id == artifact_id))
    artifact = res.scalars().first()
    if not artifact or not os.path.exists(artifact.file_path):
        raise HTTPException(status_code=404, detail="Artifact file not found on disk.")
    
    with open(artifact.file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if artifact.file_type == "json":
        import json
        return JSONResponse(content=json.loads(content))
    return PlainTextResponse(content=content, media_type="text/markdown")

@router.get("/{artifact_id}/download")
@router.get("/download/{artifact_id}")
async def download_artifact(artifact_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ArtifactDeliverable).where(ArtifactDeliverable.id == artifact_id))
    artifact = res.scalars().first()
    if not artifact or not os.path.exists(artifact.file_path):
        raise HTTPException(status_code=404, detail="Artifact file not found on disk.")

    return FileResponse(
        path=artifact.file_path,
        filename=artifact.file_name,
        media_type="text/markdown" if artifact.file_type == "markdown" else "application/json"
    )
