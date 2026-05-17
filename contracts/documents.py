"""Document and retrieval domain contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from contracts.responses import Citation

ClauseCategory = Literal[
    "coverage",
    "exclusion",
    "restriction",
    "requirement",
    "procedure",
    "exception",
]


class RetrievedChunk(BaseModel):
    """A retrieval result item with traceable source metadata."""

    chunk_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    clause_id: str | None = None
    score: float


class Clause(BaseModel):
    """A structured clause extracted from retrieved evidence."""

    category: ClauseCategory
    summary: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    clause_id: str | None = None
    supporting_chunk_ids: list[str] = Field(default_factory=list)


class ComparisonItem(BaseModel):
    """One comparison point across documents or clauses."""

    criterion: str = Field(min_length=1)
    finding: str = Field(min_length=1)
    source_documents: list[str] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    sufficient_information: bool = True
