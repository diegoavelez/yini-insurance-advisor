from __future__ import annotations

from types import SimpleNamespace

import pytest

from contracts import RetrievalQuery
from core.config import Settings
from rag.ingestion import build_parser, main, retrieve_ranked_chunks


class FakeQdrantRetrievalClient:
    def __init__(self, hits: list[object]) -> None:
        self.hits = hits
        self.last_query: dict[str, object] | None = None

    def search(
        self,
        *,
        collection_name: str,
        query_vector: list[float],
        query_filter: object,
        limit: int,
        with_payload: bool,
    ) -> list[object]:
        self.last_query = {
            "collection_name": collection_name,
            "query_vector": query_vector,
            "query_filter": query_filter,
            "limit": limit,
            "with_payload": with_payload,
        }
        return self.hits


class FakeQdrantQueryPointsClient:
    def __init__(self, hits: list[object]) -> None:
        self.hits = hits
        self.last_query: dict[str, object] | None = None

    def query_points(
        self,
        *,
        collection_name: str,
        query: list[float],
        query_filter: object,
        limit: int,
        with_payload: bool,
    ) -> object:
        self.last_query = {
            "collection_name": collection_name,
            "query": query,
            "query_filter": query_filter,
            "limit": limit,
            "with_payload": with_payload,
        }
        return SimpleNamespace(points=self.hits)


def fake_qdrant_models():
    class MatchValue:
        def __init__(self, value: object) -> None:
            self.value = value

    class FieldCondition:
        def __init__(self, key: str, match: object) -> None:
            self.key = key
            self.match = match

    class Filter:
        def __init__(self, must: list[object]) -> None:
            self.must = must

    return SimpleNamespace(MatchValue=MatchValue, FieldCondition=FieldCondition, Filter=Filter)


def make_hit(
    *,
    chunk_id: str,
    text: str,
    document_name: str,
    score: float,
    section: str | None = None,
) -> object:
    return SimpleNamespace(
        payload={
            "chunk_id": chunk_id,
            "source_pdf_id": "policy-a",
            "source_pdf_relative_path": "autonomia/vida/policy-a.pdf",
            "chunk_schema_version": "v2",
            "chunk_index": 1,
            "text": text,
            "document_name": document_name,
            "document_version": "2026-01",
            "section": section,
            "section_path": ["Policy A", section] if section else [],
        },
        score=score,
    )


def test_parser_builds_retrieval_command() -> None:
    args = build_parser().parse_args(["retrieve-chunks", "--query", "coverage"])

    assert args.command == "retrieve-chunks"
    assert args.query == "coverage"
    assert args.top_k is None


def test_retrieve_ranked_chunks_maps_search_hits_in_ranked_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            make_hit(
                chunk_id="policy-a:v2:0001",
                text="Second ranked chunk",
                document_name="Policy A",
                score=0.92,
                section="Coverage",
            ),
            make_hit(
                chunk_id="policy-a:v2:0000",
                text="First ranked chunk",
                document_name="Policy A",
                score=0.87,
                section="Exclusions",
            ),
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(query="coverage", top_k=2),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert [chunk.chunk_id for chunk in result.chunks] == [
        "policy-a:v2:0001",
        "policy-a:v2:0000",
    ]
    assert result.chunks[0].score == 0.92
    assert result.chunks[0].section == "Coverage"
    assert result.chunks[0].source_pdf_id == "policy-a"
    assert result.chunks[0].source_pdf_relative_path == "autonomia/vida/policy-a.pdf"
    assert result.chunks[0].chunk_schema_version == "v2"
    assert result.chunks[0].chunk_index == 1
    assert result.chunks[0].document_version == "2026-01"
    assert result.chunks[0].section_path == ["Policy A", "Coverage"]


