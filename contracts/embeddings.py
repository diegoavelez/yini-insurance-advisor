"""Embedding artifact contracts for offline vector preparation."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

EmbeddingGenerationStatus = Literal["succeeded", "failed", "skipped"]
EmbeddingIndexingStatus = Literal["succeeded", "failed"]


class VectorPayload(BaseModel):
    """Traceable payload shape for later vector-store indexing."""

    chunk_id: str = Field(min_length=1)
    source_pdf_id: str = Field(min_length=1)
    source_pdf_relative_path: str = Field(min_length=1)
    chunk_schema_version: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    document_type: str | None = None
    product: str | None = None
    section: str | None = None
    section_path: list[str] = Field(default_factory=list)
    text: str = Field(min_length=1)


class EmbeddingRecord(BaseModel):
    """One typed persisted embedding for a chunk record."""

    chunk_id: str = Field(min_length=1)
    source_pdf_id: str = Field(min_length=1)
    chunk_schema_version: str = Field(min_length=1)
    embedding_provider: str = Field(min_length=1)
    embedding_model: str = Field(min_length=1)
    vector_dimension: int = Field(ge=1)
    vector: list[float] = Field(min_length=1)
    payload: VectorPayload

    @model_validator(mode="after")
    def validate_vector_dimension(self) -> EmbeddingRecord:
        if len(self.vector) != self.vector_dimension:
            raise ValueError("vector_dimension must match the vector length")
        return self


class EmbeddingBundle(BaseModel):
    """A deterministic persisted embedding bundle for one chunk artifact."""

    source_pdf_id: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    document_type: str | None = None
    product: str | None = None
    source_chunk_artifact_path: str = Field(min_length=1)
    embedding_artifact_path: str = Field(min_length=1)
    embedding_schema_version: str = Field(min_length=1)
    chunk_schema_version: str = Field(min_length=1)
    embedding_provider: str = Field(min_length=1)
    embedding_model: str = Field(min_length=1)
    vector_dimension: int = Field(ge=1)
    embeddings: list[EmbeddingRecord] = Field(default_factory=list)


class EmbeddingGenerationRecord(BaseModel):
    """Manifest record for one embedding generation attempt."""

    source_pdf_id: str = Field(min_length=1)
    source_chunk_artifact_path: str = Field(min_length=1)
    embedding_artifact_path: str = Field(min_length=1)
    embedding_provider: str = Field(min_length=1)
    embedding_model: str = Field(min_length=1)
    generation_status: EmbeddingGenerationStatus
    error_message: str | None = None
    generated_at: datetime

    @model_validator(mode="after")
    def validate_failed_records(self) -> EmbeddingGenerationRecord:
        if self.generation_status == "failed" and not self.error_message:
            raise ValueError("failed embedding records must include error_message")
        return self


class EmbeddingIndexingRecord(BaseModel):
    """Manifest record for one Qdrant indexing attempt."""

    source_pdf_id: str = Field(min_length=1)
    embedding_artifact_path: str = Field(min_length=1)
    qdrant_collection: str = Field(min_length=1)
    indexed_point_count: int = Field(ge=0)
    indexing_status: EmbeddingIndexingStatus
    error_message: str | None = None
    indexed_at: datetime

    @model_validator(mode="after")
    def validate_failed_records(self) -> EmbeddingIndexingRecord:
        if self.indexing_status == "failed" and not self.error_message:
            raise ValueError("failed indexing records must include error_message")
        return self
