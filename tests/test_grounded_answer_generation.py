from __future__ import annotations

import logging

import pytest

from contracts import (
    AdvisorDraftResponse,
    Citation,
    DocumentRetrievalResult,
    GroundedAnswerResult,
    RetrievalQuery,
    RetrievedChunk,
)
from core.config import Settings
from rag.ingestion import (
    build_grounded_prompt,
    build_parser,
    generate_grounded_answer,
    main,
)


def make_retrieval_result() -> DocumentRetrievalResult:
    return DocumentRetrievalResult(
        chunks=[
            RetrievedChunk(
                chunk_id="policy-a:v2:0000",
                source_pdf_id="policy-a",
                chunk_schema_version="v2",
                chunk_index=0,
                text="Coverage applies to outpatient care after deductible.",
                document_name="Policy A",
                document_version="2026-01",
                page=4,
                section="Coverage",
                section_path=["Policy A", "Coverage"],
                clause_id="1.2",
                score=0.91,
            ),
            RetrievedChunk(
                chunk_id="policy-a:v2:0001",
                source_pdf_id="policy-a",
                chunk_schema_version="v2",
                chunk_index=1,
                text="Exclusions include cosmetic surgery.",
                document_name="Policy A",
                document_version="2026-01",
                page=7,
                section="Exclusions",
                section_path=["Policy A", "Exclusions"],
                clause_id="3.1",
                score=0.84,
            ),
        ]
    )


def test_parser_builds_answer_query_command() -> None:
    args = build_parser().parse_args(["answer-query", "--query", "What is covered?"])

    assert args.command == "answer-query"
    assert args.query == "What is covered?"
    assert args.top_k is None


def test_build_grounded_prompt_is_deterministic() -> None:
    retrieval_result = make_retrieval_result()

    first_prompt = build_grounded_prompt(
        query="What is covered?",
        retrieved_chunks=retrieval_result.chunks,
    )
    second_prompt = build_grounded_prompt(
        query="What is covered?",
        retrieved_chunks=retrieval_result.chunks,
    )

    assert first_prompt == second_prompt
    assert "Chunk ID: policy-a:v2:0000" in first_prompt
    assert "Chunk ID: policy-a:v2:0001" in first_prompt


def test_generate_grounded_answer_fails_loudly_for_missing_groq_config() -> None:
    with pytest.raises(ValueError):
        generate_grounded_answer(
            RetrievalQuery(query="What is covered?"),
            settings=Settings(
                _env_file=None,
                groq_api_key=None,
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            retrieval_result=make_retrieval_result(),
        )


def test_generate_grounded_answer_returns_scope_refusal_without_backend_dependencies() -> None:
    result = generate_grounded_answer(
        RetrievalQuery(query="What is the weather in Bogota?"),
        settings=Settings(
            _env_file=None,
            groq_api_key=None,
            qdrant_url=None,
            qdrant_api_key=None,
        ),
    )

    assert result.response.confidence == "low"
    assert "cannot answer" in result.response.suggested_answer.lower()
    assert result.response.citations == []
    assert result.response.documentary_basis == []
    assert result.verification.supported is False


def test_generate_grounded_answer_returns_typed_response_with_citations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)

    result = generate_grounded_answer(
        RetrievalQuery(query="What is covered?"),
        settings=Settings(
            _env_file=None,
            groq_api_key="secret",
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        retrieval_result=make_retrieval_result(),
        completion_generator=(
            lambda prompt, settings: "Coverage applies to outpatient care after deductible."
        ),
    )

    assert isinstance(result, GroundedAnswerResult)
    assert isinstance(result.response, AdvisorDraftResponse)
    assert result.response.suggested_answer.startswith("Coverage applies")
    assert len(result.response.citations) == 2
    assert isinstance(result.response.citations[0], Citation)
    assert result.response.citations[0].document_name == "Policy A"
    assert result.response.citations[0].chunk_id == "policy-a:v2:0000"
    assert result.verification.confidence == "high"


def test_generate_grounded_answer_downgrades_answerable_response_without_citations(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.build_citations_from_chunks", lambda _chunks: [])
    caplog.set_level(logging.INFO)

    result = generate_grounded_answer(
        RetrievalQuery(query="What is covered?"),
        settings=Settings(
            _env_file=None,
            groq_api_key="secret",
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        retrieval_result=make_retrieval_result(),
        completion_generator=(
            lambda prompt, settings: "Coverage applies to outpatient care after deductible."
        ),
        request_id="rag-123456789012",
    )

    assert result.response.confidence == "low"
    assert result.response.citations == []
    assert "did not produce traceable citations" in result.response.suggested_answer.lower()
    assert result.verification.supported is False
    guardrail_event = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "citation_presence_guardrail_triggered"
    )
    assert guardrail_event.request_id == "rag-123456789012"
    assert guardrail_event.guardrail_surface == "grounded_answer_generation"


def test_generate_grounded_answer_returns_limited_response_for_empty_retrieval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)

    result = generate_grounded_answer(
        RetrievalQuery(query="What is covered?"),
        settings=Settings(
            _env_file=None,
            groq_api_key="secret",
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        retrieval_result=DocumentRetrievalResult(chunks=[]),
    )

    assert result.response.confidence == "low"
    assert "enough grounded evidence" in result.response.suggested_answer.lower()
    assert result.verification.supported is False


def test_generate_grounded_answer_returns_limited_response_for_weak_retrieval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)

    weak_retrieval = DocumentRetrievalResult(chunks=[make_retrieval_result().chunks[0]])

    result = generate_grounded_answer(
        RetrievalQuery(query="What is covered?"),
        settings=Settings(
            _env_file=None,
            groq_api_key="secret",
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
        ),
        retrieval_result=weak_retrieval,
    )

    assert result.response.confidence == "low"
    assert "too limited" in result.response.limitations[0].lower()
    assert result.response.citations[0].chunk_id == "policy-a:v2:0000"
    assert result.verification.supported is True


def test_generate_grounded_answer_surfaces_generation_failures(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)

    with pytest.raises(RuntimeError):
        generate_grounded_answer(
            RetrievalQuery(query="What is covered?"),
            settings=Settings(
                _env_file=None,
                groq_api_key="secret",
                qdrant_url="https://example.qdrant.io",
                qdrant_api_key="secret",
            ),
            retrieval_result=make_retrieval_result(),
            completion_generator=lambda prompt, settings: (_ for _ in ()).throw(
                RuntimeError("Groq request failed")
            ),
        )


def test_answer_query_cli_prints_typed_grounded_result(
    monkeypatch: pytest.MonkeyPatch,
    capsys,
) -> None:
    monkeypatch.setattr("rag.ingestion.groq_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.retrieve_ranked_chunks",
        lambda query, settings=None: make_retrieval_result(),
    )
    monkeypatch.setattr(
        "rag.ingestion.generate_grounded_completion",
        lambda prompt, settings: "Coverage applies to outpatient care after deductible.",
    )
    monkeypatch.setattr(
        "rag.ingestion.get_settings",
        lambda: Settings(
            _env_file=None,
            groq_api_key="secret",
            qdrant_url="https://example.qdrant.io",
            qdrant_api_key="secret",
            top_k=7,
        ),
    )

    exit_code = main(["answer-query", "--query", "What is covered?"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert (
        '"suggested_answer": "Coverage applies to outpatient care after deductible."'
        in captured.out
    )
