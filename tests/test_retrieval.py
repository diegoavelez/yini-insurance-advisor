from __future__ import annotations

from types import SimpleNamespace

import pytest

from contracts import ChunkRecord, QueryExpansionRule, RetrievalQuery, TermEquivalenceSet
from core.config import Settings
from rag.ingestion import build_hybrid_recall_terms, build_parser, main, retrieve_ranked_chunks


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
            "document_type": "policy",
            "product": "health",
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
    assert result.chunks[0].document_type == "policy"
    assert result.chunks[0].product == "health"
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


def test_retrieve_ranked_chunks_supports_document_type_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)

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

    query_filter = client.last_query["query_filter"]
    assert len(query_filter.must) == 1
    assert query_filter.must[0].key == "document_type"
    assert query_filter.must[0].match.value == "policy"


def test_retrieve_ranked_chunks_supports_product_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)

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

    query_filter = client.last_query["query_filter"]
    assert len(query_filter.must) == 1
    assert query_filter.must[0].key == "product"
    assert query_filter.must[0].match.value == "health"


def test_retrieve_ranked_chunks_supports_combined_metadata_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)

    retrieve_ranked_chunks(
        RetrievalQuery(
            query="coverage",
            filters={
                "document_type": "policy",
                "product": "health",
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
    assert len(query_filter.must) == 4
    assert [(condition.key, condition.match.value) for condition in query_filter.must] == [
        ("document_type", "policy"),
        ("product", "health"),
        ("document_name", "Policy A"),
        ("document_version", "2026-01"),
    ]


def test_retrieve_ranked_chunks_applies_operator_term_equivalences_to_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])
    captured_query: dict[str, str] = {}

    def capture_embedding_query(text: str, settings: Settings) -> list[float]:
        captured_query["query"] = text
        return [0.1, 0.2]

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", capture_embedding_query)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(query_aliases={"auto": ["carro", "vehículo"]}),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(query="¿Qué cubre el carro?", top_k=2),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert "Términos equivalentes: auto" in captured_query["query"]


def test_retrieve_ranked_chunks_applies_operator_query_expansion_rules(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])
    captured_query: dict[str, str] = {}

    def capture_embedding_query(text: str, settings: Settings) -> list[float]:
        captured_query["query"] = text
        return [0.1, 0.2]

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", capture_embedding_query)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=[
                        "diferenciales sura",
                        "plan autos básico pérdidas totales",
                        "plan autos global",
                        "plan autos clásico",
                        "franquicia",
                        "nuevo de nuevo",
                        "pequeños eventos",
                    ],
                )
            ]
        ),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Qué diferencias hay entre el plan básico y los otros planes de autos?"
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert "Términos equivalentes:" in captured_query["query"]
    assert "diferenciales sura" in captured_query["query"]
    assert "plan autos básico pérdidas totales" in captured_query["query"]
    assert "plan autos global" in captured_query["query"]
    assert "plan autos clásico" in captured_query["query"]
    assert "franquicia" in captured_query["query"]
    assert "nuevo de nuevo" in captured_query["query"]


def test_retrieve_ranked_chunks_applies_motos_comparison_query_expansion_rules(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])
    captured_query: dict[str, str] = {}

    def capture_embedding_query(text: str, settings: Settings) -> list[float]:
        captured_query["query"] = text
        return [0.1, 0.2]

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", capture_embedding_query)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["motos"],
                    any_of=[
                        "diferencias",
                        "comparar",
                        "comparación",
                        "comparacion",
                        "comparativo",
                        "planes",
                    ],
                    append_terms=[
                        "comparativo motos",
                        "suratech",
                        "plan total",
                        "plan premium",
                        "bajo cilindraje",
                        "alto cilindraje",
                        "esencial",
                    ],
                )
            ]
        ),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(query="¿Qué diferencias hay entre los planes de motos?"),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert "Términos equivalentes:" in captured_query["query"]
    assert "comparativo motos" in captured_query["query"]
    assert "suratech" in captured_query["query"]
    assert "plan total" in captured_query["query"]
    assert "plan premium" in captured_query["query"]
    assert "bajo cilindraje" in captured_query["query"]
    assert "alto cilindraje" in captured_query["query"]


