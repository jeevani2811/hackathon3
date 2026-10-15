from typing import List
from fastapi import APIRouter
from backend.app.schemas.agent import AgentInfo
from backend.app.agents import AGENT_FLEET

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("", response_model=List[AgentInfo])
async def list_agents():
    agents = []
    metric_map = {
        "Planner Agent": {"tasks": 42, "success": 41, "duration": 820.0},
        "Research Agent": {"tasks": 118, "success": 115, "duration": 1250.0},
        "Execution Agent": {"tasks": 94, "success": 94, "duration": 430.0},
        "Analysis Agent": {"tasks": 76, "success": 75, "duration": 1410.0},
        "Validation Agent": {"tasks": 68, "success": 68, "duration": 620.0}
    }
    for name, agent in AGENT_FLEET.items():
        m = metric_map.get(name, {"tasks": 10, "success": 10, "duration": 500.0})
        agents.append(
            AgentInfo(
                id=f"agent-{name.lower().replace(' ', '-')}",
                name=agent.name,
                role=agent.role,
                description=f"Specialized {agent.role} in OmniAgent Multi-Agent Architecture.",
                system_prompt=agent.system_prompt.strip(),
                authorized_tools=agent.authorized_tools,
                status="active",
                total_tasks_executed=m["tasks"],
                successful_tasks=m["success"],
                avg_duration_ms=m["duration"]
            )
        )
    return agents
