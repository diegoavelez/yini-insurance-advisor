"""Thin Gradio UI over the grounded QA pipeline."""

from __future__ import annotations

import importlib
import importlib.util
import logging
import re

from contracts import Citation, GroundedAnswerResult, RetrievalQuery
from core.config import Settings, get_settings, validate_startup_settings
from core.logging import configure_logging
from core.prompt_guardrails import detect_prompt_injection_signals
from core.query_scope import classify_query_scope
from ops.observability import (
    generate_request_id,
    log_event,
    log_health_status,
    log_startup_diagnostics,
    maybe_activate_phoenix,
)
from rag.ingestion import (
    build_prompt_injection_refusal_response,
    build_unsupported_query_response,
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
DEFAULT_LOADING_MESSAGE = "Generating draft answer..."
UI_LOGGER = logging.getLogger("yini.ui")
APP_LOGGER = logging.getLogger("yini.app")
SAFE_TRACE_ITEM_PATTERN = re.compile(r"^[a-z0-9_:-]{1,40}$")


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


def format_trace_summary(result: GroundedAnswerResult) -> str:
    """Render a concise review-oriented trace summary for the current result."""

    explicit_trace = getattr(result, "trace_summary", None)
    if isinstance(explicit_trace, list) and explicit_trace:
        sanitized_items = sanitize_trace_items(explicit_trace)
        if sanitized_items:
            return " → ".join(sanitized_items)

    response = result.response
    verification = result.verification
    steps = ["query_received", "grounded_answer_drafted"]
    if response.citations:
        steps.append(f"citations:{len(response.citations)}")
    else:
        steps.append("citations:0")
    steps.append(f"confidence:{response.confidence}")
    steps.append("grounding:supported" if verification.supported else "grounding:limited")
    return " → ".join(steps)


def sanitize_trace_items(items: list[object]) -> list[str]:
    """Keep only concise public-safe trace items for the demo UI."""

    sanitized: list[str] = []
    for item in items[:5]:
        normalized = str(item).strip().lower()
        if SAFE_TRACE_ITEM_PATTERN.fullmatch(normalized):
            sanitized.append(normalized)
        else:
            sanitized.append("internal_step_redacted")
    if sanitized and all(item == "internal_step_redacted" for item in sanitized):
        return []
    return sanitized


def infer_support_outcome(result: GroundedAnswerResult) -> str:
    """Infer a concise support outcome label from the current grounded result."""

    answer = result.response.suggested_answer.lower()
    limitations = [limitation.lower() for limitation in result.response.limitations]

    if any("prompt-injection guardrail" in limitation for limitation in limitations):
        return "prompt_guardrail_refusal"
    if any(
        "outside the supported insurance-document scope" in limitation
        for limitation in limitations
    ):
        return "unsupported_scope_refusal"
    if "do not have enough grounded evidence" in answer:
        return "limited_evidence_draft"
    if result.verification.supported:
        return "grounded_draft_ready"
    return "review_required_draft"


def format_support_context(
    result: GroundedAnswerResult,
    *,
    request_id: str,
    runtime_surface: str,
) -> str:
    """Render concise demo-safe support context for the current request."""

    outcome = infer_support_outcome(result)
    return "\n".join(
        [
            f"- Request ID: {request_id}",
            f"- Runtime Surface: {runtime_surface}",
            f"- Support Outcome: {outcome}",
            "- Follow-up: share the request ID when asking for support review.",
        ]
    )


def format_debug_metadata(
    result: GroundedAnswerResult,
    *,
    request_id: str,
    runtime_surface: str,
    query_length: int,
    top_k: int | None,
) -> str:
    """Render compact operator-facing debug metadata for the current request."""

    response = result.response
    return "\n".join(
        [
            f"- Request ID: {request_id}",
            f"- Runtime Surface: {runtime_surface}",
            f"- Query Length: {query_length}",
            f"- Retrieval Top K: {top_k if top_k is not None else 'n/a'}",
            f"- Confidence Level: {response.confidence}",
            f"- Citation Count: {len(response.citations)}",
            f"- Limitation Count: {len(response.limitations)}",
            f"- Debug Outcome: {infer_support_outcome(result)}",
        ]
    )


def format_loading_state(*, is_loading: bool) -> str:
    """Render concise loading-state feedback for the current demo UI."""

    if is_loading:
        return DEFAULT_LOADING_MESSAGE
    return "Draft answer ready for review."


def format_error_state(
    *,
    error_kind: str | None,
    detail: str | None = None,
) -> str:
    """Render a concise user-visible error-state message."""

    if error_kind is None:
        return "No active errors."
    if error_kind == "input":
        return f"Input Error — {detail or 'Please review the question and try again.'}"
    if error_kind == "runtime":
        return (
            "Runtime Error — "
            + (detail or "The request could not be processed right now.")
        )
    return detail or "Unknown error state."


def format_readiness_state(*, status: str, detail: str | None = None) -> str:
    """Render concise demo-safe readiness messaging for the public UI."""

    if status == "ready":
        return "Service Readiness — Ready for grounded draft generation."
    if status == "degraded":
        return (
            "Service Readiness — Degraded. "
            + (
                detail
                or (
                    "Required runtime dependencies are unavailable. "
                    "Draft generation may not work until the service is restored."
                )
            )
        )
    return detail or "Service Readiness — Unknown."


def format_answer_quality_state(result: GroundedAnswerResult) -> str:
    """Render concise user-visible messaging for degraded draft quality."""

    response = result.response
    answer = response.suggested_answer.lower()
    limitations = [limitation.lower() for limitation in response.limitations]
    degraded = (
        response.confidence == "low"
        or not result.verification.supported
        or "do not have enough grounded evidence" in answer
        or any("insufficient" in limitation for limitation in limitations)
    )
    if degraded:
        return (
            "Answer Quality — Degraded. This draft has lower confidence or limited "
            "grounded support and requires extra advisor review."
        )
    return "Answer Quality — Standard draft quality."


def build_demo_readiness_message(
    settings: Settings,
    *,
    readiness_status_builder=None,
) -> str:
    """Build the user-visible readiness message for the current demo UI."""

    builder = readiness_status_builder or build_readiness_status
    try:
        builder(settings, runtime_surface="gradio_ui")
    except Exception as exc:
        return format_readiness_state(
            status="degraded",
            detail=str(exc),
        )
    return format_readiness_state(status="ready")


def build_retrieval_query(query: str, settings: Settings) -> RetrievalQuery:
    """Build the typed retrieval query used by the UI backend seam."""

    return RetrievalQuery(query=query, top_k=settings.top_k)


def run_query(
    query: str,
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
) -> tuple[str, str, str, str, str, str, str, str, str, str]:
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
        return (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            format_error_state(error_kind="input", detail="Please enter a question."),
            "Please enter a question.",
        )

    resolved_settings = validate_startup_settings(
        settings or get_settings(),
        require_groq=True,
        require_qdrant=True,
    )
    injection_decision = detect_prompt_injection_signals(normalized_query)
    if injection_decision.triggered:
        log_event(
            UI_LOGGER,
            event_type="prompt_injection_guardrail_triggered",
            request_id=request_id,
            runtime_surface="gradio_ui",
            triggered_signals=injection_decision.signals,
            refusal_reason=injection_decision.reason,
        )
        return render_grounded_result(
            build_prompt_injection_refusal_response(query=normalized_query),
            request_id=request_id,
            runtime_surface="gradio_ui",
            query_length=len(normalized_query),
            top_k=None,
        )
    scope_decision = classify_query_scope(normalized_query)
    if scope_decision.scope == "unsupported":
        log_event(
            UI_LOGGER,
            event_type="query_scope_refusal",
            request_id=request_id,
            runtime_surface="gradio_ui",
            scope="unsupported",
            refusal_reason=scope_decision.reason,
        )
        return render_grounded_result(
            build_unsupported_query_response(query=normalized_query),
            request_id=request_id,
            runtime_surface="gradio_ui",
            query_length=len(normalized_query),
            top_k=None,
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
        return (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            format_error_state(
                error_kind="runtime",
                detail="Unable to process the query right now. Please try again.",
            ),
            f"{DEFAULT_ERROR_MESSAGE} Error: {exc}",
        )

    log_event(
        UI_LOGGER,
        event_type="request_succeeded",
        request_id=request_id,
        runtime_surface="gradio_ui",
        confidence=result.response.confidence,
        citation_count=len(result.response.citations),
        limitation_count=len(result.response.limitations),
    )
    return render_grounded_result(
        result,
        request_id=request_id,
        runtime_surface="gradio_ui",
        query_length=len(normalized_query),
        top_k=retrieval_query.top_k,
    )


def render_grounded_result(
    result: GroundedAnswerResult,
    *,
    request_id: str,
    runtime_surface: str,
    query_length: int,
    top_k: int | None,
) -> tuple[str, str, str, str, str, str, str, str, str, str]:
    """Render the typed grounded result into UI output fields."""

    response = result.response
    answer = response.suggested_answer
    citations = format_citations(response.citations)
    confidence = response.confidence.upper()
    limitations = format_limitations(response.limitations)
    trace_summary = format_trace_summary(result)
    support_context = format_support_context(
        result,
        request_id=request_id,
        runtime_surface=runtime_surface,
    )
    debug_metadata = format_debug_metadata(
        result,
        request_id=request_id,
        runtime_surface=runtime_surface,
        query_length=query_length,
        top_k=top_k,
    )
    answer_quality_state = format_answer_quality_state(result)
    error_state = format_error_state(error_kind=None)
    status = response.advisor_review_notice
    return (
        answer,
        citations,
        confidence,
        limitations,
        trace_summary,
        support_context,
        debug_metadata,
        answer_quality_state,
        error_state,
        status,
    )


def build_query_handler(
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
):
    """Return the UI handler bound to the current runtime settings."""

    def handle_query(query: str) -> tuple[str, str, str, str, str, str, str, str, str, str]:
        return run_query(
            query,
            settings=settings,
            grounded_answer_fn=grounded_answer_fn,
        )

    return handle_query


def build_loading_query_handler(
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
):
    """Return the streaming UI handler with explicit loading-state feedback."""

    sync_handler = build_query_handler(
        settings=settings,
        grounded_answer_fn=grounded_answer_fn,
    )

    def handle_query(query: str):
        yield (
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "No active errors.",
            format_loading_state(is_loading=True),
            "",
        )
        (
            answer,
            citations,
            confidence,
            limitations,
            trace_summary,
            support_context,
            debug_metadata,
            answer_quality_state,
            error_state,
            status,
        ) = sync_handler(query)
        yield (
            answer,
            citations,
            confidence,
            limitations,
            trace_summary,
            support_context,
            debug_metadata,
            answer_quality_state,
            error_state,
            format_loading_state(is_loading=False),
            status,
        )

    return handle_query


def build_gradio_app(
    *,
    settings: Settings | None = None,
    grounded_answer_fn=generate_grounded_answer,
    gradio_module=None,
    readiness_status_builder=None,
):
    """Build the MVP Gradio query UI."""

    gr = gradio_module or importlib.import_module("gradio")
    resolved_settings = settings or get_settings()
    readiness_message = build_demo_readiness_message(
        resolved_settings,
        readiness_status_builder=readiness_status_builder,
    )
    handler = build_loading_query_handler(
        settings=resolved_settings,
        grounded_answer_fn=grounded_answer_fn,
    )
    with gr.Blocks(title=APP_TITLE) as app:
        gr.Markdown(f"# {APP_TITLE}")
        gr.Markdown(APP_DESCRIPTION)
        gr.Markdown(readiness_message, label="Service Readiness")

        query_input = gr.Textbox(
            label="Advisor Question",
            lines=3,
            placeholder="Ask about coverage, exclusions, procedures, or requirements.",
        )
        submit_button = gr.Button("Generate Draft Answer")

        with gr.Row():
            with gr.Column():
                answer_output = gr.Markdown(label="Suggested Answer")
                status_output = gr.Textbox(label="Review Status")
            with gr.Column():
                confidence_output = gr.Textbox(label="Confidence")
                limitations_output = gr.Markdown(label="Review Limitations")
                trace_output = gr.Textbox(label="Trace Summary")
                support_output = gr.Markdown(label="Support Context")
                debug_output = gr.Markdown(label="Debug Metadata")
                answer_quality_output = gr.Textbox(
                    label="Answer Quality",
                    value="Answer Quality — Standard draft quality.",
                )
                error_output = gr.Textbox(
                    label="Error State",
                    value=format_error_state(error_kind=None),
                )
                loading_output = gr.Textbox(
                    label="Loading Status",
                    value=format_loading_state(is_loading=False),
                )

        citations_output = gr.Markdown(label="Citations")

        submit_button.click(
            fn=handler,
            inputs=[query_input],
            outputs=[
                answer_output,
                citations_output,
                confidence_output,
                limitations_output,
                trace_output,
                support_output,
                debug_output,
                answer_quality_output,
                error_output,
                loading_output,
                status_output,
            ],
            show_progress="full",
        )

        app.title = APP_TITLE
        app.description = APP_DESCRIPTION
        app.flagging_mode = "never"

    return app


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
