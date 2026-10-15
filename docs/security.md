# OmniAgent Security & Governance Architecture

OmniAgent enforces multi-layered defense-in-depth security engineered for enterprise autonomous multi-agent environments.

---

## 1. Cryptographic Human-In-The-Loop (HITL) Binding

When an agent invokes a sensitive tool (`database_update`, `notification_webhook`) or when a plan requires approval, OmniAgent generates a tamper-evident payload signature:

$$\text{HMAC-SHA256}(\text{SECRET\_KEY}, \text{task\_id} \mathbin{\Vert} \text{action\_type} \mathbin{\Vert} \text{canonical\_params\_json})$$

### Security Guarantees:
- **Parameter Non-Repudiation**: If any tool parameter is altered (even by a single character) between proposal and approval, the signature validation fails immediately.
- **Workflow State Binding**: Approvals cannot be replayed across different workflow runs or tasks.
- **Backend Enforced**: Approval validation is strictly computed on the backend server; frontend controls cannot bypass authorization checks.

---

## 2. Prompt Injection Guardrails

OmniAgent analyzes all user objectives, retrieved external documents, and tool outputs with an active injection detector before prompt assembly:

```python
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s*prompt\s*override",
    r"disregard\s+(the\s+)?rules",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"dan\s+mode",
    r"sudo\s+mode",
]
```

If an injection signature is discovered, the workflow terminates immediately with status `failed`, alerts the operator, and logs a security violation audit record.

---

## 3. Strict Tool Sandboxing & Permission Boundaries

- **Zero Arbitrary Execution**: Agents do not have access to arbitrary shell environments, `eval()`, unrestricted SQL strings, or system system subprocesses.
- **Typed Pydantic Schemas**: Every tool parameter is validated against an explicit Pydantic schema before invocation.
- **Read vs. Sensitive Classification**:
  - `web_search`: Safe (Read-only)
  - `document_ingestion`: Safe (Deterministic AST extractor)
  - `financial_calculator`: Safe (Pure Python mathematical model)
  - `matrix_transformer`: Safe (Deterministic composite scorer)
  - `database_update`: **CRITICAL** (Requires human authorization)
  - `notification_webhook`: **HIGH** (Requires human authorization)

---

## 4. Tenant & Context Isolation

- Durable tasks, subtasks, and persisted deliverables are keyed by unique UUIDs.
- Working memory is strictly scoped per `task_id` and wiped upon finalization or cancellation.
- Cross-user data leakage is prevented via user authorization dependencies.
- API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `SECRET_KEY`) are masked in settings responses and never written to execution logs.
