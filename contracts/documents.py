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
    source_pdf_id: str | None = None
    chunk_schema_version: str | None = None
    chunk_index: int | None = Field(default=None, ge=0)
    text: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    page: int | None = Field(default=None, ge=1)
    section: str | None = None
    section_path: list[str] = Field(default_factory=list)
    clause_id: str | None = None
    score: float


class ChunkRecord(BaseModel):
    """A deterministic persisted chunk record for cleaned document text."""

    chunk_id: str = Field(min_length=1)
    source_pdf_id: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    source_pdf_path: str = Field(min_length=1)
    source_pdf_relative_path: str = Field(min_length=1)
    cleaned_markdown_output_path: str = Field(min_length=1)
    text: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    chunk_schema_version: str = Field(default="v2", min_length=1)
    section: str | None = None
    section_path: list[str] = Field(default_factory=list)


class ChunkBundle(BaseModel):
    """A deterministic persisted bundle of chunk records for one document."""

    source_pdf_id: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    source_pdf_path: str = Field(min_length=1)
    source_pdf_relative_path: str = Field(min_length=1)
    cleaned_markdown_output_path: str = Field(min_length=1)
    chunk_artifact_path: str = Field(min_length=1)
    chunk_size: int = Field(ge=1)
    chunk_overlap: int = Field(ge=0)
    chunk_schema_version: str = Field(default="v2", min_length=1)
    chunks: list[ChunkRecord] = Field(default_factory=list)


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
