"""Tool input and output contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from contracts.documents import Clause, ComparisonItem, RetrievedChunk
from contracts.responses import AdvisorDraftResponse, Citation, GroundingVerification


class DocumentFilters(BaseModel):
    """Optional metadata filters for retrieval."""

    document_type: str | None = None
    product: str | None = None
    document_name: str | None = None
    version: str | None = None


class RetrievalQuery(BaseModel):
    """Input contract for the document retrieval tool."""

    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
    filters: DocumentFilters = Field(default_factory=DocumentFilters)


class DocumentRetrievalResult(BaseModel):
    """Output contract for the document retrieval tool."""

    chunks: list[RetrievedChunk] = Field(default_factory=list)


ToolErrorKind = Literal[
    "configuration_failure",
    "dependency_failure",
    "backend_failure",
    "input_validation_failure",
    "extraction_failure",
    "comparison_failure",
    "verification_failure",
    "drafting_failure",
    "workflow_failure",
]


class ToolError(BaseModel):
    """Typed failure contract for independently callable tools."""

    kind: ToolErrorKind
    message: str = Field(min_length=1)


class DocumentRetrievalToolResult(BaseModel):
    """Typed success or failure result for the retrieval tool wrapper."""

    ok: bool
    result: DocumentRetrievalResult | None = None
    error: ToolError | None = None


class ClauseExtractionResult(BaseModel):
    """Output contract for the clause extraction tool."""

    clauses: list[Clause] = Field(default_factory=list)


class ClauseExtractionToolResult(BaseModel):
    """Typed success or failure result for the clause extraction tool wrapper."""

    ok: bool
    result: ClauseExtractionResult | None = None
    error: ToolError | None = None


class PolicyComparisonResult(BaseModel):
    """Output contract for policy comparison results."""

    comparison_points: list[ComparisonItem] = Field(default_factory=list)
    sufficient_information: bool = True
    notes: list[str] = Field(default_factory=list)


class PolicyComparisonToolResult(BaseModel):
    """Typed success or failure result for the policy comparison tool wrapper."""

    ok: bool
    result: PolicyComparisonResult | None = None
    error: ToolError | None = None


class GroundingVerificationResult(BaseModel):
    """Output contract for grounding verification."""

    verification: GroundingVerification
    reviewed_citations: list[Citation] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class CitationVerifierToolResult(BaseModel):
    """Typed success or failure result for the citation verifier tool wrapper."""

    ok: bool
    result: GroundingVerificationResult | None = None
    error: ToolError | None = None


class ResponseDraftToolResult(BaseModel):
    """Typed success or failure result for the response draft tool wrapper."""

    ok: bool
    result: AdvisorDraftResponse | None = None
    error: ToolError | None = None
