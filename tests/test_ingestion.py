from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from contracts import ChunkBundle, ProcessedDocument
from rag.ingestion import (
    build_chunk_records,
    build_parser,
    clean_markdown,
    docling_is_available,
    extract_document_metadata,
    main,
    parse_bool,
)


def test_parse_bool_accepts_true_and_false() -> None:
    assert parse_bool("true") is True
    assert parse_bool("false") is False


def test_parse_bool_rejects_invalid_values() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        parse_bool("yes")


def test_parser_builds_canonical_ingest_command() -> None:
    args = build_parser().parse_args(
        [
            "ingest-pdfs",
            "--input-dir",
            "data/raw",
            "--markdown-dir",
            "data/markdown",
            "--processed-dir",
            "data/processed",
            "--manifest-path",
            "data/processed/ingestion-manifest.jsonl",
            "--overwrite",
            "true",
        ]
    )

    assert args.command == "ingest-pdfs"
    assert args.chunk_size == 1200
    assert args.chunk_overlap == 200
    assert args.glob == "*.pdf"
    assert args.overwrite is True
    assert args.fail_fast is False


@pytest.mark.parametrize(
    ("flag", "value"),
    [
        ("--chunk-size", "0"),
        ("--chunk-overlap", "-1"),
    ],
)
def test_parser_rejects_invalid_chunk_configuration(flag: str, value: str) -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(
            [
                "ingest-pdfs",
                "--input-dir",
                "data/raw",
                "--markdown-dir",
                "data/markdown",
                "--processed-dir",
                "data/processed",
                "--manifest-path",
                "data/processed/ingestion-manifest.jsonl",
                flag,
                value,
            ]
        )


def test_parser_accepts_chunk_configuration_overrides() -> None:
    args = build_parser().parse_args(
        [
            "ingest-pdfs",
            "--input-dir",
            "data/raw",
            "--markdown-dir",
            "data/markdown",
            "--processed-dir",
            "data/processed",
            "--manifest-path",
            "data/processed/ingestion-manifest.jsonl",
            "--chunk-size",
            "800",
            "--chunk-overlap",
            "100",
        ]
    )

    assert args.chunk_size == 800
    assert args.chunk_overlap == 100


def test_docling_smoke_check_reflects_importability() -> None:
    assert isinstance(docling_is_available(), bool)


def test_clean_markdown_is_conservative_and_deterministic() -> None:
    dirty_markdown = "# Policy Title\r\n\r\n\r\nClause 1   \r\n[]()\r\n\r\nClause 2\r\n"

    cleaned_markdown = clean_markdown(dirty_markdown)

    assert cleaned_markdown == "# Policy Title\n\nClause 1\n\nClause 2\n"


def test_extract_document_metadata_uses_heading_and_version_when_available() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=Path(".") / "policy-a.pdf",
        cleaned_markdown_text="# Sura Health Policy\nVersion: 2026-01\n\nCoverage text",
    )

    assert document_name == "Sura Health Policy"
    assert document_version == "2026-01"


def test_extract_document_metadata_falls_back_without_heading_or_version() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=Path(".") / "policy-a.pdf",
        cleaned_markdown_text="Coverage text only",
    )

    assert document_name == "policy-a"
    assert document_version is None


def test_build_chunk_records_is_deterministic() -> None:
    cleaned_markdown_text = (
        "# Policy Title\n\n"
        "Paragraph one.\n\n"
        "Paragraph two is slightly longer.\n\n"
        "## Section A\n\n"
        "Paragraph three."
    )

    first_chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=60,
        chunk_overlap=20,
    )
    second_chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=60,
        chunk_overlap=20,
    )

    assert [record.chunk_id for record in first_chunk_records] == [
        record.chunk_id for record in second_chunk_records
    ]
    assert [record.text for record in first_chunk_records] == [
        record.text for record in second_chunk_records
    ]
    assert all(record.chunk_schema_version == "v2" for record in first_chunk_records)


def test_build_chunk_records_keeps_heading_with_following_body_when_it_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n## Coverage\n\nCoverage applies to outpatient care."
        ),
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert "## Coverage\n\nCoverage applies to outpatient care." in chunk_records[0].text
    assert chunk_records[0].section == "Coverage"
    assert chunk_records[0].section_path == ["Policy Title", "Coverage"]


def test_build_chunk_records_keeps_clause_marker_with_following_text_when_it_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text="# Policy Title\n\n1. Coverage\n\nApplies only after deductible.",
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert "1. Coverage\n\nApplies only after deductible." in chunk_records[0].text


