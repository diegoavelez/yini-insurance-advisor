from __future__ import annotations

from collections.abc import Callable, Sequence
from pathlib import Path

from contracts import (
    ChunkBundle,
    ChunkRecord,
    EmbeddingBundle,
    EmbeddingRecord,
    ProcessedDocument,
    VectorPayload,
)
from rag.local_hybrid_recall import deduplicate_exact_pv_applicability_chunks
from rag.markdown_chunk_normalization import (
    MarkdownBlock,
    ensure_chunk_text_includes_section_context,
    expand_large_blocks,
    group_semantic_blocks,
    markdown_has_non_heading_content,
    should_disable_chunk_overlap_for_entries,
    split_markdown_blocks,
)


def build_chunk_records(
    *,
    source_pdf_id: str,
    document_name: str,
    document_version: str | None,
    document_type: str | None = None,
    product: str | None = None,
    source_pdf_path: Path,
    source_pdf_relative_path: Path,
    cleaned_markdown_output_path: Path,
    cleaned_markdown_text: str,
    chunk_size: int,
    chunk_overlap: int,
    chunk_schema_version: str,
) -> list[ChunkRecord]:
    """Build deterministic chunk records from cleaned markdown text."""

    blocks = expand_large_blocks(
        group_semantic_blocks(split_markdown_blocks(cleaned_markdown_text), chunk_size),
        chunk_size,
    )
    if not blocks:
        raise RuntimeError("No cleaned markdown blocks were available for chunk generation.")

    chunk_records: list[ChunkRecord] = []
    start_index = 0
    chunk_index = 0

    def render_effective_chunk_text(
        entries: Sequence[MarkdownBlock],
    ) -> tuple[str, list[str], str | None]:
        chunk_text = "\n\n".join(entry.text for entry in entries)
        chunk_section = next(
            (entry.section for entry in reversed(entries) if entry.section),
            None,
        )
        chunk_section_path = next(
            (list(entry.section_path) for entry in reversed(entries) if entry.section_path),
            [],
        )
        return (
            ensure_chunk_text_includes_section_context(
                chunk_text=chunk_text,
                section_path=chunk_section_path,
            ),
            chunk_section_path,
            chunk_section,
        )

    normalized_blocks: list[MarkdownBlock] = []
    for block in blocks:
        effective_block_text, _effective_section_path, _effective_section = (
            render_effective_chunk_text([block])
        )
        if len(effective_block_text) <= chunk_size or "\n\n" not in block.text:
            normalized_blocks.append(block)
            continue

        paragraph_units = [unit.strip() for unit in block.text.split("\n\n") if unit.strip()]
        if len(paragraph_units) <= 1:
            normalized_blocks.append(block)
            continue

        current_units: list[str] = []
        for unit in paragraph_units:
            candidate_units = [*current_units, unit]
            candidate_block = MarkdownBlock(
                text="\n\n".join(candidate_units),
                section=block.section,
                section_path=block.section_path,
                kind=block.kind,
            )
            candidate_text, _candidate_section_path, _candidate_section = (
                render_effective_chunk_text([candidate_block])
            )
            if current_units and len(candidate_text) > chunk_size:
                normalized_blocks.append(
                    MarkdownBlock(
                        text="\n\n".join(current_units),
                        section=block.section,
                        section_path=block.section_path,
                        kind=block.kind,
                    )
                )
                current_units = [unit]
                continue
            current_units = candidate_units

        if current_units:
            normalized_blocks.append(
                MarkdownBlock(
                    text="\n\n".join(current_units),
                    section=block.section,
                    section_path=block.section_path,
                    kind=block.kind,
                )
            )

    blocks = normalized_blocks

    while start_index < len(blocks):
        current_entries: list[MarkdownBlock] = []
        end_index = start_index

        while end_index < len(blocks):
            block = blocks[end_index]
            if current_entries and block.section_path != current_entries[-1].section_path:
                break
            candidate_entries = [*current_entries, block]
            candidate_text, _candidate_section_path, _candidate_section = (
                render_effective_chunk_text(candidate_entries)
            )
            if current_entries and len(candidate_text) > chunk_size:
                break
            current_entries = candidate_entries
            end_index += 1

        chunk_text, chunk_section_path, chunk_section = render_effective_chunk_text(current_entries)
        chunk_has_non_heading_content = markdown_has_non_heading_content(chunk_text)
        should_emit_heading_only_chunk = (
            not chunk_has_non_heading_content
            and bool(chunk_text.strip())
            and len(current_entries) == 1
            and current_entries[0].kind == "heading"
        )
        if not chunk_has_non_heading_content and not should_emit_heading_only_chunk:
            if end_index >= len(blocks):
                break
        else:
            chunk_records.append(
                ChunkRecord(
                    chunk_id=f"{source_pdf_id}:{chunk_schema_version}:{chunk_index:04d}",
                    source_pdf_id=source_pdf_id,
                    document_name=document_name,
                    document_version=document_version,
                    document_type=document_type,
                    product=product,
                    source_pdf_path=str(source_pdf_path),
                    source_pdf_relative_path=source_pdf_relative_path.as_posix(),
                    cleaned_markdown_output_path=str(cleaned_markdown_output_path),
                    text=chunk_text,
                    chunk_index=chunk_index,
                    chunk_schema_version=chunk_schema_version,
                    section=chunk_section,
                    section_path=chunk_section_path,
                )
            )
            chunk_index += 1

        if end_index >= len(blocks):
            break

        if should_disable_chunk_overlap_for_entries(current_entries):
            start_index = end_index
            continue

        overlap_block_count = 0
        overlap_length = 0
        cursor = len(current_entries) - 1
        while cursor >= 0 and overlap_length < chunk_overlap:
            overlap_length += len(current_entries[cursor].text)
            overlap_block_count += 1
            cursor -= 1

        next_start_index = end_index - overlap_block_count
        start_index = max(next_start_index, start_index + 1)

    return deduplicate_exact_pv_applicability_chunks(
        chunk_records,
        chunk_schema_version=chunk_schema_version,
    )


