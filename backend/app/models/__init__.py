import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.base import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="analyst")  # admin, lead_analyst, analyst
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    objective = Column(Text, nullable=False)
    context = Column(Text, nullable=True)
    # pending, planning, awaiting_approval, running, paused, completed, failed, cancelled
    status = Column(String, default="pending", index=True)
    priority = Column(String, default="medium")  # low, medium, high, critical
    mode = Column(String, default="autonomous")   # autonomous, human_in_the_loop
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    workspace_id = Column(String, nullable=True)
    
    # Progress & Metrics
    progress_pct = Column(Integer, default=0)
    validation_score = Column(Float, nullable=True)
    final_deliverable = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="tasks")
    plan = relationship("Plan", back_populates="task", uselist=False, cascade="all, delete-orphan")
    subtasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan", order_by="SubTask.execution_order")
    approvals = relationship("ApprovalRequest", back_populates="task", cascade="all, delete-orphan")
    events = relationship("EventRecord", back_populates="task", cascade="all, delete-orphan")
    memories = relationship("MemoryItem", back_populates="task", cascade="all, delete-orphan")
    artifacts = relationship("ArtifactDeliverable", back_populates="task", cascade="all, delete-orphan")

    @property
    def pending_approvals(self):
        return [a for a in (self.approvals or []) if a.status == "pending"]


class Plan(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), unique=True, nullable=False)
    total_steps = Column(Integer, default=0)
    estimated_tokens = Column(Integer, default=0)
    summary = Column(Text, nullable=True)
    requires_approval = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="plan")
    subtasks = relationship("SubTask", back_populates="plan", cascade="all, delete-orphan")


class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    assigned_agent = Column(String, nullable=False)  # Planner, Research, Execution, Analysis, Validation
    # pending, ready, running, awaiting_approval, completed, failed, skipped
    status = Column(String, default="pending", index=True)
    execution_order = Column(Integer, default=0)
    dependencies = Column(JSON, default=list)  # list of subtask IDs that must complete first
    tools_assigned = Column(JSON, default=list)
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    error = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    duration_ms = Column(Integer, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="subtasks")
    plan = relationship("Plan", back_populates="subtasks")


class AgentRecord(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    system_prompt = Column(Text, nullable=False)
    authorized_tools = Column(JSON, default=list)
    status = Column(String, default="idle")  # idle, active, error
    total_tasks_executed = Column(Integer, default=0)
    successful_tasks = Column(Integer, default=0)
    avg_duration_ms = Column(Float, default=0.0)


class ToolInvocation(Base):
    __tablename__ = "tool_invocations"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    subtask_id = Column(String, nullable=True)
    agent_name = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    parameters = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    is_sensitive = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=True)
    duration_ms = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    subtask_id = Column(String, nullable=True)
    action_type = Column(String, nullable=False)  # plan_approval, sensitive_tool, state_change
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    parameters = Column(JSON, default=dict)
    payload_hash = Column(String, nullable=False)  # integrity checksum
    # pending, approved, rejected, modified
    status = Column(String, default="pending", index=True)
    decision_notes = Column(Text, nullable=True)
    decided_by = Column(String, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="approvals")


class EventRecord(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)  # task_started, agent_action, tool_called, approval_requested, validation_completed, etc.
    agent_name = Column(String, nullable=True)
    payload = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="events")


class MemoryItem(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False, index=True)
    memory_type = Column(String, default="evidence")  # objective, evidence, assumption, calculation, constraint
    key = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="memories")


class ArtifactDeliverable(Base):
    __tablename__ = "artifacts"

    id = Column(String, primary_key=True, default=generate_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # markdown, json, pdf, csv
    size_bytes = Column(Integer, default=0)
    content_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="artifacts")
