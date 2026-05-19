"""Shared workflow state contract."""

from __future__ import annotations

from pydantic import BaseModel, Field

from contracts.documents import Clause, RetrievedChunk
from contracts.responses import (
    AdvisorDraftResponse,
    Citation,
    ConfidenceLevel,
    GroundingVerification,
)
from contracts.tools import PolicyComparisonResult


class AgentState(BaseModel):
    """Typed shared state for the controlled workflow."""

    user_query: str = Field(min_length=1)
    query_type: str | None = None
    plan: list[str] = Field(default_factory=list)
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)
    extracted_clauses: list[Clause] = Field(default_factory=list)
    comparison_result: PolicyComparisonResult | None = None
    draft_response: AdvisorDraftResponse | None = None
    draft_answer: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    verification: GroundingVerification | None = None
    final_answer: str | None = None
    confidence: ConfidenceLevel = "medium"
    requires_human_review: bool = True
    trace_summary: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
