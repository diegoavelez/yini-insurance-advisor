"""Offline PDF ingestion contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

IngestionStatus = Literal["succeeded", "failed", "skipped"]


class ProcessedDocument(BaseModel):
    """Metadata contract for one ingestion attempt."""

    source_pdf_id: str = Field(min_length=1)
    source_pdf_path: str = Field(min_length=1)
    source_pdf_relative_path: str = Field(min_length=1)
    markdown_output_path: str = Field(min_length=1)
    cleaned_markdown_output_path: str = Field(min_length=1)
    processed_output_path: str = Field(min_length=1)
    document_name: str = Field(min_length=1)
    document_version: str | None = None
    ingestion_status: IngestionStatus
    error_message: str | None = None
    ingested_at: datetime

    @model_validator(mode="after")
    def validate_failed_records(self) -> ProcessedDocument:
        if self.ingestion_status == "failed" and not self.error_message:
            raise ValueError("failed ingestion records must include error_message")
        return self
