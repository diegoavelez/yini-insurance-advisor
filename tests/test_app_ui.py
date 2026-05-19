from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.ui import (
    APP_DESCRIPTION,
    APP_TITLE,
    build_gradio_app,
    format_citations,
    format_limitations,
    render_grounded_result,
    run_query,
)
from contracts import AdvisorDraftResponse, Citation, GroundedAnswerResult, GroundingVerification
from core.config import Settings, clear_settings_cache


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


def make_grounded_result(
    *,
    answer: str = "Coverage applies when the waiting period has already passed.",
    confidence: str = "high",
    limitations: list[str] | None = None,
) -> GroundedAnswerResult:
    return GroundedAnswerResult(
        query="What is covered?",
        response=AdvisorDraftResponse(
            suggested_answer=answer,
            documentary_basis=[],
            citations=[
                Citation(
                    document_name="Auto Policy",
                    section="Coverage",
                    page=3,
                    clause_id="COV-1",
                    chunk_id="chunk-001",
                    quote="Coverage applies after the waiting period.",
                )
            ],
            confidence=confidence,  # type: ignore[arg-type]
            limitations=limitations or ["Advisor review is still required."],
            advisor_review_notice="Advisor review required before external use.",
        ),
        verification=GroundingVerification(
            supported=confidence != "low",
            confidence=confidence,  # type: ignore[arg-type]
            unsupported_claims=[],
            missing_citations=[],
        ),
    )


def test_format_citations_renders_traceable_markdown() -> None:
    rendered = format_citations(
        [
            Citation(
                document_name="Policy A",
                section="Eligibility",
                page=2,
                clause_id="ELIG-2",
                chunk_id="chunk-v2-0",
                quote="Applicant must be over 18 years old.",
            )
        ]
    )

    assert "Policy A" in rendered
    assert "section: Eligibility" in rendered
    assert "page: 2" in rendered
    assert "clause: ELIG-2" in rendered
    assert "chunk: chunk-v2-0" in rendered
    assert "Applicant must be over 18 years old." in rendered


def test_format_limitations_handles_empty_and_non_empty_lists() -> None:
    assert format_limitations([]) == "No additional limitations noted."
    assert format_limitations(["First", "Second"]) == "- First\n- Second"


def test_render_grounded_result_maps_typed_response_fields() -> None:
    answer, citations, confidence, limitations, status = render_grounded_result(
        make_grounded_result()
    )

    assert "Coverage applies" in answer
    assert "Auto Policy" in citations
    assert confidence == "HIGH"
    assert "Advisor review is still required." in limitations
    assert status == "Advisor review required before external use."


def test_run_query_returns_successful_grounded_output() -> None:
    def grounded_answer_fn(*_args, **_kwargs):
        return make_grounded_result()

    answer, citations, confidence, limitations, status = run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=grounded_answer_fn,
    )

    assert "Coverage applies" in answer
    assert "Auto Policy" in citations
    assert confidence == "HIGH"
    assert "Advisor review is still required." in limitations
    assert status == "Advisor review required before external use."


def test_run_query_returns_blank_query_error_without_backend_call() -> None:
    called = False

    def grounded_answer_fn(*_args, **_kwargs):
        nonlocal called
        called = True
        return make_grounded_result()

    answer, citations, confidence, limitations, status = run_query(
        "   ",
        settings=make_settings(),
        grounded_answer_fn=grounded_answer_fn,
    )

    assert (answer, citations, confidence, limitations) == ("", "", "", "")
    assert status == "Please enter a question."
    assert called is False


def test_run_query_distinguishes_insufficient_evidence_from_runtime_failure() -> None:
    def insufficient_answer_fn(*_args, **_kwargs):
        return make_grounded_result(
            answer=(
                "I do not have enough grounded evidence in the retrieved documents "
                "to answer this confidently."
            ),
            confidence="low",
            limitations=["Retrieved evidence is insufficient for a strong grounded answer."],
        )

    answer, citations, confidence, limitations, status = run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=insufficient_answer_fn,
    )

    assert "do not have enough grounded evidence" in answer
    assert confidence == "LOW"
    assert "insufficient" in limitations.lower()
    assert "Error:" not in status


def test_run_query_surfaces_runtime_failures_as_explicit_errors() -> None:
    def failing_grounded_answer_fn(*_args, **_kwargs):
        raise RuntimeError("backend offline")

    answer, citations, confidence, limitations, status = run_query(
        "What is covered?",
        settings=make_settings(),
        grounded_answer_fn=failing_grounded_answer_fn,
    )

    assert (answer, citations, confidence, limitations) == ("", "", "", "")
    assert "Unable to process the query right now." in status
    assert "backend offline" in status


@dataclass
class FakeComponent:
    kind: str
    kwargs: dict


class FakeInterface:
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

    def launch(self) -> None:
        self.launched = True


class FakeGradioModule:
    def Textbox(self, **kwargs):
        return FakeComponent("Textbox", kwargs)

    def Markdown(self, **kwargs):
        return FakeComponent("Markdown", kwargs)

    def Interface(self, **kwargs):
        return FakeInterface(**kwargs)


def test_build_gradio_app_creates_expected_interface_contract() -> None:
    app = build_gradio_app(
        settings=make_settings(),
        grounded_answer_fn=lambda *_args, **_kwargs: make_grounded_result(),
        gradio_module=FakeGradioModule(),
    )

    assert app.kwargs["title"] == APP_TITLE
    assert app.kwargs["description"] == APP_DESCRIPTION
    assert app.kwargs["inputs"].kind == "Textbox"
    assert len(app.kwargs["outputs"]) == 5
    assert app.kwargs["flagging_mode"] == "never"

    handler = app.kwargs["fn"]
    answer, citations, confidence, limitations, status = handler("What is covered?")
    assert "Coverage applies" in answer
    assert "Auto Policy" in citations
    assert confidence == "HIGH"
    assert "Advisor review is still required." in limitations
    assert status == "Advisor review required before external use."
