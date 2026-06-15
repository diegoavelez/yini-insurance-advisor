"""Document identity and metadata canonicalization helpers."""

from __future__ import annotations

import re
import unicodedata
from datetime import UTC, datetime
from pathlib import Path

from contracts import DocumentMetadataOverlayEntry, ProcessedDocument, TermEquivalenceSet
from rag.term_equivalences import (
    normalize_equivalence_text,
    query_contains_equivalent_phrase,
    tokenize_lexical_surface,
)

VERSION_PATTERN = re.compile(r"(?i)\b(?:version|versión)\b[:\s-]*([A-Za-z0-9][A-Za-z0-9._/-]*)")


def extract_document_metadata(
    source_pdf_path: Path,
    cleaned_markdown_text: str,
) -> tuple[str, str | None]:
    """Extract low-risk document metadata or return deterministic fallbacks."""

    document_name = source_pdf_path.stem
    document_version = None

    heading_candidates: list[str] = []
    for line in cleaned_markdown_text.splitlines()[:40]:
        stripped_line = line.strip()
        if not stripped_line.startswith("#"):
            continue
        heading_text = stripped_line.lstrip("#").strip()
        if is_safe_document_name_heading(heading_text):
            heading_candidates.append(heading_text)

    if heading_candidates:
        document_name = select_best_document_name_heading(
            source_pdf_path=source_pdf_path,
            heading_candidates=heading_candidates,
        )

    version_match = VERSION_PATTERN.search("\n".join(cleaned_markdown_text.splitlines()[:40]))
    if version_match:
        document_version = version_match.group(1)

    return document_name, document_version


def is_safe_document_name_heading(heading_text: str) -> bool:
    """Return whether a heading is safe to promote as document_name."""

    normalized_heading = heading_text.strip()
    if not normalized_heading:
        return False

    normalized_lower = normalized_heading.casefold()
    noisy_prefixes = (
        "grabación:",
        "grabacion:",
        "video:",
        "vídeo:",
        "estas recomendaciones",
        "asegurate de vivir",
        "asegúrate de vivir",
    )
    if normalized_lower.startswith(noisy_prefixes):
        return False

    if (
        "http://" in normalized_lower
        or "https://" in normalized_lower
        or "www." in normalized_lower
    ):
        return False

    return True


def select_best_document_name_heading(
    *,
    source_pdf_path: Path,
    heading_candidates: list[str] | tuple[str, ...],
) -> str:
    """Select the safest heading candidate using conservative filename overlap."""

    source_tokens = set(tokenize_lexical_surface(source_pdf_path.stem))

    def score_heading(heading_text: str) -> tuple[int, int, int]:
        heading_tokens = set(tokenize_lexical_surface(heading_text))
        overlap = len(source_tokens & heading_tokens)
        question_bonus = 1 if "?" in heading_text or "¿" in heading_text else 0
        brevity_bonus = 1 if len(heading_text) <= 60 else 0
        return (overlap, question_bonus, brevity_bonus)

    return max(heading_candidates, key=score_heading)


def infer_canonical_product_from_relative_path(
    source_pdf_relative_path: str,
    *,
    term_equivalences: TermEquivalenceSet,
) -> str | None:
    """Infer one canonical product from source-relative path segments."""

    path_segments = [
        normalize_equivalence_text(segment)
        for segment in Path(source_pdf_relative_path).parts
        if segment.strip()
    ]
    if not path_segments:
        return None

    product_aliases = term_equivalences.filter_aliases.get("product", {})
    for canonical_product, aliases in product_aliases.items():
        candidate_values = {
            normalize_equivalence_text(canonical_product),
            *(normalize_equivalence_text(alias) for alias in aliases),
        }
        if any(segment in candidate_values for segment in path_segments):
            return canonical_product
        if canonical_product == "auto" and "autos" in path_segments:
            return canonical_product
    return None


