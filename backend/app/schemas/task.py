from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class SubTaskSchema(BaseModel):
    id: str
    task_id: str
    title: str
    description: Optional[str] = None
    assigned_agent: str
    status: str
    execution_order: int
    dependencies: List[str] = []
    tools_assigned: List[str] = []
    input_data: Dict[str, Any] = {}
    output_data: Dict[str, Any] = {}
    error: Optional[str] = None
    duration_ms: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class PlanSchema(BaseModel):
    id: str
    task_id: str
    total_steps: int
    estimated_tokens: int
    summary: Optional[str] = None
    requires_approval: bool
    is_approved: bool
    created_at: datetime
    subtasks: Optional[List[SubTaskSchema]] = None

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, example="Deep-Dive SaaS Competitor Pricing & Moat Analysis")
    objective: str = Field(..., min_length=10, example="Analyze top 3 enterprise vector database providers: pinecone, weaviate, qdrant on pricing, indexing latency, enterprise moats, and financial ROI.")
    context: Optional[str] = Field(None, example="Targeting series-B fintech migration. Priority is multi-cloud failover, SOC2 Type II compliance, and p99 latency under 20ms.")
    priority: str = Field("medium", pattern="^(low|medium|high|critical)$")
    mode: str = Field("autonomous", pattern="^(autonomous|human_in_the_loop|supervised|hitl)$")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    mode: Optional[str] = None

class ApprovalSummary(BaseModel):
    id: str
    task_id: str
    action_type: str
    title: str
    description: str
    status: str
    payload_hash: str
    requested_at: datetime

class TaskDetail(BaseModel):
    id: str
    title: str
    objective: str
    context: Optional[str] = None
    status: str
    priority: str
    mode: str
    progress_pct: int
    validation_score: Optional[float] = None
    final_deliverable: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    subtasks: List[SubTaskSchema] = []
    plan: Optional[PlanSchema] = None
    pending_approvals: List[ApprovalSummary] = []

class TaskListResponse(BaseModel):
    tasks: List[TaskDetail]
    total: int
    active_count: int
    completed_count: int
    failed_count: int