def build_chunk_bundle(
    *,
    processed_document: ProcessedDocument,
    chunk_artifact_path: Path,
    cleaned_markdown_text: str,
    chunk_size: int,
    chunk_overlap: int,
    chunk_schema_version: str,
    build_chunk_records_fn: Callable[..., list[ChunkRecord]] = build_chunk_records,
) -> ChunkBundle:
    """Build a deterministic chunk bundle for one processed document."""

    chunk_records = build_chunk_records_fn(
        source_pdf_id=processed_document.source_pdf_id,
        document_name=processed_document.document_name,
        document_version=processed_document.document_version,
        document_type=processed_document.document_type,
        product=processed_document.product,
        source_pdf_path=Path(processed_document.source_pdf_path),
        source_pdf_relative_path=Path(processed_document.source_pdf_relative_path),
        cleaned_markdown_output_path=Path(processed_document.cleaned_markdown_output_path),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        chunk_schema_version=chunk_schema_version,
    )
    return ChunkBundle(
        source_pdf_id=processed_document.source_pdf_id,
        document_name=processed_document.document_name,
        document_version=processed_document.document_version,
        document_type=processed_document.document_type,
        product=processed_document.product,
        source_pdf_path=processed_document.source_pdf_path,
        source_pdf_relative_path=processed_document.source_pdf_relative_path,
        cleaned_markdown_output_path=processed_document.cleaned_markdown_output_path,
        chunk_artifact_path=str(chunk_artifact_path),
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        chunk_schema_version=chunk_schema_version,
        chunks=chunk_records,
    )


def write_chunk_bundle(chunk_bundle: ChunkBundle, chunk_artifact_path: Path) -> None:
    """Persist a deterministic chunk bundle to JSON."""

    chunk_artifact_path.parent.mkdir(parents=True, exist_ok=True)
    chunk_artifact_path.write_text(chunk_bundle.model_dump_json(indent=2), encoding="utf-8")


def build_embedding_payload(chunk_record: ChunkRecord) -> VectorPayload:
    """Build the explicit later-indexing payload from one chunk record."""

    return VectorPayload(
        chunk_id=chunk_record.chunk_id,
        source_pdf_id=chunk_record.source_pdf_id,
        source_pdf_relative_path=chunk_record.source_pdf_relative_path,
        chunk_schema_version=chunk_record.chunk_schema_version,
        chunk_index=chunk_record.chunk_index,
        document_name=chunk_record.document_name,
        document_version=chunk_record.document_version,
        document_type=chunk_record.document_type,
        product=chunk_record.product,
        section=chunk_record.section,
        section_path=chunk_record.section_path,
        text=chunk_record.text,
    )


def build_embedding_bundle(
    *,
    chunk_bundle: ChunkBundle,
    embedding_artifact_path: Path,
    embedding_schema_version: str,
    embedding_provider: str,
    embedding_model: str,
    generate_embedding_vector_fn: Callable[[str], list[float]],
) -> EmbeddingBundle:
    """Build a deterministic embedding bundle from one chunk bundle."""

    embedding_records: list[EmbeddingRecord] = []

    for chunk_record in chunk_bundle.chunks:
        vector = generate_embedding_vector_fn(chunk_record.text)
        embedding_records.append(
            EmbeddingRecord(
                chunk_id=chunk_record.chunk_id,
                source_pdf_id=chunk_record.source_pdf_id,
                chunk_schema_version=chunk_record.chunk_schema_version,
                embedding_provider=embedding_provider,
                embedding_model=embedding_model,
                vector_dimension=len(vector),
                vector=vector,
                payload=build_embedding_payload(chunk_record),
            )
        )

    if not embedding_records:
        raise RuntimeError("No chunk records were available for embedding generation.")

    return EmbeddingBundle(
        source_pdf_id=chunk_bundle.source_pdf_id,
        document_name=chunk_bundle.document_name,
        document_version=chunk_bundle.document_version,
        document_type=chunk_bundle.document_type,
        product=chunk_bundle.product,
        source_chunk_artifact_path=chunk_bundle.chunk_artifact_path,
        embedding_artifact_path=str(embedding_artifact_path),
        embedding_schema_version=embedding_schema_version,
        chunk_schema_version=chunk_bundle.chunk_schema_version,
        embedding_provider=embedding_provider,
        embedding_model=embedding_model,
        vector_dimension=embedding_records[0].vector_dimension,
        embeddings=embedding_records,
    )