def infer_canonical_document_type_from_relative_path(
    source_pdf_relative_path: str,
    *,
    term_equivalences: TermEquivalenceSet,
) -> str | None:
    """Infer one canonical document type from source-relative path tokens."""

    normalized_path = normalize_equivalence_text(source_pdf_relative_path)
    path_tokens = tokenize_lexical_surface(normalized_path)
    if not normalized_path:
        return None

    document_type_aliases = term_equivalences.filter_aliases.get("document_type", {})
    for canonical_document_type, aliases in document_type_aliases.items():
        candidate_values = (
            canonical_document_type,
            *aliases,
        )
        for candidate_value in candidate_values:
            if query_contains_equivalent_phrase(normalized_path, candidate_value):
                return canonical_document_type
            candidate_tokens = tokenize_lexical_surface(candidate_value)
            if candidate_tokens and candidate_tokens.issubset(path_tokens):
                return canonical_document_type
    return None


def resolve_document_product(
    *,
    source_pdf_relative_path: Path,
    overlay_entry: DocumentMetadataOverlayEntry | None,
    term_equivalences: TermEquivalenceSet,
) -> str | None:
    """Resolve persisted product metadata with overlay precedence."""

    if overlay_entry is not None and overlay_entry.product is not None:
        return overlay_entry.product
    return infer_canonical_product_from_relative_path(
        source_pdf_relative_path.as_posix(),
        term_equivalences=term_equivalences,
    )


def resolve_document_type(
    *,
    source_pdf_relative_path: Path,
    overlay_entry: DocumentMetadataOverlayEntry | None,
    term_equivalences: TermEquivalenceSet,
) -> str | None:
    """Resolve persisted document type metadata with overlay precedence."""

    if overlay_entry is not None and overlay_entry.document_type is not None:
        return overlay_entry.document_type
    return infer_canonical_document_type_from_relative_path(
        source_pdf_relative_path.as_posix(),
        term_equivalences=term_equivalences,
    )


def build_processed_document(
    *,
    source_pdf_id: str,
    source_pdf_path: Path,
    source_pdf_relative_path: Path,
    markdown_output_path: Path,
    cleaned_markdown_output_path: Path,
    processed_output_path: Path,
    ingestion_status: str,
    document_name: str | None = None,
    document_version: str | None = None,
    document_type: str | None = None,
    product: str | None = None,
    error_message: str | None = None,
) -> ProcessedDocument:
    """Build one deterministic processed-document record."""

    return ProcessedDocument(
        source_pdf_id=source_pdf_id,
        source_pdf_path=str(source_pdf_path),
        source_pdf_relative_path=source_pdf_relative_path.as_posix(),
        markdown_output_path=str(markdown_output_path),
        cleaned_markdown_output_path=str(cleaned_markdown_output_path),
        processed_output_path=str(processed_output_path),
        document_name=document_name or source_pdf_id,
        document_version=document_version,
        document_type=document_type,
        product=product,
        ingestion_status=ingestion_status,
        error_message=error_message,
        ingested_at=datetime.now(UTC),
    )


def slugify_path_component(value: str) -> str:
    """Return a deterministic ASCII slug for one source-path component."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug or "document"


def derive_source_pdf_id(*, input_dir: Path, source_pdf_path: Path) -> str:
    """Derive a collision-safe document id from the relative source path."""

    relative_path = source_pdf_path.relative_to(input_dir)
    components = [*relative_path.parts[:-1], relative_path.stem]
    return "__".join(slugify_path_component(component) for component in components)


def build_ingestion_artifact_paths(
    *,
    source_pdf_id: str,
    markdown_dir: Path,
    processed_dir: Path,
) -> tuple[Path, Path, Path, Path]:
    """Build deterministic artifact paths for one source document id."""

    markdown_output_path = markdown_dir / f"{source_pdf_id}.md"
    cleaned_markdown_output_path = processed_dir / f"{source_pdf_id}.cleaned.md"
    processed_output_path = processed_dir / f"{source_pdf_id}.json"
    chunk_artifact_path = processed_dir / "chunks" / f"{source_pdf_id}.chunks.json"
    return (
        markdown_output_path,
        cleaned_markdown_output_path,
        processed_output_path,
        chunk_artifact_path,
    )
