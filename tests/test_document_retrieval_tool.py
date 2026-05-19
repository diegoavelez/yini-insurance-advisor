from __future__ import annotations

import importlib
import logging

import pytest

from agents.document_retrieval_tool import (
    classify_tool_error,
    document_retrieval_tool,
    unwrap_retrieval_tool_result,
)
from contracts import (
    DocumentRetrievalResult,
    DocumentRetrievalToolResult,
    RetrievalQuery,
    RetrievedChunk,
    ToolError,
)
from core.config import Settings

retrieval_tool_module = importlib.import_module("agents.document_retrieval_tool")


def make_settings() -> Settings:
    return Settings(
        _env_file=None,
        groq_api_key="test-groq-key",
        qdrant_url="https://qdrant.example.com",
        qdrant_api_key="test-qdrant-key",
        app_env="test",
    )


def make_retrieval_result() -> DocumentRetrievalResult:
    return DocumentRetrievalResult(
        chunks=[
            RetrievedChunk(
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
        ]
    )


def test_document_retrieval_tool_returns_typed_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        retrieval_tool_module,
        "retrieve_ranked_chunks",
        lambda *args, **kwargs: make_retrieval_result(),
    )

    tool_result = document_retrieval_tool(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=make_settings(),
    )

    assert tool_result.ok is True
    assert tool_result.error is None
    assert tool_result.result == make_retrieval_result()


def test_document_retrieval_tool_treats_empty_results_as_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        retrieval_tool_module,
        "retrieve_ranked_chunks",
        lambda *args, **kwargs: DocumentRetrievalResult(chunks=[]),
    )

    tool_result = document_retrieval_tool(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=make_settings(),
    )

    assert tool_result.ok is True
    assert tool_result.result == DocumentRetrievalResult(chunks=[])
    assert tool_result.error is None


@pytest.mark.parametrize(
    ("exception", "expected_kind"),
    [
        (
            ValueError("QDRANT_URL is required when Qdrant usage is enabled."),
            "configuration_failure",
        ),
        (
            RuntimeError(
                "qdrant-client is not installed. Install project dependencies before "
                "running Qdrant indexing."
            ),
            "dependency_failure",
        ),
        (RuntimeError("Qdrant search failed."), "backend_failure"),
    ],
)
def test_document_retrieval_tool_returns_typed_failure(
    monkeypatch: pytest.MonkeyPatch,
    exception: Exception,
    expected_kind: str,
) -> None:
    def raise_error(*args, **kwargs):
        raise exception

    monkeypatch.setattr(retrieval_tool_module, "retrieve_ranked_chunks", raise_error)

    tool_result = document_retrieval_tool(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=make_settings(),
    )

    assert tool_result.ok is False
    assert tool_result.result is None
    assert tool_result.error is not None
    assert tool_result.error.kind == expected_kind
    assert tool_result.error.message == str(exception)


def test_document_retrieval_tool_preserves_request_correlation(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(
        retrieval_tool_module,
        "retrieve_ranked_chunks",
        lambda *args, **kwargs: DocumentRetrievalResult(chunks=[]),
    )

    document_retrieval_tool(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=make_settings(),
        request_id="tool-123456789012",
    )

    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "document_retrieval_tool_started" in event_types
    assert "document_retrieval_tool_succeeded" in event_types
    success_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "document_retrieval_tool_succeeded"
    )
    assert success_record.request_id == "tool-123456789012"
    assert success_record.duration_ms >= 0


def test_document_retrieval_tool_failure_remains_observable(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    def raise_error(*args, **kwargs):
        raise RuntimeError("Qdrant backend unavailable.")

    monkeypatch.setattr(retrieval_tool_module, "retrieve_ranked_chunks", raise_error)

    tool_result = document_retrieval_tool(
        RetrievalQuery(query="What is covered?", top_k=5),
        settings=make_settings(),
        request_id="tool-123456789012",
    )

    assert tool_result.ok is False
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "document_retrieval_tool_started" in event_types
    assert "document_retrieval_tool_failed" in event_types
    failure_record = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "document_retrieval_tool_failed"
    )
    assert failure_record.request_id == "tool-123456789012"
    assert failure_record.error_message == "Qdrant backend unavailable."


def test_classify_tool_error_distinguishes_runtime_availability_failure() -> None:
    tool_error = classify_tool_error(RuntimeError("Embedding backend unavailable."))

    assert tool_error.kind == "dependency_failure"
    assert tool_error.message == "Embedding backend unavailable."


def test_unwrap_retrieval_tool_result_raises_on_typed_failure() -> None:
    with pytest.raises(RuntimeError, match="Typed backend failure."):
        unwrap_retrieval_tool_result(
            DocumentRetrievalToolResult(
                ok=False,
                error=ToolError(kind="backend_failure", message="Typed backend failure."),
            )
        )
