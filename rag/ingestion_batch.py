from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from contracts import (
    EmbeddingBundle,
    EmbeddingGenerationRecord,
    EmbeddingIndexingRecord,
    ProcessedDocument,
)
from core.config import Settings


def append_manifest_record(manifest_path: Path, record: ProcessedDocument) -> None:
    """Append one JSONL manifest record."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as manifest_file:
        manifest_file.write(record.model_dump_json())
        manifest_file.write("\n")


def build_embedding_generation_record(
    *,
    chunk_bundle,
    embedding_artifact_path: Path,
    settings: Settings,
    generation_status: str,
    error_message: str | None = None,
) -> EmbeddingGenerationRecord:
    """Build one manifest record for embedding generation."""

    return EmbeddingGenerationRecord(
        source_pdf_id=chunk_bundle.source_pdf_id,
        source_chunk_artifact_path=chunk_bundle.chunk_artifact_path,
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        generation_status=generation_status,
        error_message=error_message,
        generated_at=datetime.now(UTC),
    )


def build_failed_embedding_record_from_artifact_path(
    *,
    chunk_artifact_path: Path,
    embedding_artifact_path: Path,
    settings: Settings,
    error_message: str,
) -> EmbeddingGenerationRecord:
    """Build a failed embedding manifest record without a valid chunk bundle."""

    source_pdf_id = chunk_artifact_path.name.removesuffix(".chunks.json")
    return EmbeddingGenerationRecord(
        source_pdf_id=source_pdf_id,
        source_chunk_artifact_path=str(chunk_artifact_path),
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_provider=settings.embedding_provider,
        embedding_model=settings.embedding_model,
        generation_status="failed",
        error_message=error_message,
        generated_at=datetime.now(UTC),
    )


def append_embedding_manifest_record(
    manifest_path: Path,
    record: EmbeddingGenerationRecord,
) -> None:
    """Append one JSONL embedding manifest record."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as manifest_file:
        manifest_file.write(record.model_dump_json())
        manifest_file.write("\n")


def append_indexing_manifest_record(
    manifest_path: Path,
    record: EmbeddingIndexingRecord,
) -> None:
    """Append one JSONL indexing manifest record."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("a", encoding="utf-8") as manifest_file:
        manifest_file.write(record.model_dump_json())
        manifest_file.write("\n")


def build_indexing_record(
    *,
    embedding_bundle: EmbeddingBundle,
    settings: Settings,
    indexing_status: str,
    indexed_point_count: int,
    error_message: str | None = None,
) -> EmbeddingIndexingRecord:
    """Build one indexing manifest record."""

    return EmbeddingIndexingRecord(
        source_pdf_id=embedding_bundle.source_pdf_id,
        embedding_artifact_path=embedding_bundle.embedding_artifact_path,
        qdrant_collection=settings.qdrant_collection,
        indexed_point_count=indexed_point_count,
        indexing_status=indexing_status,
        error_message=error_message,
        indexed_at=datetime.now(UTC),
    )


def build_failed_indexing_record_from_artifact_path(
    *,
    embedding_artifact_path: Path,
    settings: Settings,
    error_message: str,
) -> EmbeddingIndexingRecord:
    """Build a failed indexing record without a valid embedding bundle."""

    source_pdf_id = embedding_artifact_path.name.removesuffix(".embeddings.json")
    return EmbeddingIndexingRecord(
        source_pdf_id=source_pdf_id,
        embedding_artifact_path=str(embedding_artifact_path),
        qdrant_collection=settings.qdrant_collection,
        indexed_point_count=0,
        indexing_status="failed",
        error_message=error_message,
        indexed_at=datetime.now(UTC),
    )


def iter_source_pdfs(input_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching PDF files under the configured input directory."""

    return sorted(path for path in input_dir.rglob(glob_pattern) if path.is_file())


def iter_chunk_artifacts(chunk_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching chunk artifacts under the configured directory."""

    return sorted(path for path in chunk_dir.glob(glob_pattern) if path.is_file())


def iter_embedding_artifacts(embedding_dir: Path, glob_pattern: str) -> list[Path]:
    """Return sorted matching embedding artifacts under the configured directory."""

    return sorted(path for path in embedding_dir.glob(glob_pattern) if path.is_file())
