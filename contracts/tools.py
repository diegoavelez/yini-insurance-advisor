"""Tool input and output contracts."""

from __future__ import annotations

from pydantic import BaseModel, Field

from contracts.documents import Clause, ComparisonItem, RetrievedChunk
from contracts.responses import GroundingVerification


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


class ClauseExtractionResult(BaseModel):
    """Output contract for the clause extraction tool."""

    clauses: list[Clause] = Field(default_factory=list)


class PolicyComparisonResult(BaseModel):
    """Output contract for policy comparison results."""

    comparison_points: list[ComparisonItem] = Field(default_factory=list)
    sufficient_information: bool = True
    notes: list[str] = Field(default_factory=list)


class GroundingVerificationResult(BaseModel):
    """Output contract for grounding verification."""

    verification: GroundingVerification
