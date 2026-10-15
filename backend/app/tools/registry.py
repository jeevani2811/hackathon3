import time
import inspect
from typing import Dict, Any, Callable, List, Optional
from pydantic import BaseModel
from backend.app.schemas.tool import ToolDefinition, ToolParameterSpec
from backend.app.security.permissions import is_tool_sensitive
from backend.app.security.sanitization import sanitize_tool_parameters
from backend.app.core.logging import logger

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register(
        self,
        name: str,
        description: str,
        category: str,
        func: Callable,
        parameters: List[ToolParameterSpec],
        output_schema: Dict[str, Any],
        timeout_seconds: int = 30,
        is_sensitive: bool = False
    ):
        self._tools[name] = {
            "name": name,
            "description": description,
            "category": category,
            "func": func,
            "parameters": parameters,
            "output_schema": output_schema,
            "timeout_seconds": timeout_seconds,
            "is_sensitive": is_sensitive or is_tool_sensitive(name),
            "requires_approval": is_sensitive or is_tool_sensitive(name)
        }
        logger.info(f"Registered tool: {name} (sensitive={self._tools[name]['is_sensitive']})")

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        return self._tools.get(name)

    def list_tools(self) -> List[ToolDefinition]:
        return [
            ToolDefinition(
                name=t["name"],
                description=t["description"],
                category=t["category"],
                is_sensitive=t["is_sensitive"],
                requires_approval=t["requires_approval"],
                timeout_seconds=t["timeout_seconds"],
                parameters=t["parameters"],
                output_schema=t["output_schema"]
            )
            for t in self._tools.values()
        ]

    async def execute_tool(
        self, 
        name: str, 
        parameters: Dict[str, Any], 
        task_id: str = "",
        is_approved: bool = False
    ) -> Dict[str, Any]:
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' is not registered in system.")

        if tool["is_sensitive"] and not is_approved:
            raise PermissionError(f"Tool '{name}' is sensitive and requires explicit human approval.")

        # Sanitize parameters
        clean_params = sanitize_tool_parameters(parameters)

        start_time = time.time()
        try:
            func = tool["func"]
            if inspect.iscoroutinefunction(func):
                result = await func(**clean_params)
            else:
                result = func(**clean_params)

            duration_ms = int((time.time() - start_time) * 1000)
            return {
                "success": True,
                "tool_name": name,
                "duration_ms": duration_ms,
                "result": result,
                "error": None
            }
        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "tool_name": name,
                "duration_ms": duration_ms,
                "result": None,
                "error": str(e)
            }

tool_registry = ToolRegistry()