def test_build_hybrid_recall_terms_skips_anchor_restatement_append_terms() -> None:
    terms = build_hybrid_recall_terms(
        "¿Qué diferencias hay entre el plan básico y los otros planes de autos?",
        matched_expansion_rules=[
            QueryExpansionRule(
                all_of=["plan básico", "autos"],
                any_of=["diferencias", "otros planes"],
                append_terms=[
                    "plan autos básico pérdidas totales",
                    "plan autos global",
                    "plan autos clásico",
                    "franquicia",
                ],
            )
        ],
    )

    assert "¿Qué diferencias hay entre el plan básico y los otros planes de autos?" in terms
    assert "plan autos básico pérdidas totales" not in terms
    assert "plan autos global" in terms
    assert "plan autos clásico" in terms
    assert "franquicia" in terms


def test_retrieve_ranked_chunks_does_not_apply_comparison_bundle_without_comparison_intent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])
    captured_query: dict[str, str] = {}

    def capture_embedding_query(text: str, settings: Settings) -> list[float]:
        captured_query["query"] = text
        return [0.1, 0.2]

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", capture_embedding_query)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=[
                        "plan autos global",
                        "plan autos clásico",
                        "diferenciales planes autos",
                    ],
                )
            ]
        ),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(query="¿Qué cubre el plan básico de autos?"),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert captured_query["query"] == "¿Qué cubre el plan básico de autos?"
    assert client.last_query["limit"] == 5


def test_retrieve_ranked_chunks_applies_deductible_query_expansion_rules(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])
    captured_query: dict[str, str] = {}

    def capture_embedding_query(text: str, settings: Settings) -> list[float]:
        captured_query["query"] = text
        return [0.1, 0.2]

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.generate_embedding_vector", capture_embedding_query)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["deducible"],
                    any_of=["bicicletas", "patinetas"],
                    append_terms=[
                        "smlmv",
                        "pérdida total",
                        "hurto",
                        "renta diaria por hospitalización",
                    ],
                )
            ]
        ),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(query="¿Cuál es el deducible del seguro de bicicletas y patinetas?"),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert "Términos equivalentes:" in captured_query["query"]
    assert "smlmv" in captured_query["query"]
    assert "pérdida total" in captured_query["query"]
    assert "hurto" in captured_query["query"]


def test_retrieve_ranked_chunks_adds_local_lexical_candidates_for_deductible_queries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            SimpleNamespace(
                payload={
                    "chunk_id": "guide:v2:0000",
                    "source_pdf_id": "guide",
                    "source_pdf_relative_path": "MOVILIDAD/BICICLETAS Y PATINETAS/ayudaventas.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 0,
                    "text": "Servicios y asistencias para bicicletas y patinetas.",
                    "document_name": "Sentirte acompañado",
                    "document_version": None,
                    "document_type": "guide",
                    "product": "movilidad",
                    "section": "Acompañamiento",
                    "section_path": ["Sentirte acompañado", "Acompañamiento"],
                },
                score=0.92,
            ),
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["deducible"],
                    any_of=["bicicletas", "patinetas"],
                    append_terms=["smlmv", "pérdida total", "hurto"],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (
            ChunkRecord(
                chunk_id="pv:v2:0008",
                source_pdf_id="pv",
                document_name="pv bicis y patinetas v2",
                document_version="1",
                document_type="guide",
                product="movilidad",
                source_pdf_path="data/raw/MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                source_pdf_relative_path="MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                cleaned_markdown_output_path="data/processed/pv.cleaned.md",
                text=(
                    "DEDUCIBLE. Bicis: Entre $600.000 y $3.000.000. "
                    "No aplica cobertura 15%. SMLMV. Hurto."
                ),
                chunk_index=8,
                chunk_schema_version="v2",
                section="DEDUCIBLE",
                section_path=["pv bicis y patinetas v2", "DEDUCIBLE"],
            ),
        ),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Cuál es el deducible del seguro de bicicletas y patinetas?",
            top_k=2,
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].section == "DEDUCIBLE"
    assert result.chunks[0].chunk_id == "pv:v2:0008"


