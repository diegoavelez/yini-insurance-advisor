from __future__ import annotations

from pathlib import Path

from contracts import DocumentMetadataOverlayEntry, TermEquivalenceSet
from rag.document_canonicalization import (
    build_ingestion_artifact_paths,
    derive_source_pdf_id,
    extract_document_metadata,
    resolve_document_product,
    resolve_document_type,
)


def test_extract_document_metadata_uses_heading_and_version_when_available() -> None:
    document_name, document_version = extract_document_metadata(
        Path("policy-a.pdf"),
        "# Policy A\n\nVersión 2026-01\n\nContenido.",
    )

    assert document_name == "Policy A"
    assert document_version == "2026-01"


def test_extract_document_metadata_rejects_noisy_media_heading() -> None:
    document_name, document_version = extract_document_metadata(
        Path("registro unico.pdf"),
        "# Grabación: https://example.com/video\n\n# Registro único de intermediación\n",
    )

    assert document_name == "Registro único de intermediación"
    assert document_version is None


def test_derive_source_pdf_id_is_collision_safe_for_nested_paths() -> None:
    input_dir = Path("data/raw")

    first = derive_source_pdf_id(
        input_dir=input_dir,
        source_pdf_path=input_dir / "MOVILIDAD" / "AUTOS" / "diferenciales planes autos.pdf",
    )
    second = derive_source_pdf_id(
        input_dir=input_dir,
        source_pdf_path=input_dir / "MOVILIDAD" / "MOTOS" / "diferenciales planes autos.pdf",
    )

    assert first == "movilidad__autos__diferenciales-planes-autos"
    assert second == "movilidad__motos__diferenciales-planes-autos"
    assert first != second


def test_resolve_document_metadata_prefers_overlay_then_path_inference() -> None:
    term_equivalences = TermEquivalenceSet(
        filter_aliases={
            "product": {
                "auto": ["autos"],
            },
            "document_type": {
                "guide": ["ayudaventas"],
            },
        }
    )
    relative_path = Path("MOVILIDAD/AUTOS/ayudaventas autos v2.pdf")

    assert (
        resolve_document_product(
            source_pdf_relative_path=relative_path,
            overlay_entry=None,
            term_equivalences=term_equivalences,
        )
        == "auto"
    )
    assert (
        resolve_document_type(
            source_pdf_relative_path=relative_path,
            overlay_entry=None,
            term_equivalences=term_equivalences,
        )
        == "guide"
    )

    overlay = DocumentMetadataOverlayEntry(product="arl", document_type="policy")
    assert (
        resolve_document_product(
            source_pdf_relative_path=relative_path,
            overlay_entry=overlay,
            term_equivalences=term_equivalences,
        )
        == "arl"
    )
    assert (
        resolve_document_type(
            source_pdf_relative_path=relative_path,
            overlay_entry=overlay,
            term_equivalences=term_equivalences,
        )
        == "policy"
    )


def test_build_ingestion_artifact_paths_use_source_pdf_id() -> None:
    markdown_output, cleaned_output, processed_output, chunk_output = (
        build_ingestion_artifact_paths(
            source_pdf_id="arl__policy-a",
            markdown_dir=Path("data/markdown"),
            processed_dir=Path("data/processed"),
        )
    )

    assert markdown_output == Path("data/markdown/arl__policy-a.md")
    assert cleaned_output == Path("data/processed/arl__policy-a.cleaned.md")
    assert processed_output == Path("data/processed/arl__policy-a.json")
    assert chunk_output == Path("data/processed/chunks/arl__policy-a.chunks.json")