def test_retrieve_ranked_chunks_supports_query_points_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantQueryPointsClient(
        [
            make_hit(
                chunk_id="policy-a:v2:0001",
                text="Second ranked chunk",
                document_name="Policy A",
                score=0.92,
                section="Coverage",
            )
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(query="coverage", top_k=1),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert [chunk.chunk_id for chunk in result.chunks] == ["policy-a:v2:0001"]
    assert client.last_query is not None
    assert client.last_query["query"] == [0.1, 0.2]


def test_retrieve_ranked_chunks_allows_missing_relative_path_for_older_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            SimpleNamespace(
                payload={
                    "chunk_id": "policy-a:v2:0001",
                    "source_pdf_id": "policy-a",
                    "chunk_schema_version": "v2",
                    "chunk_index": 1,
                    "text": "Coverage chunk",
                    "document_name": "Policy A",
                    "document_version": "2026-01",
                    "section": "Coverage",
                    "section_path": ["Policy A", "Coverage"],
                },
                score=0.92,
            )
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(query="coverage", top_k=1),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].source_pdf_relative_path is None


def test_retrieve_ranked_chunks_returns_empty_result_explicitly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(query="missing", top_k=3),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks == []


def test_retrieve_ranked_chunks_fails_for_missing_qdrant_config() -> None:
    with pytest.raises(ValueError):
        retrieve_ranked_chunks(
            RetrievalQuery(query="coverage"),
            settings=Settings(_env_file=None, qdrant_url=None, qdrant_api_key=None),
            client=FakeQdrantRetrievalClient([]),
        )


def test_retrieve_ranked_chunks_fails_for_malformed_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [SimpleNamespace(payload={"text": "missing chunk id"}, score=0.5)]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    with pytest.raises(RuntimeError):
        retrieve_ranked_chunks(
            RetrievalQuery(query="coverage"),
            settings=Settings(
                _env_file=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            client=client,
        )


def test_retrieve_ranked_chunks_fails_for_non_dict_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([SimpleNamespace(payload="bad payload", score=0.5)])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    with pytest.raises(RuntimeError):
        retrieve_ranked_chunks(
            RetrievalQuery(query="coverage"),
            settings=Settings(
                _env_file=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            client=client,
        )


def test_retrieve_ranked_chunks_fails_for_missing_document_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [SimpleNamespace(payload={"chunk_id": "policy-a:v2:0000", "text": "x"}, score=0.5)]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    with pytest.raises(RuntimeError):
        retrieve_ranked_chunks(
            RetrievalQuery(query="coverage"),
            settings=Settings(
                _env_file=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            client=client,
        )


def test_retrieve_ranked_chunks_uses_filters_in_qdrant_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    retrieve_ranked_chunks(
        RetrievalQuery(
            query="coverage",
            top_k=4,
            filters={
                "document_name": "Policy A",
                "version": "2026-01",
            },
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    query_filter = client.last_query["query_filter"]
    assert client.last_query["limit"] == 4
    assert len(query_filter.must) == 2


def test_retrieve_ranked_chunks_rejects_unsupported_document_type_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    with pytest.raises(RuntimeError, match="document_type"):
        retrieve_ranked_chunks(
            RetrievalQuery(
                query="coverage",
                filters={"document_type": "policy"},
            ),
            settings=Settings(
                _env_file=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            client=client,
        )


def test_retrieve_ranked_chunks_rejects_unsupported_product_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )

    with pytest.raises(RuntimeError, match="product"):
        retrieve_ranked_chunks(
            RetrievalQuery(
                query="coverage",
                filters={"product": "health"},
            ),
            settings=Settings(
                _env_file=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            client=client,
        )


def test_retrieve_cli_prints_typed_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            make_hit(
                chunk_id="policy-a:v2:0000",
                text="Coverage applies.",
                document_name="Policy A",
                score=0.8,
                section="Coverage",
            )
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.create_qdrant_client", lambda settings: client)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
            top_k=7,
        ),
    )

    exit_code = main(["retrieve-chunks", "--query", "coverage"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"chunk_id": "policy-a:v2:0000"' in captured.out