def test_retrieve_ranked_chunks_biases_explicit_deductible_sections_for_deductible_queries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            SimpleNamespace(
                payload={
                    "chunk_id": "guide:v2:0000",
                    "source_pdf_id": "guide",
                    "source_pdf_relative_path": "MOVILIDAD/BICICLETAS Y PATINETAS/guide.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 0,
                    "text": "Valor comercial menos el deducible pactado.",
                    "document_name": "Sentirte acompañado",
                    "document_version": None,
                    "document_type": "guide",
                    "product": "movilidad",
                    "section": "Pérdida total",
                    "section_path": ["Sentirte acompañado", "Pérdida total"],
                },
                score=0.92,
            ),
            SimpleNamespace(
                payload={
                    "chunk_id": "pv:v2:0008",
                    "source_pdf_id": "pv",
                    "source_pdf_relative_path": "MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 8,
                    "text": "DEDUCIBLE. Bicis: Entre $600.000 y $3.000.000.",
                    "document_name": "pv bicis y patinetas v2",
                    "document_version": "1",
                    "document_type": "guide",
                    "product": "movilidad",
                    "section": "DEDUCIBLE",
                    "section_path": ["pv bicis y patinetas v2", "DEDUCIBLE"],
                },
                score=0.80,
            ),
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["deducible"],
                    any_of=["bicicletas", "patinetas"],
                    append_terms=["smlmv", "pérdida total", "hurto"],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Cuál es el deducible del seguro de bicicletas y patinetas?",
            top_k=2,
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].section == "DEDUCIBLE"
    assert result.chunks[0].chunk_id == "pv:v2:0008"


def test_retrieve_ranked_chunks_prefers_local_deductible_candidate_over_adjacent_sections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["deducible"],
                    any_of=["bicicletas", "patinetas"],
                    append_terms=[
                        "smlmv",
                        "pérdida total",
                        "hurto",
                        "renta diaria por hospitalización",
                        "expedición requisitos",
                    ],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (
            ChunkRecord(
                chunk_id="pv:v2:0006",
                source_pdf_id="pv",
                document_name="pv bicis y patinetas v2",
                document_version="1",
                document_type="guide",
                product="movilidad",
                source_pdf_path="data/raw/MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                source_pdf_relative_path="MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                cleaned_markdown_output_path="data/processed/pv.cleaned.md",
                text="EXPEDICIÓN REQUISITOS. valor comercial menos el deducible pactado.",
                chunk_index=6,
                chunk_schema_version="v2",
                section="EXPEDICIÓN REQUISITOS",
                section_path=["pv bicis y patinetas v2", "EXPEDICIÓN REQUISITOS"],
            ),
            ChunkRecord(
                chunk_id="pv:v2:0008",
                source_pdf_id="pv",
                document_name="pv bicis y patinetas v2",
                document_version="1",
                document_type="guide",
                product="movilidad",
                source_pdf_path="data/raw/MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                source_pdf_relative_path="MOVILIDAD/BICICLETAS Y PATINETAS/pv.pdf",
                cleaned_markdown_output_path="data/processed/pv.cleaned.md",
                text="DEDUCIBLE. Bicis: Entre $600.000 y $3.000.000. SMLMV.",
                chunk_index=8,
                chunk_schema_version="v2",
                section="DEDUCIBLE",
                section_path=["pv bicis y patinetas v2", "DEDUCIBLE"],
            ),
        ),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Cuál es el deducible del seguro de bicicletas y patinetas?",
            top_k=2,
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].section == "DEDUCIBLE"
    assert result.chunks[0].chunk_id == "pv:v2:0008"


