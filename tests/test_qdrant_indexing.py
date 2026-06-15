from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID

import pytest

from contracts import (
    EmbeddingBundle,
    EmbeddingIndexingRecord,
    EmbeddingRecord,
    VectorPayload,
)
from core.config import DEFAULT_EMBEDDING_MODEL, Settings
from rag.ingestion import build_parser, build_qdrant_point_id, main


def build_embedding_bundle_artifact(embedding_artifact_path: str) -> EmbeddingBundle:
    return EmbeddingBundle(
        source_pdf_id="policy-a",
        document_name="Policy A",
        document_version="2026-01",
        source_chunk_artifact_path="data/processed/chunks/policy-a.chunks.json",
        embedding_artifact_path=embedding_artifact_path,
        embedding_schema_version="v1",
        chunk_schema_version="v2",
        embedding_provider="sentence-transformers",
        embedding_model=DEFAULT_EMBEDDING_MODEL,
        vector_dimension=3,
        embeddings=[
            EmbeddingRecord(
                chunk_id="policy-a:v2:0000",
                source_pdf_id="policy-a",
                chunk_schema_version="v2",
                embedding_provider="sentence-transformers",
                embedding_model=DEFAULT_EMBEDDING_MODEL,
                vector_dimension=3,
                vector=[0.1, 0.2, 0.3],
                payload=VectorPayload(
                    chunk_id="policy-a:v2:0000",
                    source_pdf_id="policy-a",
                    source_pdf_relative_path="policy-a.pdf",
                    chunk_schema_version="v2",
                    chunk_index=0,
                    document_name="Policy A",
                    document_version="2026-01",
                    section="Coverage",
                    section_path=["Policy A", "Coverage"],
                    text="Coverage applies.",
                ),
            ),
            EmbeddingRecord(
                chunk_id="policy-a:v2:0001",
                source_pdf_id="policy-a",
                chunk_schema_version="v2",
                embedding_provider="sentence-transformers",
                embedding_model=DEFAULT_EMBEDDING_MODEL,
                vector_dimension=3,
                vector=[0.4, 0.5, 0.6],
                payload=VectorPayload(
                    chunk_id="policy-a:v2:0001",
                    source_pdf_id="policy-a",
                    source_pdf_relative_path="policy-a.pdf",
                    chunk_schema_version="v2",
                    chunk_index=1,
                    document_name="Policy A",
                    document_version="2026-01",
                    section="Exclusions",
                    section_path=["Policy A", "Exclusions"],
                    text="Exclusions apply.",
                ),
            ),
        ],
    )


def build_embedding_bundle_for_source(
    source_pdf_id: str,
    embedding_artifact_path: str,
) -> EmbeddingBundle:
    bundle = build_embedding_bundle_artifact(embedding_artifact_path)
    return bundle.model_copy(
        update={
            "source_pdf_id": source_pdf_id,
            "embedding_artifact_path": embedding_artifact_path,
            "embeddings": [
                record.model_copy(
                    update={
                        "chunk_id": record.chunk_id.replace("policy-a", source_pdf_id),
                        "source_pdf_id": source_pdf_id,
                        "payload": record.payload.model_copy(
                            update={
                                "chunk_id": record.payload.chunk_id.replace(
                                    "policy-a",
                                    source_pdf_id,
                                ),
                                "source_pdf_id": source_pdf_id,
                            }
                        ),
                    }
                )
                for record in bundle.embeddings
            ],
        }
    )


class FakeCollectionInfo:
    def __init__(self, size: int) -> None:
        self.config = SimpleNamespace(
            params=SimpleNamespace(vectors=SimpleNamespace(size=size))
        )


class FakeQdrantClient:
    def __init__(self) -> None:
        self.collection_size: int | None = None
        self.points: dict[str, object] = {}
        self.upsert_calls = 0
        self.delete_calls = 0
        self.payload_indexes: list[tuple[str, object, bool]] = []

    def get_collection(self, collection_name: str):
        if self.collection_size is None:
            raise RuntimeError("missing collection")
        return FakeCollectionInfo(self.collection_size)

    def create_collection(self, collection_name: str, vectors_config: object) -> None:
        self.collection_size = vectors_config.size

    def create_payload_index(
        self,
        *,
        collection_name: str,
        field_name: str,
        field_schema: object,
        wait: bool,
    ) -> None:
        self.payload_indexes.append((field_name, field_schema, wait))

    def upsert(self, collection_name: str, points: list[object], wait: bool) -> None:
        self.upsert_calls += 1
        for point in points:
            self.points[point.id] = point

    def delete(self, collection_name: str, points_selector: object, wait: bool) -> None:
        self.delete_calls += 1
        must_conditions = getattr(points_selector, "must", [])
        source_pdf_id = None
        for condition in must_conditions:
            if getattr(condition, "key", None) != "source_pdf_id":
                continue
            match = getattr(condition, "match", None)
            source_pdf_id = getattr(match, "value", None)
            break
        if source_pdf_id is None:
            return
        self.points = {
            point_id: point
            for point_id, point in self.points.items()
            if point.payload.get("source_pdf_id") != source_pdf_id
        }

    def count(self, collection_name: str, exact: bool):
        return SimpleNamespace(count=len(self.points))


