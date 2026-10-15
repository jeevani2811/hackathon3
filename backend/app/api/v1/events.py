from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.app.core.events import event_bus

router = APIRouter(prefix="/events", tags=["Real-Time Events"])

@router.get("/stream/{task_id}")
async def stream_task_events(task_id: str):
    """
    Server-Sent Events (SSE) streaming endpoint for live execution observability.
    Emits subtask transitions, agent thoughts, tool calls, approvals, and completion reports.
    """
    return StreamingResponse(
        event_bus.event_generator(task_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
