# OmniAgent REST API Specification (v1)

Base URL: `/api/v1`

---

## 1. Diagnostics & Health

### `GET /api/v1/health`
Returns system operational health, database readiness, memory usage, and runtime metrics.

**Response (200 OK):**
```json
{
  "status": "HEALTHY",
  "service": "OmniAgent Intelligent Systems",
  "version": "1.0.0",
  "database_connected": true,
  "uptime_seconds": 1420,
  "ai_provider": "mock",
  "system_metrics": {
    "ram_usage_pct": 42.5,
    "cpu_count": 8
  }
}
```

---

## 2. Authentication

### `POST /api/v1/auth/login`
Authenticates user identity and issues a signed JWT bearer token.

**Request:**
```json
{
  "email": "analyst@enterprise.ai",
  "password": "demo1234"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "usr-demo-001",
    "email": "analyst@enterprise.ai",
    "name": "Lead Strategy Analyst",
    "role": "lead_analyst"
  }
}
```

---

## 3. Tasks & Workflows

### `POST /api/v1/tasks`
Creates a new strategic task and dispatches autonomous multi-agent orchestration.

**Request:**
```json
{
  "title": "Deep-Dive SaaS Vector Database Disruption & Moat Analysis",
  "objective": "Analyze top 3 enterprise vector database providers: Pinecone, Weaviate, and Qdrant on p99 latency, enterprise compliance, and multi-year TCO.",
  "context": "Fintech cloud migration.",
  "priority": "high",
  "mode": "human_in_the_loop"
}
```

### `GET /api/v1/tasks`
Query parameters:
- `status`: `pending`, `planning`, `awaiting_approval`, `running`, `paused`, `completed`, `failed`
- `priority`: `low`, `medium`, `high`, `critical`
- `search`: Keyword search string

### `GET /api/v1/tasks/{id}`
Returns full task details including DAG subtasks, generated execution plan, pending approvals, and compiled deliverables.

### Lifecycle Control Endpoints:
- `POST /api/v1/tasks/{id}/pause`
- `POST /api/v1/tasks/{id}/resume`
- `POST /api/v1/tasks/{id}/cancel`
- `POST /api/v1/tasks/{id}/retry`

---

## 4. Human-In-The-Loop Approvals

### `GET /api/v1/approvals`
Lists pending or decided approval requests.

### `POST /api/v1/approvals/{id}/decide`
Submits human operator decision on sensitive operations.

**Request:**
```json
{
  "decision": "approve",
  "decision_notes": "Reviewed pricing boundaries; approved catalog write."
}
```

---

## 5. Real-Time Observability (SSE)

### `GET /api/v1/events/stream/{task_id}`
Server-Sent Events (SSE) stream emitting real-time subtask transitions, agent thoughts, tool execution results, and validation reports.

**Stream Protocol:**
```
event: subtask_started
data: {"task_id":"...","subtask_id":"...","title":"Gather Competitive Market Evidence","agent":"Research Agent"}

event: subtask_completed
data: {"task_id":"...","duration_ms":1250,"summary":"Gathered 3 verified market evidence profiles..."}
```

---

## 6. Agent Fleet & Tools

### `GET /api/v1/agents`
Returns catalog of specialized agents (`Planner`, `Research`, `Execution`, `Analysis`, `Validation`), their assigned tools, system prompt, and telemetry.

### `GET /api/v1/tools`
Returns registered tool schemas, parameter definitions, and sensitivity classifications.
