import hmac
import hashlib
import json
from typing import Dict, Any
from backend.app.core.config import settings

def calculate_action_payload_hash(task_id: str, action_type: str, parameters: Dict[str, Any]) -> str:
    """
    Computes a cryptographic HMAC-SHA256 signature over task_id, action_type, and sorted parameters.
    This guarantees that if parameters or action details are modified, previous approvals are instantly invalidated.
    """
    canonical_params = json.dumps(parameters, sort_keys=True)
    payload_raw = f"{task_id}::{action_type}::{canonical_params}"
    sig = hmac.new(
        settings.SECRET_KEY.encode('utf-8'),
        payload_raw.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return sig

def verify_action_payload_hash(task_id: str, action_type: str, parameters: Dict[str, Any], expected_hash: str) -> bool:
    computed = calculate_action_payload_hash(task_id, action_type, parameters)
    return hmac.compare_digest(computed, expected_hash)

SENSITIVE_TOOLS = {
    "database_update": {
        "risk_level": "CRITICAL",
        "reason": "Direct state modification of corporate enterprise catalog"
    },
    "notification_webhook": {
        "risk_level": "HIGH",
        "reason": "External communications dispatched to third-party endpoints / webhooks"
    }
}

def is_tool_sensitive(tool_name: str) -> bool:
    return tool_name in SENSITIVE_TOOLS
