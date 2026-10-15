# OmniAgent Backend Service

High-performance Python FastAPI multi-agent orchestration backend with asynchronous DAG scheduling, persistent state, deterministic computational tooling, and Server-Sent Events (SSE) streaming.

## Features

- **Agent Fleet**: Planner, Research, Execution, Analysis, and Validation Agents.
- **Workflow State Machine**: `pending`, `planning`, `awaiting_approval`, `running`, `paused`, `completed`, `failed`, `cancelled`.
- **Human-in-the-Loop Engine**: Cryptographic payload integrity hashing and authorization controls for sensitive tools (`database_update`, `notification_webhook`).
- **Deterministic Math Engine**: Non-hallucinated financial calculations (1-yr & 3-yr TCO, ROI %, payback period).
- **Persistent Storage**: SQLAlchemy with async SQLite or PostgreSQL.
- **Streaming Observability**: Server-Sent Events (SSE) broadcasting real-time agent thoughts and subtask lifecycle events.

## Running Locally

```bash
# 1. Activate Virtual Environment
source venv/bin/activate  # Or backend\venv\Scripts\Activate.ps1 on Windows

# 2. Run Database Initializer & FastAPI Dev Server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation available at: `http://localhost:8000/docs`
