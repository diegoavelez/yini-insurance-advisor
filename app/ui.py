"""Thin Gradio UI over the grounded QA pipeline."""

from __future__ import annotations

import importlib
import importlib.util
import logging

from contracts import Citation, GroundedAnswerResult, RetrievalQuery
from core.config import Settings, get_settings, validate_startup_settings
from core.logging import configure_logging
from ops.observability import (
    generate_request_id,
    log_event,
    log_health_status,
    log_startup_diagnostics,
    maybe_activate_phoenix,
)
from rag.ingestion import (
    embedding_backend_is_available,
    generate_grounded_answer,
    groq_backend_is_available,
    qdrant_backend_is_available,
    validate_embedding_settings,
)

APP_TITLE = "Yini"
APP_DESCRIPTION = (
    "Grounded insurance document assistant for advisor review. Answers are drafts and "
    "must remain tied to cited evidence."
)
DEFAULT_ERROR_MESSAGE = "Unable to process the query right now."
UI_LOGGER = logging.getLogger("yini.ui")
APP_LOGGER = logging.getLogger("yini.app")


def format_citations(citations: list[Citation]) -> str:
    """Render citations into a stable markdown block for the MVP UI."""

    if not citations:
        return "No citations available."

    lines: list[str] = []
    for citation in citations:
        parts = [citation.document_name]
        if citation.section:
            parts.append(f"section: {citation.section}")
        if citation.page is not None:
            parts.append(f"page: {citation.page}")
        if citation.clause_id:
            parts.append(f"clause: {citation.clause_id}")
        if citation.chunk_id:
            parts.append(f"chunk: {citation.chunk_id}")
        line = "- " + " | ".join(parts)
        if citation.quote:
            line += f"\n  > {citation.quote}"
        lines.append(line)
    return "\n".join(lines)


def format_limitations(limitations: list[str]) -> str:
    """Render limitations into a stable markdown block for the MVP UI."""

    if not limitations:
        return "No additional limitations noted."
    return "\n".join(f"- {limitation}" for limitation in limitations)


def build_retrieval_query(query: str, settings: Settings) -> RetrievalQuery:
    """Build the typed retrieval query used by the UI backend seam."""

    return RetrievalQuery(query=query, top_k=settings.top_k)


