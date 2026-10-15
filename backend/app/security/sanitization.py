import re
from typing import Any, Dict

PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s*prompt\s*override",
    r"disregard\s+(the\s+)?rules",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"dan\s+mode",
    r"sudo\s+mode",
]

def sanitize_user_input(text: str) -> str:
    """
    Sanitizes user input by stripping dangerous terminal escapes and flagging prompt injection keywords.
    """
    if not text:
        return ""
    # Strip null bytes and non-printable control characters
    cleaned = "".join(ch for ch in text if ch.isprintable() or ch in "\n\r\t")
    return cleaned.strip()

def detect_prompt_injection(text: str) -> bool:
    """
    Returns True if malicious prompt override patterns are detected in user or retrieved text.
    """
    if not text:
        return False
    lower_text = text.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, lower_text):
            return True
    return False

def sanitize_tool_parameters(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep sanitizes tool parameter dictionary to prevent code/command execution escapes.
    """
    sanitized = {}
    for k, v in parameters.items():
        if isinstance(v, str):
            sanitized[k] = sanitize_user_input(v)
        elif isinstance(v, dict):
            sanitized[k] = sanitize_tool_parameters(v)
        elif isinstance(v, list):
            sanitized[k] = [
                sanitize_user_input(item) if isinstance(item, str) else item 
                for item in v
            ]
        else:
            sanitized[k] = v
    return sanitized
