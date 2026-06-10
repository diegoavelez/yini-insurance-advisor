"""Response, citation, and grounding contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ConfidenceLevel = Literal["high", "medium", "low"]


class Citation(BaseModel):
    """A citation that traces an answer back to source material."""

    document_name: str = Field(min_length=1)
    source_pdf_relative_path: str | None = None
    chunk_id: str | None = None
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    clause_id: str | None = None
    quote: str | None = None


class DocumentaryBasisItem(BaseModel):
    """A structured documentary support entry for advisor review."""

    document_name: str = Field(min_length=1)
    source_pdf_relative_path: str | None = None
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    clause_id: str | None = None
    note: str | None = None


class GroundingVerification(BaseModel):
    """Grounding assessment for a draft answer."""

    supported: bool
    confidence: ConfidenceLevel
    unsupported_claims: list[str] = Field(default_factory=list)
    missing_citations: list[str] = Field(default_factory=list)


class AdvisorDraftResponse(BaseModel):
    """Structured advisor-facing response draft."""

    suggested_answer: str = Field(min_length=1)
    documentary_basis: list[DocumentaryBasisItem] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    confidence: ConfidenceLevel
    limitations: list[str] = Field(default_factory=list)
    advisor_review_notice: str = Field(min_length=1)


class GroundedAnswerResult(BaseModel):
    """Typed grounded-QA output for the first answer-generation slice."""

    query: str = Field(min_length=1)
    response: AdvisorDraftResponse
    verification: GroundingVerification
