"""Deterministic query-scope classification for supported insurance workflows."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

QueryScope = Literal["supported", "unsupported"]

SUPPORTED_QUERY_TOKENS = {
    "accident",
    "accidente",
    "authorization",
    "autorizacion",
    "autorización",
    "benefit",
    "beneficio",
    "claim",
    "clause",
    "clausula",
    "cláusula",
    "compare",
    "comparison",
    "copay",
    "copago",
    "comparacion",
    "comparación",
    "comparar",
    "coverage",
    "cobertura",
    "covered",
    "deductible",
    "deducible",
    "difference",
    "diferencia",
    "endorsement",
    "endoso",
    "exclusion",
    "exclusión",
    "hospital",
    "hospitalizacion",
    "hospitalización",
    "insurance",
    "poliza",
    "policy",
    "póliza",
    "premium",
    "prima",
    "procedure",
    "procedimiento",
    "reembolso",
    "reimbursement",
    "restriccion",
    "restriction",
    "restricción",
    "versus",
    "vs",
}


class QueryScopeDecision(BaseModel):
    """Typed scope decision for one user query."""

    scope: QueryScope
    reason: str = Field(min_length=1)


def classify_query_scope(user_query: str) -> QueryScopeDecision:
    """Return a deterministic scope decision for one user query."""

    normalized_tokens = {
        token.strip(".,:;!?()[]{}'\"").lower()
        for token in user_query.split()
        if token.strip(".,:;!?()[]{}'\"")
    }
    if normalized_tokens & SUPPORTED_QUERY_TOKENS:
        return QueryScopeDecision(
            scope="supported",
            reason="Query matches supported insurance-document workflow patterns.",
        )
    return QueryScopeDecision(
        scope="unsupported",
        reason="Query is outside the supported insurance-document scope.",
    )
