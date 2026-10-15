from typing import List, Dict, Any

PREBUILT_TEMPLATES: List[Dict[str, Any]] = [
    {
        "id": "tpl-vector-db",
        "title": "Deep-Dive SaaS Vector Database Disruption & Moat Analysis",
        "category": "Market Intelligence & Infrastructure",
        "priority": "high",
        "mode": "human_in_the_loop",
        "objective": "Analyze top 3 enterprise vector database providers: Pinecone, Weaviate, and Qdrant. Compare on p99 query latency, multi-cloud availability, serverless pricing curves, SOC2 compliance, and enterprise moats.",
        "context": "Evaluating migration for a high-growth fintech platform. Critical requirements: p99 latency under 20ms at 12M monthly queries, 350GB vector dataset, multi-cloud disaster recovery, and SOC2 Type II certification.",
        "tags": ["Vector DB", "AI Infrastructure", "TCO Modeling", "Pinecone", "Qdrant", "Weaviate"]
    },
    {
        "id": "tpl-hyperscaler-ai",
        "title": "Hyperscaler LLM Gateway & Enterprise Cloud Benchmark",
        "category": "Enterprise Cloud & AI Strategy",
        "priority": "critical",
        "mode": "autonomous",
        "objective": "Benchmark AWS Bedrock, Azure OpenAI Service, and Google Cloud Vertex AI on token rate limits, regional failover, HIPAA compliance, and 3-year TCO projections.",
        "context": "Consolidating LLM inference gateways for enterprise healthcare workloads. High-volume document summarization pipeline processing 50M tokens weekly.",
        "tags": ["Hyperscalers", "AWS", "Azure", "Vertex AI", "Compliance", "TCO"]
    },
    {
        "id": "tpl-identity-consolidation",
        "title": "Zero-Trust Identity & Access Management (IAM) Vendor Audit",
        "category": "Cybersecurity & Operations",
        "priority": "medium",
        "mode": "human_in_the_loop",
        "objective": "Evaluate Okta, Microsoft Entra ID, and CyberArk on conditional access policy ergonomics, per-seat licensing cost models, and migration payback period.",
        "context": "Enterprise corporate consolidation across 4,500 active employees. Current multi-vendor sprawl costs $45,000 monthly.",
        "tags": ["IAM", "Zero-Trust", "Cybersecurity", "SaaS Pricing"]
    }
]