def test_build_chunk_records_avoids_tiny_heading_only_chunk_when_next_body_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n## Exclusions\n\nNo coverage applies to cosmetic surgery.\n\n"
            "## Waiting Period\n\nThirty days."
        ),
        chunk_size=120,
        chunk_overlap=20,
    )

    assert all(record.text.strip() != "## Exclusions" for record in chunk_records)
    assert all(record.text.strip() != "## Waiting Period" for record in chunk_records)


def test_build_chunk_records_preserves_clause_split_fallback_for_oversized_content() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text="# Policy Title\n\n1. Coverage\n\n" + ("A" * 160),
        chunk_size=80,
        chunk_overlap=20,
    )

    assert len(chunk_records) >= 2
    assert chunk_records[0].text.startswith("# Policy Title")
    assert any("1. Coverage" in record.text for record in chunk_records)


def test_cli_fails_when_input_directory_is_missing(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(tmp_path / "missing"),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Input directory does not exist" in captured.err


def test_cli_fails_loudly_when_docling_is_unavailable(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: False)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Docling is not installed" in captured.err


def test_cli_fails_when_no_matching_pdfs_are_found(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "No PDF files matched glob" in captured.err


def test_successful_ingestion_writes_deterministic_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown",
        lambda source_pdf_path: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    markdown_output = markdown_dir / "policy-a.md"
    cleaned_markdown_output = processed_dir / "policy-a.cleaned.md"
    processed_output = processed_dir / "policy-a.json"
    chunk_output = processed_dir / "chunks" / "policy-a.chunks.json"
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())
    chunk_bundle = ChunkBundle.model_validate_json(chunk_output.read_text())

    assert exit_code == 0
    assert markdown_output.read_text(encoding="utf-8") == "# Converted policy-a"
    assert cleaned_markdown_output.read_text(encoding="utf-8") == "# Converted policy-a\n"
    assert processed_document.source_pdf_id == "policy-a"
    assert processed_document.markdown_output_path == str(markdown_output)
    assert processed_document.cleaned_markdown_output_path == str(cleaned_markdown_output)
    assert processed_document.processed_output_path == str(processed_output)
    assert processed_document.ingestion_status == "succeeded"
    assert chunk_bundle.chunk_artifact_path == str(chunk_output)
    assert chunk_bundle.chunks
    assert chunk_bundle.chunks[0].source_pdf_id == "policy-a"
    assert chunk_bundle.chunks[0].chunk_id.startswith("policy-a:v2:")
    assert chunk_bundle.chunk_schema_version == "v2"
    assert isinstance(chunk_bundle.chunks[0].section_path, list)
    assert len(manifest_records) == 1


def test_existing_outputs_are_skipped_when_overwrite_is_false(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")
    markdown_dir.mkdir()
    processed_dir.mkdir()
    (markdown_dir / "policy-a.md").write_text("existing markdown", encoding="utf-8")
    existing_record = ProcessedDocument(
        source_pdf_id="policy-a",
        source_pdf_path=str(source_pdf),
        markdown_output_path=str(markdown_dir / "policy-a.md"),
        cleaned_markdown_output_path=str(processed_dir / "policy-a.cleaned.md"),
        processed_output_path=str(processed_dir / "policy-a.json"),
        document_name="policy-a",
        document_version=None,
        ingestion_status="succeeded",
        error_message=None,
        ingested_at="2026-05-18T00:00:00Z",
    )
    (processed_dir / "policy-a.cleaned.md").write_text("existing cleaned", encoding="utf-8")
    (processed_dir / "chunks").mkdir()
    (processed_dir / "chunks" / "policy-a.chunks.json").write_text(
        ChunkBundle(
            source_pdf_id="policy-a",
            document_name="policy-a",
            document_version=None,
            source_pdf_path=str(source_pdf),
            cleaned_markdown_output_path=str(processed_dir / "policy-a.cleaned.md"),
            chunk_artifact_path=str(processed_dir / "chunks" / "policy-a.chunks.json"),
            chunk_size=1200,
            chunk_overlap=200,
            chunks=[],
        ).model_dump_json(indent=2),
        encoding="utf-8",
    )
    (processed_dir / "policy-a.json").write_text(
        existing_record.model_dump_json(indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").read_text(encoding="utf-8") == "existing markdown"
    assert (processed_dir / "policy-a.cleaned.md").read_text(encoding="utf-8") == "existing cleaned"
    assert (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert manifest_record.ingestion_status == "skipped"


def test_overwrite_true_regenerates_outputs(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")
    markdown_dir.mkdir()
    processed_dir.mkdir()
    (markdown_dir / "policy-a.md").write_text("stale markdown", encoding="utf-8")
    (processed_dir / "policy-a.cleaned.md").write_text("stale cleaned", encoding="utf-8")
    (processed_dir / "chunks").mkdir()
    (processed_dir / "chunks" / "policy-a.chunks.json").write_text("{}", encoding="utf-8")
    (processed_dir / "policy-a.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", lambda _: "# Fresh markdown")

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--overwrite",
            "true",
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").read_text(encoding="utf-8") == "# Fresh markdown"
    assert (
        processed_dir / "policy-a.cleaned.md"
    ).read_text(encoding="utf-8") == "# Fresh markdown\n"
    assert (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert manifest_record.ingestion_status == "succeeded"


def test_manifest_is_append_only_across_reruns(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", lambda _: "# First markdown")

    first_exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    second_exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_records = [
        ProcessedDocument.model_validate_json(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]

    assert first_exit_code == 0
    assert second_exit_code == 0
    assert len(manifest_records) == 2
    assert [record.ingestion_status for record in manifest_records] == ["succeeded", "skipped"]


def test_cleaning_failure_records_failed_manifest_and_no_cleaned_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", lambda _: "# Raw markdown")

    def fail_cleaning(_: str) -> str:
        raise RuntimeError("cleaning failed")

    monkeypatch.setattr("rag.ingestion.clean_markdown", fail_cleaning)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "cleaning failed"


def test_chunk_generation_failure_records_failed_manifest_and_no_chunk_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", lambda _: "# Raw markdown")

    def fail_chunk_build(*args, **kwargs):
        raise RuntimeError("chunk generation failed")

    monkeypatch.setattr("rag.ingestion.build_chunk_bundle", fail_chunk_build)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert not (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "chunk generation failed"


def test_refined_chunk_generation_failure_records_failed_manifest_and_no_chunk_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown",
        lambda _: "# Policy Title\n\n## Coverage\n\nCoverage applies.",
    )

    def fail_refined_chunk_generation(*args, **kwargs):
        raise RuntimeError("refined chunk generation failed")

    monkeypatch.setattr("rag.ingestion.build_chunk_records", fail_refined_chunk_generation)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "refined chunk generation failed"


def test_fail_fast_true_stops_after_first_cleaning_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", lambda _: "# Raw markdown")

    def fail_cleaning(_: str) -> str:
        raise RuntimeError("cleaning failed")

    monkeypatch.setattr("rag.ingestion.clean_markdown", fail_cleaning)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
            "--fail-fast",
            "true",
        ]
    )
    captured = capsys.readouterr()
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()

    assert exit_code == 1
    assert "Failed to ingest policy-a.pdf: cleaning failed" in captured.err
    assert len(manifest_records) == 1
    assert ProcessedDocument.model_validate_json(manifest_records[0]).ingestion_status == "failed"


def test_fail_fast_false_records_failures_and_continues(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    def fake_convert(source_pdf_path):
        if source_pdf_path.stem == "policy-a":
            raise RuntimeError("conversion failed")
        return "# Converted"

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", fake_convert)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
        ]
    )
    captured = capsys.readouterr()
    manifest_records = [
        ProcessedDocument.model_validate_json(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]

    assert exit_code == 0
    assert "Failed to ingest policy-a.pdf" in captured.err
    assert [record.ingestion_status for record in manifest_records] == ["failed", "succeeded"]


def test_fail_fast_true_stops_after_first_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    def fake_convert(_):
        raise RuntimeError("conversion failed")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown", fake_convert)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
            "--fail-fast",
            "true",
        ]
    )
    captured = capsys.readouterr()
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()

    assert exit_code == 1
    assert "Failed to ingest policy-a.pdf" in captured.err
    assert len(manifest_records) == 1
    assert ProcessedDocument.model_validate_json(manifest_records[0]).ingestion_status == "failed"


def test_processed_document_requires_error_message_for_failed_status() -> None:
    with pytest.raises(ValueError):
        ProcessedDocument(
            source_pdf_id="policy-a",
            source_pdf_path="data/raw/policy-a.pdf",
            markdown_output_path="data/markdown/policy-a.md",
            cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
            processed_output_path="data/processed/policy-a.json",
            document_name="policy-a",
            document_version=None,
            ingestion_status="failed",
            error_message=None,
            ingested_at="2026-05-18T00:00:00Z",
        )


def test_processed_document_rejects_invalid_ingestion_status() -> None:
    with pytest.raises(ValueError):
        ProcessedDocument(
            source_pdf_id="policy-a",
            source_pdf_path="data/raw/policy-a.pdf",
            markdown_output_path="data/markdown/policy-a.md",
            cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
            processed_output_path="data/processed/policy-a.json",
            document_name="policy-a",
            document_version=None,
            ingestion_status="completed",
            error_message=None,
            ingested_at="2026-05-18T00:00:00Z",
        )
