from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.schemas.tool import ToolDefinition
from backend.app.tools.registry import tool_registry

router = APIRouter(prefix="/tools", tags=["Tools"])

class ToolTestRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]

@router.get("", response_model=List[ToolDefinition])
async def list_tools():
    return tool_registry.list_tools()

@router.get("/{name}", response_model=ToolDefinition)
async def get_tool(name: str):
    tool = tool_registry.get_tool(name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return ToolDefinition(
        name=tool["name"],
        description=tool["description"],
        category=tool["category"],
        is_sensitive=tool["is_sensitive"],
        requires_approval=tool["requires_approval"],
        timeout_seconds=tool["timeout_seconds"],
        parameters=tool["parameters"],
        output_schema=tool["output_schema"]
    )

@router.post("/test")
async def test_tool(req: ToolTestRequest):
    tool = tool_registry.get_tool(req.tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    if tool["is_sensitive"]:
        raise HTTPException(status_code=403, detail="Direct invocation of sensitive tools requires workflow authorization context.")

    result = await tool_registry.execute_tool(
        name=req.tool_name,
        parameters=req.parameters,
        is_approved=True
    )
    return result