def test_retrieve_ranked_chunks_expands_candidate_pool_and_reranks_comparison_hits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            SimpleNamespace(
                payload={
                    "chunk_id": "faq:v2:0000",
                    "source_pdf_id": "faq",
                    "source_pdf_relative_path": "MOVILIDAD/AUTOS/faq.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 0,
                    "text": "Plan Autos Básico Pérdidas Totales frente a Autos Global y Clásico.",
                    "document_name": "Seguro Plan Autos Básico Pérdidas Totales",
                    "document_version": "2",
                    "document_type": "faq",
                    "product": "auto",
                    "section": "Comparación comercial",
                    "section_path": [
                        "Seguro Plan Autos Básico Pérdidas Totales",
                        "Comparación comercial",
                    ],
                },
                score=0.92,
            ),
            SimpleNamespace(
                payload={
                    "chunk_id": "diff:v2:0000",
                    "source_pdf_id": "diff",
                    "source_pdf_relative_path": "MOVILIDAD/AUTOS/diferenciales.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 0,
                    "text": (
                        "Plan Autos Global, Plan Autos Clásico, franquicia, "
                        "nuevo de nuevo y pequeños eventos."
                    ),
                    "document_name": "DIFERENCIALES SURA",
                    "document_version": None,
                    "document_type": "guide",
                    "product": "auto",
                    "section": "Plan Autos Global",
                    "section_path": ["DIFERENCIALES SURA", "Plan Autos Global"],
                },
                score=0.78,
            ),
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=[
                        "diferenciales sura",
                        "plan autos global",
                        "plan autos clásico",
                        "franquicia",
                        "nuevo de nuevo",
                        "pequeños eventos",
                    ],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Qué diferencias hay entre el plan básico y los otros planes de autos?",
            top_k=2,
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert client.last_query["limit"] == 6
    assert result.chunks[0].document_name == "DIFERENCIALES SURA"
    assert result.chunks[0].score > result.chunks[1].score


def test_retrieve_ranked_chunks_adds_local_lexical_candidates_for_comparison_queries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient(
        [
            SimpleNamespace(
                payload={
                    "chunk_id": "faq:v2:0000",
                    "source_pdf_id": "faq",
                    "source_pdf_relative_path": "MOVILIDAD/AUTOS/faq.pdf",
                    "chunk_schema_version": "v2",
                    "chunk_index": 0,
                    "text": "El plan básico se diferencia de otros planes en pérdidas totales.",
                    "document_name": "Seguro Plan Autos Básico Pérdidas Totales",
                    "document_version": "2",
                    "document_type": "faq",
                    "product": "auto",
                    "section": "Comparación comercial",
                    "section_path": [
                        "Seguro Plan Autos Básico Pérdidas Totales",
                        "Comparación comercial",
                    ],
                },
                score=0.92,
            ),
        ]
    )

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=[
                        "diferenciales sura",
                        "plan autos global",
                        "plan autos clásico",
                        "franquicia",
                        "nuevo de nuevo",
                        "pequeños eventos",
                    ],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (
            ChunkRecord(
                chunk_id="diff:v2:0000",
                source_pdf_id="diff",
                document_name="DIFERENCIALES SURA",
                document_version=None,
                document_type="guide",
                product="auto",
                source_pdf_path="data/raw/MOVILIDAD/AUTOS/diferenciales.pdf",
                source_pdf_relative_path="MOVILIDAD/AUTOS/diferenciales.pdf",
                cleaned_markdown_output_path="data/processed/diff.cleaned.md",
                text=(
                    "Plan Autos Global. Plan Autos Clásico. Franquicia. "
                    "Nuevo de nuevo. Pequeños eventos."
                ),
                chunk_index=0,
                chunk_schema_version="v2",
                section="Plan Autos Global",
                section_path=["DIFERENCIALES SURA", "Plan Autos Global"],
            ),
        ),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Qué diferencias hay entre el plan básico y los otros planes de autos?",
            top_k=2,
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].document_name == "DIFERENCIALES SURA"
    assert result.chunks[0].chunk_id == "diff:v2:0000"