class FakeQdrantClientWithoutPayloadIndex(FakeQdrantClient):
    create_payload_index = None


class FakeTransientError(RuntimeError):
    transient = True


def fake_qdrant_models():
    class MatchValue:
        def __init__(self, value: object) -> None:
            self.value = value

    class FieldCondition:
        def __init__(self, key: str, match: MatchValue) -> None:
            self.key = key
            self.match = match

    class Filter:
        def __init__(self, must: list[FieldCondition]) -> None:
            self.must = must

    class PayloadSchemaType:
        KEYWORD = "keyword"

    class Distance:
        COSINE = "cosine"

    class VectorParams:
        def __init__(self, size: int, distance: str) -> None:
            self.size = size
            self.distance = distance

    class PointStruct:
        def __init__(self, id: str, vector: list[float], payload: dict[str, object]) -> None:
            self.id = id
            self.vector = vector
            self.payload = payload

    return SimpleNamespace(
        Distance=Distance,
        FieldCondition=FieldCondition,
        Filter=Filter,
        MatchValue=MatchValue,
        PayloadSchemaType=PayloadSchemaType,
        PointStruct=PointStruct,
        VectorParams=VectorParams,
    )


def test_parser_builds_qdrant_indexing_command() -> None:
    args = build_parser().parse_args(["index-embeddings"])

    assert args.command == "index-embeddings"
    assert args.embedding_dir == "data/processed/embeddings"
    assert args.manifest_path == "data/processed/qdrant-indexing-manifest.jsonl"
    assert args.glob == "*.embeddings.json"
    assert args.max_retries == 3


