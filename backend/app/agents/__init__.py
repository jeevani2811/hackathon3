from backend.app.agents.planner import PlannerAgent
from backend.app.agents.research import ResearchAgent
from backend.app.agents.execution import ExecutionAgent
from backend.app.agents.analysis import AnalysisAgent
from backend.app.agents.validation import ValidationAgent

planner_agent = PlannerAgent()
research_agent = ResearchAgent()
execution_agent = ExecutionAgent()
analysis_agent = AnalysisAgent()
validation_agent = ValidationAgent()

AGENT_FLEET = {
    "Planner Agent": planner_agent,
    "Research Agent": research_agent,
    "Execution Agent": execution_agent,
    "Analysis Agent": analysis_agent,
    "Validation Agent": validation_agent
}

def get_agent(name: str):
    return AGENT_FLEET.get(name) or AGENT_FLEET.get(f"{name} Agent")