def test_retrieve_ranked_chunks_skips_local_lexical_candidates_without_matching_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=["diferenciales sura", "plan autos global"],
                )
            ]
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (
            ChunkRecord(
                chunk_id="diff:v2:0000",
                source_pdf_id="diff",
                document_name="DIFERENCIALES SURA",
                document_version=None,
                document_type="guide",
                product="health",
                source_pdf_path="data/raw/autonomia/vida/diff.pdf",
                source_pdf_relative_path="AUTONOMIA/VIDA/diff.pdf",
                cleaned_markdown_output_path="data/processed/diff.cleaned.md",
                text="Plan Autos Global.",
                chunk_index=0,
                chunk_schema_version="v2",
                section="Plan Autos Global",
                section_path=["DIFERENCIALES SURA", "Plan Autos Global"],
            ),
        ),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Qué diferencias hay entre el plan básico y los otros planes de autos?",
            top_k=2,
            filters={"product": "auto"},
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks == []


def test_retrieve_ranked_chunks_matches_missing_product_from_source_relative_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(
            filter_aliases={"product": {"auto": ["autos", "carro"]}},
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["plan básico", "autos"],
                    any_of=["diferencias", "otros planes"],
                    append_terms=["diferenciales sura", "plan autos global"],
                )
            ],
        ),
    )
    monkeypatch.setattr(
        "rag.ingestion.load_local_chunk_corpus",
        lambda chunk_dir="data/processed/chunks": (
            ChunkRecord(
                chunk_id="diff:v2:0000",
                source_pdf_id="diff",
                document_name="DIFERENCIALES SURA",
                document_version=None,
                document_type="guide",
                product=None,
                source_pdf_path="data/raw/MOVILIDAD/AUTOS/diferenciales.pdf",
                source_pdf_relative_path="MOVILIDAD/AUTOS/diferenciales.pdf",
                cleaned_markdown_output_path="data/processed/diff.cleaned.md",
                text="Plan Autos Global. Franquicia.",
                chunk_index=0,
                chunk_schema_version="v2",
                section="Plan Autos Global",
                section_path=["DIFERENCIALES SURA", "Plan Autos Global"],
            ),
        ),
    )

    result = retrieve_ranked_chunks(
        RetrievalQuery(
            query="¿Qué diferencias hay entre el plan básico y los otros planes de autos?",
            top_k=2,
            filters={"product": "auto"},
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    assert result.chunks[0].chunk_id == "diff:v2:0000"


def test_retrieve_ranked_chunks_applies_operator_term_equivalences_to_filters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = FakeQdrantRetrievalClient([])

    monkeypatch.setattr("rag.ingestion.qdrant_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.generate_embedding_vector",
        lambda text, settings: [0.1, 0.2],
    )
    monkeypatch.setattr("rag.ingestion.get_qdrant_models", fake_qdrant_models)
    monkeypatch.setattr(
        "rag.ingestion.load_term_equivalences",
        lambda: TermEquivalenceSet(filter_aliases={"product": {"auto": ["carro", "vehículo"]}}),
    )

    retrieve_ranked_chunks(
        RetrievalQuery(
            query="coverage",
            filters={"product": "vehículo"},
        ),
        settings=Settings(
            _env_file=None,
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        client=client,
    )

    query_filter = client.last_query["query_filter"]
    assert len(query_filter.must) == 1
    assert query_filter.must[0].key == "product"
    assert query_filter.must[0].match.value == "auto"


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