def test_qdrant_indexing_fails_when_embedding_directory_is_missing(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(tmp_path / "missing"),
            "--manifest-path",
            str(tmp_path / "qdrant-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Embedding directory does not exist" in captured.err


def test_qdrant_indexing_fails_when_required_config_is_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    (embedding_dir / "policy-a.embeddings.json").write_text(
        build_embedding_bundle_artifact(
            str(embedding_dir / "policy-a.embeddings.json")
        ).model_dump_json(indent=2),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(_env_file=None, qdrant_url=None, qdrant_api_key=None),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(tmp_path / "qdrant-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "QDRANT_URL is required" in captured.err


def test_qdrant_indexing_bootstraps_collection_and_indexes_points(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingIndexingRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert fake_client.collection_size == 3
    assert fake_client.payload_indexes == [
        ("document_type", "keyword", True),
        ("product", "keyword", True),
        ("document_name", "keyword", True),
        ("source_pdf_id", "keyword", True),
    ]
    assert len(fake_client.points) == 2
    for point_id, point in fake_client.points.items():
        assert str(UUID(point_id)) == point_id
        assert point.payload["chunk_id"].startswith("policy-a:v2:")
    assert manifest_record.indexing_status == "succeeded"
    assert manifest_record.indexed_point_count == 2


def test_build_qdrant_point_id_is_deterministic_uuid() -> None:
    bundle = build_embedding_bundle_artifact("data/processed/embeddings/policy-a.embeddings.json")
    first_id = build_qdrant_point_id(bundle.embeddings[0])
    second_id = build_qdrant_point_id(bundle.embeddings[0])

    assert first_id == second_id
    assert str(UUID(first_id)) == first_id


def test_qdrant_indexing_fails_for_incompatible_collection_shape(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()
    fake_client.collection_size = 5

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingIndexingRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert manifest_record.indexing_status == "failed"
    assert "incompatible" in manifest_record.error_message.lower()


def test_qdrant_indexing_is_idempotent_across_reruns(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    first_exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )
    second_exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    assert first_exit_code == 0
    assert second_exit_code == 0
    assert len(fake_client.points) == 2
    assert fake_client.upsert_calls == 2
    assert fake_client.delete_calls == 2
    assert fake_client.payload_indexes == [
        ("document_type", "keyword", True),
        ("product", "keyword", True),
        ("document_name", "keyword", True),
        ("source_pdf_id", "keyword", True),
        ("document_type", "keyword", True),
        ("product", "keyword", True),
        ("document_name", "keyword", True),
        ("source_pdf_id", "keyword", True),
    ]


def test_qdrant_indexing_skips_payload_index_creation_when_client_lacks_support(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClientWithoutPayloadIndex()

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    assert exit_code == 0
    assert len(fake_client.points) == 2


def test_qdrant_indexing_prunes_legacy_points_for_same_source_pdf_id(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()
    stale_point = SimpleNamespace(
        id="legacy-policy-a",
        payload={
            "chunk_id": "policy-a:v2:legacy",
            "source_pdf_id": "policy-a",
            "text": "legacy stale payload",
        },
    )
    unrelated_point = SimpleNamespace(
        id="policy-b-existing",
        payload={
            "chunk_id": "policy-b:v2:0000",
            "source_pdf_id": "policy-b",
            "text": "other source",
        },
    )
    fake_client.points = {
        stale_point.id: stale_point,
        unrelated_point.id: unrelated_point,
    }

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    assert exit_code == 0
    assert fake_client.delete_calls == 1
    assert "legacy-policy-a" not in fake_client.points
    assert "policy-b-existing" in fake_client.points
    assert len(fake_client.points) == 3


def test_qdrant_indexing_retries_transient_failures(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()
    sleep_calls: list[float] = []

    def flaky_upsert(collection_name: str, points: list[object], wait: bool) -> None:
        if fake_client.upsert_calls == 0:
            fake_client.upsert_calls += 1
            raise FakeTransientError("temporary")
        fake_client.upsert_calls += 1
        for point in points:
            fake_client.points[point.id] = point

    fake_client.upsert = flaky_upsert  # type: ignore[method-assign]

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.sleep_with_backoff",
        lambda seconds: sleep_calls.append(seconds),
    )
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    assert exit_code == 0
    assert sleep_calls == [0.25]
    assert len(fake_client.points) == 2


def test_qdrant_indexing_records_permanent_upsert_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    artifact_path = embedding_dir / "policy-a.embeddings.json"
    artifact_path.write_text(
        build_embedding_bundle_artifact(str(artifact_path)).model_dump_json(indent=2),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()

    def failing_upsert(collection_name: str, points: list[object], wait: bool) -> None:
        raise RuntimeError("permanent upsert failure")

    fake_client.upsert = failing_upsert  # type: ignore[method-assign]

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = EmbeddingIndexingRecord.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert manifest_record.indexing_status == "failed"
    assert manifest_record.error_message == "permanent upsert failure"


def test_qdrant_indexing_continues_after_one_failure_when_fail_fast_is_false(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    embedding_dir = tmp_path / "embeddings"
    embedding_dir.mkdir()
    first_artifact_path = embedding_dir / "policy-a.embeddings.json"
    second_artifact_path = embedding_dir / "policy-b.embeddings.json"
    first_artifact_path.write_text(
        build_embedding_bundle_for_source("policy-a", str(first_artifact_path)).model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )
    second_artifact_path.write_text(
        build_embedding_bundle_for_source("policy-b", str(second_artifact_path)).model_dump_json(
            indent=2
        ),
        encoding="utf-8",
    )
    manifest_path = tmp_path / "qdrant-manifest.jsonl"
    fake_client = FakeQdrantClient()

    def selective_upsert(collection_name: str, points: list[object], wait: bool) -> None:
        if any(point.payload["chunk_id"].startswith("policy-a:") for point in points):
            raise RuntimeError("policy-a failed")
        for point in points:
            fake_client.points[point.id] = point

    fake_client.upsert = selective_upsert  # type: ignore[method-assign]

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: fake_client)
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
    )

    exit_code = main(
        [
            "index-embeddings",
            "--embedding-dir",
            str(embedding_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_records = [
        EmbeddingIndexingRecord.model_validate_json(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]

    assert exit_code == 0
    assert [record.indexing_status for record in manifest_records] == ["failed", "succeeded"]
    assert any(
        point.payload["chunk_id"].startswith("policy-b:")
        for point in fake_client.points.values()
    )