def write_embedding_bundle(
    embedding_bundle: EmbeddingBundle,
    embedding_artifact_path: Path,
) -> None:
    """Persist a deterministic embedding bundle to JSON."""

    embedding_artifact_path.parent.mkdir(parents=True, exist_ok=True)
    embedding_artifact_path.write_text(
        embedding_bundle.model_dump_json(indent=2),
        encoding="utf-8",
    )


def load_chunk_bundle(chunk_artifact_path: Path) -> ChunkBundle:
    """Load one persisted chunk bundle."""

    return ChunkBundle.model_validate_json(chunk_artifact_path.read_text(encoding="utf-8"))


def load_embedding_bundle(embedding_artifact_path: Path) -> EmbeddingBundle:
    """Load one persisted embedding bundle."""

    return EmbeddingBundle.model_validate_json(embedding_artifact_path.read_text(encoding="utf-8"))


def existing_ingestion_artifacts_match_resolved_metadata(
    *,
    processed_output_path: Path,
    chunk_artifact_path: Path,
    resolved_document_type: str | None,
    resolved_product: str | None,
    allow_legacy_missing_metadata: bool = False,
) -> bool:
    """Return whether persisted ingestion artifacts still match current metadata."""

    try:
        processed_document = ProcessedDocument.model_validate_json(
            processed_output_path.read_text(encoding="utf-8")
        )
        chunk_bundle = load_chunk_bundle(chunk_artifact_path)
    except Exception:
        return False

    def metadata_matches(existing_value: str | None, resolved_value: str | None) -> bool:
        if existing_value == resolved_value:
            return True
        return allow_legacy_missing_metadata and existing_value is None

    return (
        metadata_matches(processed_document.document_type, resolved_document_type)
        and metadata_matches(processed_document.product, resolved_product)
        and metadata_matches(chunk_bundle.document_type, resolved_document_type)
        and metadata_matches(chunk_bundle.product, resolved_product)
    )


def should_reuse_existing_ingestion_artifacts(
    *,
    overwrite: bool,
    markdown_output_path: Path,
    cleaned_markdown_output_path: Path,
    processed_output_path: Path,
    chunk_artifact_path: Path,
    resolved_document_type: str | None,
    resolved_product: str | None,
    metadata_refresh_requested: bool,
) -> bool:
    """Return whether one source PDF can reuse existing ingestion artifacts."""

    return (
        not overwrite
        and markdown_output_path.exists()
        and cleaned_markdown_output_path.exists()
        and processed_output_path.exists()
        and chunk_artifact_path.exists()
        and existing_ingestion_artifacts_match_resolved_metadata(
            processed_output_path=processed_output_path,
            chunk_artifact_path=chunk_artifact_path,
            resolved_document_type=resolved_document_type,
            resolved_product=resolved_product,
            allow_legacy_missing_metadata=not metadata_refresh_requested,
        )
    )


def existing_embedding_artifact_matches_chunk_bundle(
    *,
    embedding_artifact_path: Path,
    chunk_bundle: ChunkBundle,
) -> bool:
    """Return whether one persisted embedding artifact still matches its chunk bundle."""

    try:
        embedding_bundle = load_embedding_bundle(embedding_artifact_path)
    except Exception:
        return False

    if (
        embedding_bundle.document_name != chunk_bundle.document_name
        or embedding_bundle.document_version != chunk_bundle.document_version
        or embedding_bundle.document_type != chunk_bundle.document_type
        or embedding_bundle.product != chunk_bundle.product
        or embedding_bundle.chunk_schema_version != chunk_bundle.chunk_schema_version
    ):
        return False

    expected_chunk_ids = [chunk.chunk_id for chunk in chunk_bundle.chunks]
    actual_chunk_ids = [record.chunk_id for record in embedding_bundle.embeddings]
    if actual_chunk_ids != expected_chunk_ids:
        return False

    actual_payload_metadata = [
        (
            record.payload.document_name,
            record.payload.document_version,
            record.payload.document_type,
            record.payload.product,
        )
        for record in embedding_bundle.embeddings
    ]
    expected_payload_metadata = [
        (
            chunk.document_name,
            chunk.document_version,
            chunk.document_type,
            chunk.product,
        )
        for chunk in chunk_bundle.chunks
    ]
    return actual_payload_metadata == expected_payload_metadata


def should_reuse_existing_embedding_artifact(
    *,
    overwrite: bool,
    embedding_artifact_path: Path,
    chunk_bundle: ChunkBundle,
) -> bool:
    """Return whether one chunk bundle can reuse its persisted embedding artifact."""

    return (
        not overwrite
        and embedding_artifact_path.exists()
        and existing_embedding_artifact_matches_chunk_bundle(
            embedding_artifact_path=embedding_artifact_path,
            chunk_bundle=chunk_bundle,
        )
    )
