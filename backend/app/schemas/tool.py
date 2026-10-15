from typing import Dict, Any, List
from pydantic import BaseModel

class ToolParameterSpec(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

class ToolDefinition(BaseModel):
    name: str
    description: str
    category: str
    is_sensitive: bool
    requires_approval: bool
    timeout_seconds: int
    parameters: List[ToolParameterSpec]
    output_schema: Dict[str, Any]
