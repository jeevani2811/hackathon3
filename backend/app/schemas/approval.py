from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ApprovalDecision(BaseModel):
    decision: str = Field(..., pattern="^(approve|approved|reject|rejected|modify|modified)$")
    decision_notes: Optional[str] = Field(None)
    modified_parameters: Optional[Dict[str, Any]] = None

class ApprovalResponse(BaseModel):
    id: str
    task_id: str
    action_type: str
    title: str
    description: str
    parameters: Dict[str, Any]
    payload_hash: str
    status: str
    decision_notes: Optional[str] = None
    decided_by: Optional[str] = None
    requested_at: datetime
    decided_at: Optional[datetime] = None
