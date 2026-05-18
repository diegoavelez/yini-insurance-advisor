from __future__ import annotations

from pathlib import Path

import pytest

from contracts import ChunkBundle, ChunkRecord, EmbeddingBundle, EmbeddingGenerationRecord
from core.config import Settings, clear_settings_cache
from rag.ingestion import build_parser, main


def build_chunk_bundle_artifact(chunk_artifact_path: Path) -> ChunkBundle:
    return ChunkBundle(
        source_pdf_id="policy-a",
        document_name="Policy A",
        document_version="2026-01",
        source_pdf_path="data/raw/policy-a.pdf",
        cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
        chunk_artifact_path=str(chunk_artifact_path),
        chunk_size=1200,
        chunk_overlap=200,
        chunk_schema_version="v2",
        chunks=[
            ChunkRecord(
                chunk_id="policy-a:v2:0000",
                source_pdf_id="policy-a",
                document_name="Policy A",
                document_version="2026-01",
                source_pdf_path="data/raw/policy-a.pdf",
                cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
                text="Coverage applies to outpatient care.",
                chunk_index=0,
                chunk_schema_version="v2",
                section="Coverage",
                section_path=["Policy A", "Coverage"],
            ),
            ChunkRecord(
                chunk_id="policy-a:v2:0001",
                source_pdf_id="policy-a",
                document_name="Policy A",
                document_version="2026-01",
                source_pdf_path="data/raw/policy-a.pdf",
                cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
                text="Exclusions apply to cosmetic procedures.",
                chunk_index=1,
                chunk_schema_version="v2",
                section="Exclusions",
                section_path=["Policy A", "Exclusions"],
            ),
        ],
    )


def test_parser_builds_embedding_generation_command() -> None:
    args = build_parser().parse_args(
        [
            "generate-embeddings",
            "--chunk-dir",
            "data/processed/chunks",
            "--manifest-path",
            "data/processed/embedding-manifest.jsonl",
        ]
    )

    assert args.command == "generate-embeddings"
    assert args.glob == "*.chunks.json"
    assert args.embedding_dir == "data/processed/embeddings"
    assert args.overwrite is False
    assert args.fail_fast is False


def test_embedding_generation_fails_when_chunk_directory_is_missing(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(tmp_path / "missing"),
            "--embedding-dir",
            str(tmp_path / "embeddings"),
            "--manifest-path",
            str(tmp_path / "embedding-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Chunk directory does not exist" in captured.err


def test_embedding_generation_fails_when_provider_is_unsupported(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    chunk_artifact_path = chunk_dir / "policy-a.chunks.json"
    chunk_artifact_path.write_text(
        build_chunk_bundle_artifact(chunk_artifact_path).model_dump_json(indent=2),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            embedding_provider="mock-provider",
            embedding_model="test-model",
        ),
    )

    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(chunk_dir),
            "--embedding-dir",
            str(tmp_path / "embeddings"),
            "--manifest-path",
            str(tmp_path / "embedding-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "EMBEDDING_PROVIDER must be sentence-transformers" in captured.err


def test_successful_embedding_generation_writes_typed_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    clear_settings_cache()
    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    chunk_artifact_path = chunk_dir / "policy-a.chunks.json"
    chunk_artifact_path.write_text(
        build_chunk_bundle_artifact(chunk_artifact_path).model_dump_json(indent=2),
        encoding="utf-8",
    )
    embedding_dir = tmp_path / "embeddings"
    manifest_path = tmp_path / "embedding-manifest.jsonl"
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            embedding_provider="sentence-transformers",
            embedding_model="BAAI/bge-small-en-v1.5",
        ),
    )
    monkeypatch.setattr("rag.ingestion.embedding_backend_is_available", lambda settings: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [float(len(text)), 0.5, 1.0],
    )

    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(chunk_dir),
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    artifact_path = embedding_dir / "policy-a.embeddings.json"
    embedding_bundle = EmbeddingBundle.model_validate_json(
        artifact_path.read_text(encoding="utf-8")
    )
    manifest_record = EmbeddingGenerationRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert embedding_bundle.embedding_schema_version == "v1"
    assert embedding_bundle.embedding_provider == "sentence-transformers"
    assert embedding_bundle.embedding_model == "BAAI/bge-small-en-v1.5"
    assert [record.chunk_id for record in embedding_bundle.embeddings] == [
        "policy-a:v2:0000",
        "policy-a:v2:0001",
    ]
    assert embedding_bundle.embeddings[0].payload.section_path == ["Policy A", "Coverage"]
    assert manifest_record.generation_status == "succeeded"


def test_embedding_generation_skips_existing_artifact_when_overwrite_is_false(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    chunk_artifact_path = chunk_dir / "policy-a.chunks.json"
    chunk_artifact_path.write_text(
        build_chunk_bundle_artifact(chunk_artifact_path).model_dump_json(indent=2),
        encoding="utf-8",
    )
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text("existing artifact", encoding="utf-8")
    manifest_path = tmp_path / "embedding-manifest.jsonl"
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            embedding_provider="sentence-transformers",
            embedding_model="BAAI/bge-small-en-v1.5",
        ),
    )
    monkeypatch.setattr("rag.ingestion.embedding_backend_is_available", lambda settings: True)

    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(chunk_dir),
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingGenerationRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert artifact_path.read_text(encoding="utf-8") == "existing artifact"
    assert manifest_record.generation_status == "skipped"


def test_embedding_generation_failure_removes_partial_artifact_and_records_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    chunk_artifact_path = chunk_dir / "policy-a.chunks.json"
    chunk_artifact_path.write_text(
        build_chunk_bundle_artifact(chunk_artifact_path).model_dump_json(indent=2),
        encoding="utf-8",
    )
    embedding_dir = tmp_path / "embeddings"
    manifest_path = tmp_path / "embedding-manifest.jsonl"
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            embedding_provider="sentence-transformers",
            embedding_model="BAAI/bge-small-en-v1.5",
        ),
    )
    monkeypatch.setattr("rag.ingestion.embedding_backend_is_available", lambda settings: True)

    def fail_embedding(text: str, settings: Settings) -> list[float]:
        artifact_path = embedding_dir / "policy-a.embeddings.json"
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text("partial artifact", encoding="utf-8")
        raise RuntimeError("embedding generation failed")

    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", fail_embedding)

    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(chunk_dir),
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingGenerationRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert not (embedding_dir / "policy-a.embeddings.json").exists()
    assert manifest_record.generation_status == "failed"
    assert manifest_record.error_message == "embedding generation failed"


def test_malformed_chunk_artifact_records_failed_manifest(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    chunk_dir = tmp_path / "chunks"
    chunk_dir.mkdir()
    chunk_artifact_path = chunk_dir / "policy-a.chunks.json"
    chunk_artifact_path.write_text("{invalid json", encoding="utf-8")
    embedding_dir = tmp_path / "embeddings"
    manifest_path = tmp_path / "embedding-manifest.jsonl"
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            embedding_provider="sentence-transformers",
            embedding_model="BAAI/bge-small-en-v1.5",
        ),
    )
    monkeypatch.setattr("rag.ingestion.embedding_backend_is_available", lambda settings: True)

    exit_code = main(
        [
            "generate-embeddings",
            "--chunk-dir",
            str(chunk_dir),
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingGenerationRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert manifest_record.source_pdf_id == "policy-a"
    assert manifest_record.generation_status == "failed"
    assert "chunk artifact load failed" in manifest_record.error_message
