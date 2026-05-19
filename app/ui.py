"""Thin Gradio UI over the grounded QA pipeline."""

from __future__ import annotations

import importlib
import logging

from contracts import Citation, GroundedAnswerResult, RetrievalQuery
from core.config import Settings, get_settings, validate_startup_settings
from core.logging import configure_logging
from rag.ingestion import generate_grounded_answer

APP_TITLE = "Yini"
APP_DESCRIPTION = (
    "Grounded insurance document assistant for advisor review. Answers are drafts and "
    "must remain tied to cited evidence."
)
DEFAULT_ERROR_MESSAGE = "Unable to process the query right now."


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

    normalized_query = query.strip()
    if not normalized_query:
        return "", "", "", "", "Please enter a question."

    resolved_settings = validate_startup_settings(
        settings or get_settings(),
        require_groq=True,
        require_qdrant=True,
    )
    retrieval_query = build_retrieval_query(normalized_query, resolved_settings)

    try:
        result = grounded_answer_fn(retrieval_query, settings=resolved_settings)
    except Exception as exc:
        return "", "", "", "", f"{DEFAULT_ERROR_MESSAGE} Error: {exc}"

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


def main(*, launch: bool = True) -> int:
    """Start the MVP Gradio app entrypoint."""

    settings = validate_startup_settings(get_settings())
    configure_logging(settings.log_level)

    logger = logging.getLogger("yini.app")
    app = build_gradio_app(settings=settings)
    logger.info(
        "Phase 5 MVP UI ready",
        extra={
            "app_env": settings.app_env,
            "groq_model": settings.groq_model,
            "top_k": settings.top_k,
        },
    )
    if launch:
        app.launch()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
