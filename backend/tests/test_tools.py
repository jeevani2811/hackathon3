import pytest
from backend.app.tools.registry import tool_registry
from backend.app.tools.financial_calculator import execute_financial_calculator
from backend.app.tools.matrix_transformer import execute_matrix_transformer
import backend.app.tools  # Ensure tools are registered

@pytest.mark.asyncio
async def test_tool_registry_registration():
    tools = tool_registry.list_tools()
    tool_names = [t.name for t in tools]
    assert "web_search" in tool_names
    assert "financial_calculator" in tool_names
    assert "matrix_transformer" in tool_names
    assert "database_update" in tool_names
    assert "notification_webhook" in tool_names
    assert "report_generator" in tool_names

@pytest.mark.asyncio
async def test_financial_calculator_math():
    res = execute_financial_calculator(
        monthly_queries_million=10.0,
        storage_gb=250.0,
        developer_count=5,
        legacy_monthly_cost=8500.0,
        hourly_engineer_rate=120.0
    )
    assert res["math_verified"] is True
    assert "annual_comparisons" in res
    assert "Pinecone_Serverless" in res["annual_comparisons"]
    assert "Qdrant_Cloud" in res["annual_comparisons"]
    assert res["annual_comparisons"]["Legacy_Infrastructure"]["annual_cost_usd"] == 102000.0

@pytest.mark.asyncio
async def test_sensitive_tool_permission_enforcement():
    # Attempting to execute sensitive tool without approval must fail with PermissionError
    with pytest.raises(PermissionError):
        await tool_registry.execute_tool(
            name="database_update",
            parameters={"catalog_table": "test", "record_key": "k", "record_payload": {}},
            is_approved=False
        )

    # With is_approved=True, execution succeeds
    res = await tool_registry.execute_tool(
        name="database_update",
        parameters={"catalog_table": "test", "record_key": "k", "record_payload": {}},
        is_approved=True
    )
    assert res["success"] is True
    assert res["result"]["status"] == "COMMITTED"
