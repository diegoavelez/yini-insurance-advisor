from __future__ import annotations

import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TypeVar

from contracts import (
    EmbeddingGenerationRecord,
    EmbeddingIndexingRecord,
    ProcessedDocument,
)

ItemT = TypeVar("ItemT")
RecordT = TypeVar("RecordT")


def execute_batch_operation(
    *,
    items: Sequence[ItemT],
    process_item_fn: Callable[[ItemT], RecordT],
    recover_failure_record_fn: Callable[[ItemT, Exception], RecordT],
    append_record_fn: Callable[[RecordT], None],
    is_failure_record_fn: Callable[[RecordT], bool],
    format_failure_message_fn: Callable[[ItemT, RecordT], str],
    fail_fast: bool,
) -> int:
    """Execute one batch operation with per-item recovery and manifest append semantics."""

    for item in items:
        try:
            record = process_item_fn(item)
        except Exception as exc:
            record = recover_failure_record_fn(item, exc)

        append_record_fn(record)

        if is_failure_record_fn(record):
            print(format_failure_message_fn(item, record), file=sys.stderr)
            if fail_fast:
                return 1

    return 0


def recover_failed_ingestion_record(
    *,
    source_pdf_path: Path,
    input_dir: Path,
    markdown_dir: Path,
    processed_dir: Path,
    metadata_overlays: dict | None,
    term_equivalences,
    error: Exception,
    derive_source_pdf_id_fn: Callable[..., str],
    build_ingestion_artifact_paths_fn: Callable[..., tuple[Path, Path, Path, Path]],
    resolve_document_type_fn: Callable[..., str | None],
    resolve_document_product_fn: Callable[..., str | None],
    remove_artifact_if_exists_fn: Callable[[Path], None],
    build_processed_document_fn: Callable[..., ProcessedDocument],
) -> ProcessedDocument:
    """Build the deterministic failed ingestion record for one source PDF."""

    source_pdf_relative_path = source_pdf_path.relative_to(input_dir)
    source_pdf_id = derive_source_pdf_id_fn(
        input_dir=input_dir,
        source_pdf_path=source_pdf_path,
    )
    (
        markdown_output_path,
        cleaned_markdown_output_path,
        processed_output_path,
        chunk_artifact_path,
    ) = build_ingestion_artifact_paths_fn(
        source_pdf_id=source_pdf_id,
        markdown_dir=markdown_dir,
        processed_dir=processed_dir,
    )
    overlay_entry = (metadata_overlays or {}).get(source_pdf_id)
    resolved_document_type = resolve_document_type_fn(
        source_pdf_relative_path=source_pdf_relative_path,
        overlay_entry=overlay_entry,
        term_equivalences=term_equivalences,
    )
    resolved_product = resolve_document_product_fn(
        source_pdf_relative_path=source_pdf_relative_path,
        overlay_entry=overlay_entry,
        term_equivalences=term_equivalences,
    )
    remove_artifact_if_exists_fn(cleaned_markdown_output_path)
    remove_artifact_if_exists_fn(processed_output_path)
    remove_artifact_if_exists_fn(chunk_artifact_path)
    return build_processed_document_fn(
        source_pdf_id=source_pdf_id,
        source_pdf_path=source_pdf_path,
        source_pdf_relative_path=source_pdf_relative_path,
        markdown_output_path=markdown_output_path,
        cleaned_markdown_output_path=cleaned_markdown_output_path,
        processed_output_path=processed_output_path,
        ingestion_status="failed",
        document_type=resolved_document_type,
        product=resolved_product,
        error_message=str(error),
    )


def recover_failed_embedding_generation_record(
    *,
    chunk_artifact_path: Path,
    embedding_dir: Path,
    settings,
    error: Exception,
    load_chunk_bundle_fn: Callable[[Path], object],
    remove_artifact_if_exists_fn: Callable[[Path], None],
    build_embedding_generation_record_fn: Callable[..., EmbeddingGenerationRecord],
    build_failed_embedding_record_from_artifact_path_fn: Callable[
        ..., EmbeddingGenerationRecord
    ],
) -> EmbeddingGenerationRecord:
    """Build the deterministic failed embedding-generation record for one artifact."""

    embedding_artifact_path = embedding_dir / (
        f"{chunk_artifact_path.name.removesuffix('.chunks.json')}.embeddings.json"
    )
    try:
        chunk_bundle = load_chunk_bundle_fn(chunk_artifact_path)
        embedding_artifact_path = embedding_dir / f"{chunk_bundle.source_pdf_id}.embeddings.json"
        remove_artifact_if_exists_fn(embedding_artifact_path)
        return build_embedding_generation_record_fn(
            chunk_bundle=chunk_bundle,
            embedding_artifact_path=embedding_artifact_path,
            settings=settings,
            generation_status="failed",
            error_message=str(error),
        )
    except Exception as load_exc:
        remove_artifact_if_exists_fn(embedding_artifact_path)
        return build_failed_embedding_record_from_artifact_path_fn(
            chunk_artifact_path=chunk_artifact_path,
            embedding_artifact_path=embedding_artifact_path,
            settings=settings,
            error_message=f"{error}; chunk artifact load failed: {load_exc}",
        )


def recover_failed_indexing_record(
    *,
    embedding_artifact_path: Path,
    settings,
    error: Exception,
    load_embedding_bundle_fn: Callable[[Path], object],
    build_indexing_record_fn: Callable[..., EmbeddingIndexingRecord],
    build_failed_indexing_record_from_artifact_path_fn: Callable[
        ..., EmbeddingIndexingRecord
    ],
) -> EmbeddingIndexingRecord:
    """Build the deterministic failed indexing record for one artifact."""

    try:
        embedding_bundle = load_embedding_bundle_fn(embedding_artifact_path)
        return build_indexing_record_fn(
            embedding_bundle=embedding_bundle,
            settings=settings,
            indexing_status="failed",
            indexed_point_count=0,
            error_message=str(error),
        )
    except Exception as load_exc:
        return build_failed_indexing_record_from_artifact_path_fn(
            embedding_artifact_path=embedding_artifact_path,
            settings=settings,
            error_message=f"{error}; embedding artifact load failed: {load_exc}",
        )
