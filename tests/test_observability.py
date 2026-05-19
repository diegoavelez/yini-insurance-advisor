from __future__ import annotations

import logging

import pytest

import app.ui as app_ui
import rag.ingestion as rag_ingestion
from contracts import (
    AdvisorDraftResponse,
    DocumentRetrievalResult,
    GroundedAnswerResult,
    GroundingVerification,
    RetrievalQuery,
    RetrievedChunk,
)
from core.config import Settings, clear_settings_cache
from ops.observability import build_startup_diagnostics, generate_request_id


@pytest.fixture(autouse=True)
def reset_settings_cache() -> None:
    clear_settings_cache()
    yield
    clear_settings_cache()


def make_settings() -> Settings:
    return Settings(
        _env_file=None,
        groq_api_key="test-groq-key",
        qdrant_url="https://qdrant.example.com",
        qdrant_api_key="test-qdrant-key",
        app_env="test",
    )


def make_retrieved_chunk() -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="chunk-v2-0",
        source_pdf_id="policy-1",
        chunk_schema_version="v2",
        chunk_index=0,
        text="Coverage applies after the waiting period.",
        document_name="Policy A",
        document_version="2026",
        page=3,
        section="Coverage",
        section_path=["Coverage"],
        clause_id="COV-1",
        score=0.92,
    )


def make_grounded_result() -> GroundedAnswerResult:
    return GroundedAnswerResult(
        query="What is covered?",
        response=AdvisorDraftResponse(
            suggested_answer="Coverage applies after the waiting period.",
            documentary_basis=[],
            citations=[],
            confidence="high",
            limitations=[],
            advisor_review_notice="Advisor review required before external use.",
        ),
        verification=GroundingVerification(
            supported=True,
            confidence="high",
            unsupported_claims=[],
            missing_citations=[],
        ),
    )


def test_generate_request_id_uses_expected_shape() -> None:
    request_id = generate_request_id("ui")

    assert request_id.startswith("ui-")
    assert len(request_id) == 15


def test_build_startup_diagnostics_excludes_secrets() -> None:
    payload = build_startup_diagnostics(make_settings(), runtime_surface="gradio_ui")

    assert payload["event_type"] == "startup_diagnostics"
    assert payload["runtime_surface"] == "gradio_ui"
    assert payload["groq_model"] == "gpt-oss-120b"
    assert "groq_api_key" not in payload
    assert "qdrant_api_key" not in payload


def test_ui_run_query_emits_correlated_success_events(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    answer, _citations, confidence, _limitations, _status = app_ui.run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=lambda *_args, **_kwargs: make_grounded_result(),
    )

    assert "Coverage applies" in answer
    assert confidence == "HIGH"
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "request_started" in event_types
    assert "request_succeeded" in event_types
    request_ids = {
        record.request_id for record in caplog.records if getattr(record, "event_type", None)
    }
    assert len(request_ids) == 1


def test_ui_run_query_emits_correlated_failure_event(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    app_ui.run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )

    failure_records = [
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "request_failed"
    ]
    assert len(failure_records) == 1
    assert failure_records[0].error_message == "boom"


def test_ui_blank_query_emits_correlated_failure_event(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    answer, citations, confidence, limitations, status = app_ui.run_query(
        "   ",
        settings=make_settings(),
    )

    assert (answer, citations, confidence, limitations) == ("", "", "", "")
    assert status == "Please enter a question."
    failure_records = [
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "request_failed"
    ]
    assert len(failure_records) == 1
    assert failure_records[0].request_id.startswith("ui-")
    assert failure_records[0].error_message == "Please enter a question."


def test_retrieve_ranked_chunks_emits_correlated_events(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    settings = make_settings()
    chunk = make_retrieved_chunk()

    monkeypatch.setattr(rag_ingestion, "ensure_qdrant_backend_available", lambda: None)
    monkeypatch.setattr(rag_ingestion, "create_qdrant_client", lambda _settings: object())
    monkeypatch.setattr(
        rag_ingestion,
        "generate_embedding_vector",
        lambda _query, _settings: [0.1, 0.2],
    )
    monkeypatch.setattr(rag_ingestion, "search_qdrant_chunks", lambda **_kwargs: [object()])
    monkeypatch.setattr(rag_ingestion, "map_search_hit_to_retrieved_chunk", lambda _hit: chunk)

    result = rag_ingestion.retrieve_ranked_chunks(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=settings,
        request_id="req-123456789012",
    )

    assert result == DocumentRetrievalResult(chunks=[chunk])
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "retrieval_execution_started" in event_types
    assert "retrieval_execution_succeeded" in event_types
    success_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "retrieval_execution_succeeded"
    )
    assert success_record.request_id == "req-123456789012"
    assert success_record.result_count == 1


def test_generate_grounded_answer_emits_correlated_events(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    settings = make_settings()
    retrieval_result = DocumentRetrievalResult(
        chunks=[make_retrieved_chunk(), make_retrieved_chunk()]
    )

    monkeypatch.setattr(rag_ingestion, "ensure_groq_backend_available", lambda: None)

    result = rag_ingestion.generate_grounded_answer(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=settings,
        retrieval_result=retrieval_result,
        completion_generator=(
            lambda _prompt, _settings: "Coverage applies after the waiting period."
        ),
        request_id="req-123456789012",
    )

    assert "Coverage applies" in result.response.suggested_answer
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "grounded_answer_execution_started" in event_types
    assert "grounded_answer_execution_succeeded" in event_types
    success_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "grounded_answer_execution_succeeded"
    )
    assert success_record.request_id == "req-123456789012"
    assert success_record.confidence == "high"


def test_cli_main_emits_correlated_execution_events(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(rag_ingestion, "configure_logging", lambda _level: None)
    monkeypatch.setattr(rag_ingestion, "get_settings", make_settings)
    monkeypatch.setattr(rag_ingestion, "run_retrieval", lambda args, request_id=None: 0)

    exit_code = rag_ingestion.main(["retrieve-chunks", "--query", "What is covered?"])

    assert exit_code == 0
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "startup_diagnostics" in event_types
    assert "request_started" in event_types
    assert "request_succeeded" in event_types


def test_cli_main_non_zero_exit_emits_request_failed(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(rag_ingestion, "configure_logging", lambda _level: None)
    monkeypatch.setattr(rag_ingestion, "get_settings", make_settings)
    monkeypatch.setattr(rag_ingestion, "run_retrieval", lambda args, request_id=None: 1)

    exit_code = rag_ingestion.main(["retrieve-chunks", "--query", "What is covered?"])

    assert exit_code == 1
    failure_records = [
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "request_failed"
    ]
    assert len(failure_records) == 1
    assert failure_records[0].error_type == "CommandExit"
    assert failure_records[0].exit_code == 1


def test_execution_events_do_not_include_secrets(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)

    app_ui.run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=lambda *_args, **_kwargs: make_grounded_result(),
    )

    serialized_records = [record.__dict__ for record in caplog.records]
    assert all("groq_api_key" not in record for record in serialized_records)
    assert all("qdrant_api_key" not in record for record in serialized_records)