def run_query(
    query: str,
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
) -> tuple[str, str, str, str, str]:
    """Execute one grounded QA request for the UI."""

    request_id = generate_request_id("ui")
    normalized_query = query.strip()
    if not normalized_query:
        log_event(
            UI_LOGGER,
            event_type="request_failed",
            request_id=request_id,
            level=logging.ERROR,
            runtime_surface="gradio_ui",
            error_type="ValidationError",
            error_message="Please enter a question.",
        )
        return "", "", "", "", "Please enter a question."

    resolved_settings = validate_startup_settings(
        settings or get_settings(),
        require_groq=True,
        require_qdrant=True,
    )
    retrieval_query = build_retrieval_query(normalized_query, resolved_settings)
    log_event(
        UI_LOGGER,
        event_type="request_started",
        request_id=request_id,
        runtime_surface="gradio_ui",
        query_length=len(normalized_query),
        top_k=retrieval_query.top_k,
    )

    try:
        result = grounded_answer_fn(
            retrieval_query,
            settings=resolved_settings,
            request_id=request_id,
        )
    except Exception as exc:
        log_event(
            UI_LOGGER,
            event_type="request_failed",
            request_id=request_id,
            level=logging.ERROR,
            runtime_surface="gradio_ui",
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        return "", "", "", "", f"{DEFAULT_ERROR_MESSAGE} Error: {exc}"

    log_event(
        UI_LOGGER,
        event_type="request_succeeded",
        request_id=request_id,
        runtime_surface="gradio_ui",
        confidence=result.response.confidence,
        citation_count=len(result.response.citations),
        limitation_count=len(result.response.limitations),
    )
    return render_grounded_result(result)


def render_grounded_result(result: GroundedAnswerResult) -> tuple[str, str, str, str, str]:
    """Render the typed grounded result into UI output fields."""

    response = result.response
    answer = response.suggested_answer
    citations = format_citations(response.citations)
    confidence = response.confidence.upper()
    limitations = format_limitations(response.limitations)
    status = response.advisor_review_notice
    return answer, citations, confidence, limitations, status


def build_query_handler(
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
):
    """Return the UI handler bound to the current runtime settings."""

    def handle_query(query: str) -> tuple[str, str, str, str, str]:
        return run_query(
            query,
            settings=settings,
            grounded_answer_fn=grounded_answer_fn,
        )

    return handle_query


def build_gradio_app(
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
    gradio_module=None,
):
    """Build the MVP Gradio query UI."""

    gr = gradio_module or importlib.import_module("gradio")
    handler = build_query_handler(
        settings=settings,
        grounded_answer_fn=grounded_answer_fn,
    )
    return gr.Interface(
        fn=handler,
        inputs=gr.Textbox(
            label="Advisor Question",
            lines=3,
            placeholder="Ask about coverage, exclusions, procedures, or requirements.",
        ),
        outputs=[
            gr.Markdown(label="Suggested Answer"),
            gr.Markdown(label="Citations"),
            gr.Textbox(label="Confidence"),
            gr.Markdown(label="Limitations"),
            gr.Textbox(label="Status"),
        ],
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        flagging_mode="never",
    )


def gradio_backend_is_available() -> bool:
    """Return whether Gradio is importable in the current runtime."""

    return importlib.util.find_spec("gradio") is not None


def build_readiness_status(
    settings: Settings,
    *,
    runtime_surface: str,
    gradio_available: bool | None = None,
    groq_available: bool | None = None,
    qdrant_available: bool | None = None,
    embedding_available: bool | None = None,
) -> dict[str, object]:
    """Build the narrow readiness payload for the current MVP runtime path."""

    validated_settings = validate_startup_settings(
        settings,
        require_groq=True,
        require_qdrant=True,
    )
    validate_embedding_settings(validated_settings)

    if gradio_available is None:
        gradio_available = gradio_backend_is_available()
    if groq_available is None:
        groq_available = groq_backend_is_available()
    if qdrant_available is None:
        qdrant_available = qdrant_backend_is_available()
    if embedding_available is None:
        embedding_available = embedding_backend_is_available(validated_settings)

    missing_dependencies: list[str] = []
    if not gradio_available:
        missing_dependencies.append("gradio")
    if not groq_available:
        missing_dependencies.append("groq")
    if not qdrant_available:
        missing_dependencies.append("qdrant-client")
    if not embedding_available:
        missing_dependencies.append("sentence-transformers")

    if missing_dependencies:
        raise RuntimeError(
            "Hosted readiness failed because required runtime dependencies are unavailable: "
            + ", ".join(missing_dependencies)
            + "."
        )

    return {
        "event_type": "readiness_check_succeeded",
        "runtime_surface": runtime_surface,
        "status": "ready",
        "dependency_checks": {
            "gradio": gradio_available,
            "groq": groq_available,
            "qdrant": qdrant_available,
            "embedding_backend": embedding_available,
        },
    }


def log_readiness_status(
    logger: logging.Logger,
    settings: Settings,
    *,
    runtime_surface: str,
    gradio_available: bool | None = None,
    groq_available: bool | None = None,
    qdrant_available: bool | None = None,
    embedding_available: bool | None = None,
) -> dict[str, object]:
    """Emit readiness status for the MVP runtime path."""

    try:
        payload = build_readiness_status(
            settings,
            runtime_surface=runtime_surface,
            gradio_available=gradio_available,
            groq_available=groq_available,
            qdrant_available=qdrant_available,
            embedding_available=embedding_available,
        )
    except Exception as exc:
        payload = {
            "event_type": "readiness_check_failed",
            "runtime_surface": runtime_surface,
            "status": "not_ready",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        logger.error("Readiness check failed", extra=payload)
        raise

    logger.info("Readiness check succeeded", extra=payload)
    return payload


def main(*, launch: bool = True) -> int:
    """Start the MVP Gradio app entrypoint."""

    settings = validate_startup_settings(get_settings())
    configure_logging(settings.log_level)

    log_startup_diagnostics(APP_LOGGER, settings, runtime_surface="gradio_ui")
    log_health_status(APP_LOGGER, runtime_surface="gradio_ui")
    log_readiness_status(APP_LOGGER, settings, runtime_surface="gradio_ui")
    maybe_activate_phoenix(APP_LOGGER, settings, runtime_surface="gradio_ui")
    app = build_gradio_app(settings=settings)
    if launch:
        app.launch()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
