import pytest
import httpx
from backend.app.main import app
from backend.app.db.session import init_db

@pytest.fixture(autouse=True)
async def setup_database():
    await init_db()
    yield

@pytest.mark.asyncio
async def test_health_check_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] in ["HEALTHY", "DEGRADED"]
        assert "uptime_seconds" in data
        assert "service" in data

@pytest.mark.asyncio
async def test_settings_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/settings")
        assert res.status_code == 200
        data = res.json()
        assert "ai_provider" in data
        assert "available_providers" in data

@pytest.mark.asyncio
async def test_list_agents_endpoint():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/v1/agents")
        assert res.status_code == 200
        agents = res.json()
        assert len(agents) >= 5
        agent_names = [a["name"] for a in agents]
        assert "Planner Agent" in agent_names
        assert "Research Agent" in agent_names
        assert "Execution Agent" in agent_names
        assert "Analysis Agent" in agent_names
        assert "Validation Agent" in agent_names

@pytest.mark.asyncio
async def test_create_task_and_inspect():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        create_payload = {
            "title": "API Test Vector Database Evaluation",
            "objective": "Evaluate Pinecone, Weaviate, and Qdrant on p99 latency, enterprise compliance, and multi-year TCO.",
            "context": "Fintech cloud migration.",
            "priority": "high",
            "mode": "autonomous"
        }
        res = await client.post("/api/v1/tasks", json=create_payload)
        assert res.status_code == 200
        task_data = res.json()
        task_id = task_data["id"]
        assert task_data["title"] == create_payload["title"]
        assert task_data["status"] in ["pending", "planning", "running"]

        # Fetch detail
        detail_res = await client.get(f"/api/v1/tasks/{task_id}")
        assert detail_res.status_code == 200
        detail = detail_res.json()
        assert detail["id"] == task_id

@pytest.mark.asyncio
async def test_artifacts_endpoints():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Listing artifacts
        res = await client.get("/api/v1/artifacts")
        assert res.status_code == 200
        assert isinstance(res.json(), list)

@pytest.mark.asyncio
async def test_hitl_task_creation():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "title": "Supervised HITL Task Evaluation",
            "objective": "Evaluate strategic enterprise procurement with human approval checkpoints.",
            "context": "Compliance with strict security governance.",
            "priority": "critical",
            "mode": "human_in_the_loop"
        }
        res = await client.post("/api/v1/tasks", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["mode"] == "human_in_the_loop"
        assert data["priority"] == "critical"
