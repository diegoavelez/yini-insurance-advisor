from __future__ import annotations

import argparse

import pytest

from contracts import ProcessedDocument
from rag.ingestion import (
    build_parser,
    docling_is_available,
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
    assert args.glob == "*.pdf"
    assert args.overwrite is True
    assert args.fail_fast is False


def test_docling_smoke_check_reflects_importability() -> None:
    assert isinstance(docling_is_available(), bool)


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
    processed_output = processed_dir / "policy-a.json"
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert markdown_output.read_text(encoding="utf-8") == "# Converted policy-a"
    assert processed_document.source_pdf_id == "policy-a"
    assert processed_document.markdown_output_path == str(markdown_output)
    assert processed_document.processed_output_path == str(processed_output)
    assert processed_document.ingestion_status == "succeeded"
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
        processed_output_path=str(processed_dir / "policy-a.json"),
        document_name="policy-a",
        document_version=None,
        ingestion_status="succeeded",
        error_message=None,
        ingested_at="2026-05-18T00:00:00Z",
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
            processed_output_path="data/processed/policy-a.json",
            document_name="policy-a",
            document_version=None,
            ingestion_status="completed",
            error_message=None,
            ingested_at="2026-05-18T00:00:00Z",
        )
