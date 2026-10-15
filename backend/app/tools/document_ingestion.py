from typing import Dict, Any, List

def execute_document_ingestion(document_name: str, document_text: str = "") -> Dict[str, Any]:
    """
    Ingests technical architecture notes, pricing proposals, or 10-K filings,
    extracting structured financial figures, constraints, and compliance attributes.
    """
    lines = [line.strip() for line in document_text.splitlines() if line.strip()]
    
    extracted_metrics = {}
    extracted_constraints = []
    
    for line in lines:
        lower = line.lower()
        if "budget" in lower or "$" in line or "cost" in lower:
            extracted_metrics["budget_signal"] = line
        if "latency" in lower or "ms" in lower:
            extracted_metrics["latency_target"] = line
        if "soc2" in lower or "hipaa" in lower or "compliance" in lower or "iso" in lower:
            extracted_constraints.append(line)
        if "migration" in lower or "deadline" in lower or "q4" in lower or "q1" in lower:
            extracted_constraints.append(line)

    return {
        "document_name": document_name,
        "total_lines_parsed": len(lines),
        "extracted_metrics": extracted_metrics,
        "extracted_constraints": extracted_constraints,
        "status": "SUCCESS",
        "ingestion_method": "Deterministic AST / Key-Phrase Extractor"
    }
