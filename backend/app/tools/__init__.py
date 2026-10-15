from backend.app.tools.registry import tool_registry
from backend.app.schemas.tool import ToolParameterSpec

from backend.app.tools.web_search import execute_web_search
from backend.app.tools.document_ingestion import execute_document_ingestion
from backend.app.tools.financial_calculator import execute_financial_calculator
from backend.app.tools.matrix_transformer import execute_matrix_transformer
from backend.app.tools.database_update import execute_database_update
from backend.app.tools.notification_webhook import execute_notification_webhook
from backend.app.tools.report_generator import execute_report_generator

# Register Web Search
tool_registry.register(
    name="web_search",
    description="Searches verified market, SEC, and architectural databases for factual intelligence.",
    category="research",
    func=execute_web_search,
    parameters=[
        ToolParameterSpec(name="query", type="string", description="The search query topic or entity name", required=True),
        ToolParameterSpec(name="domain_filter", type="string", description="Optional domain restriction", required=False, default="")
    ],
    output_schema={"type": "object", "properties": {"verified_evidence": {"type": "array"}}},
    timeout_seconds=20,
    is_sensitive=False
)

# Register Document Ingestion
tool_registry.register(
    name="document_ingestion",
    description="Parses enterprise documents, extracting metrics, constraints, and compliance signals.",
    category="processing",
    func=execute_document_ingestion,
    parameters=[
        ToolParameterSpec(name="document_name", type="string", description="Name of the document", required=True),
        ToolParameterSpec(name="document_text", type="string", description="Raw text content of document", required=False, default="")
    ],
    output_schema={"type": "object", "properties": {"extracted_metrics": {"type": "object"}}},
    timeout_seconds=20,
    is_sensitive=False
)

# Register Financial Calculator
tool_registry.register(
    name="financial_calculator",
    description="Deterministic calculation of multi-year TCO, ROI percentage, and sensitivity analysis.",
    category="computational",
    func=execute_financial_calculator,
    parameters=[
        ToolParameterSpec(name="monthly_queries_million", type="number", description="Monthly queries in millions", required=False, default=10.0),
        ToolParameterSpec(name="storage_gb", type="number", description="Storage in gigabytes", required=False, default=250.0),
        ToolParameterSpec(name="developer_count", type="integer", description="Engineering team size", required=False, default=5),
        ToolParameterSpec(name="legacy_monthly_cost", type="number", description="Current monthly cost in USD", required=False, default=8500.0),
        ToolParameterSpec(name="hourly_engineer_rate", type="number", description="Hourly engineering rate in USD", required=False, default=120.0)
    ],
    output_schema={"type": "object", "properties": {"annual_comparisons": {"type": "object"}}},
    timeout_seconds=15,
    is_sensitive=False
)

# Register Matrix Transformer
tool_registry.register(
    name="matrix_transformer",
    description="Transforms collected qualitative evidence into a normalized comparative evaluation matrix.",
    category="analysis",
    func=execute_matrix_transformer,
    parameters=[
        ToolParameterSpec(name="competitors", type="array", description="List of competitors", required=False),
        ToolParameterSpec(name="evaluation_dimensions", type="array", description="List of dimensions", required=False)
    ],
    output_schema={"type": "object", "properties": {"matrix": {"type": "array"}}},
    timeout_seconds=15,
    is_sensitive=False
)

# Register Database Update (SENSITIVE)
tool_registry.register(
    name="database_update",
    description="SENSITIVE: Writes approved findings to enterprise corporate knowledge base / catalog.",
    category="database",
    func=execute_database_update,
    parameters=[
        ToolParameterSpec(name="catalog_table", type="string", description="Catalog table name", required=True),
        ToolParameterSpec(name="record_key", type="string", description="Primary entity key", required=True),
        ToolParameterSpec(name="record_payload", type="object", description="Payload to write", required=True),
        ToolParameterSpec(name="commit_reason", type="string", description="Reason for update", required=False, default="Auto strategic update")
    ],
    output_schema={"type": "object", "properties": {"status": {"type": "string"}}},
    timeout_seconds=15,
    is_sensitive=True
)

# Register Notification Webhook (SENSITIVE)
tool_registry.register(
    name="notification_webhook",
    description="SENSITIVE: Dispatches external executive briefings to stakeholder endpoints or webhooks.",
    category="integrations",
    func=execute_notification_webhook,
    parameters=[
        ToolParameterSpec(name="channel_or_endpoint", type="string", description="Destination webhook or channel", required=True),
        ToolParameterSpec(name="subject", type="string", description="Subject line", required=True),
        ToolParameterSpec(name="summary_markdown", type="string", description="Brief summary in markdown", required=True),
        ToolParameterSpec(name="priority", type="string", description="Priority level", required=False, default="normal")
    ],
    output_schema={"type": "object", "properties": {"status": {"type": "string"}}},
    timeout_seconds=15,
    is_sensitive=True
)

# Register Report Generator
tool_registry.register(
    name="report_generator",
    description="Compiles verified evidence, matrix, and calculations into downloadable deliverables.",
    category="artifacts",
    func=execute_report_generator,
    parameters=[
        ToolParameterSpec(name="task_id", type="string", description="Task UUID", required=True),
        ToolParameterSpec(name="title", type="string", description="Report title", required=True),
        ToolParameterSpec(name="executive_summary", type="string", description="High-level narrative summary", required=True),
        ToolParameterSpec(name="evidence_items", type="array", description="Evidence list", required=False),
        ToolParameterSpec(name="financial_data", type="object", description="Financial TCO data", required=False),
        ToolParameterSpec(name="matrix_data", type="object", description="Competitive matrix data", required=False),
        ToolParameterSpec(name="strategic_recommendations", type="array", description="List of recommendations", required=False)
    ],
    output_schema={"type": "object", "properties": {"markdown_content": {"type": "string"}}},
    timeout_seconds=25,
    is_sensitive=False
)
