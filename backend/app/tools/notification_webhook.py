import time
from typing import Dict, Any

async def execute_notification_webhook(
    channel_or_endpoint: str,
    subject: str,
    summary_markdown: str,
    priority: str = "normal"
) -> Dict[str, Any]:
    """
    SENSITIVE OPERATION: Dispatches an external notification alert (e.g. Slack, Teams, Email, PagerDuty).
    Requires explicit human approval before execution.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())
    
    return {
        "status": "DISPATCHED",
        "destination": channel_or_endpoint,
        "subject": subject,
        "priority": priority,
        "delivered_at": timestamp,
        "receipt_id": f"msg-ack-{int(time.time())}",
        "summary_preview": summary_markdown[:150] + ("..." if len(summary_markdown) > 150 else "")
    }
