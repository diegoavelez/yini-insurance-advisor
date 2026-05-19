"""Independently callable retrieval tool wrapper."""

from __future__ import annotations

import logging

from contracts import (
    DocumentRetrievalResult,
    DocumentRetrievalToolResult,
    RetrievalQuery,
    ToolError,
)
from core.config import Settings
from ops.observability import log_timed_event
from rag.ingestion import retrieve_ranked_chunks

TOOL_LOGGER = logging.getLogger("yini.tools.document_retrieval")


def classify_tool_error(exc: Exception) -> ToolError:
    """Map expected retrieval failures into the typed tool error surface."""

    message = str(exc)
    normalized_message = message.lower()

    if (
        isinstance(exc, ValueError)
        or "must be" in normalized_message
        or "required" in normalized_message
    ):
        return ToolError(kind="configuration_failure", message=message)
    if "not installed" in normalized_message or "unavailable" in normalized_message:
        return ToolError(kind="dependency_failure", message=message)
    return ToolError(kind="backend_failure", message=message)


def document_retrieval_tool(
    retrieval_query: RetrievalQuery,
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
) -> DocumentRetrievalToolResult:
    """Execute the reusable document retrieval tool over the existing retrieval seam."""

    try:
        with log_timed_event(
            TOOL_LOGGER,
            event_type="document_retrieval_tool",
            request_id=request_id,
            start_fields={"top_k": retrieval_query.top_k},
            success_fields_factory=(
                lambda _duration_ms: {"result_count": len(retrieval_result.chunks)}
            ),
        ):
            retrieval_result = retrieve_ranked_chunks(
                retrieval_query,
                settings=settings,
                client=client,
                request_id=request_id,
            )
            return DocumentRetrievalToolResult(ok=True, result=retrieval_result)
    except Exception as exc:
        return DocumentRetrievalToolResult(
            ok=False,
            error=classify_tool_error(exc),
        )


def unwrap_retrieval_tool_result(
    tool_result: DocumentRetrievalToolResult,
) -> DocumentRetrievalResult:
    """Return the successful retrieval result or raise on typed tool failure."""

    if tool_result.result is None or not tool_result.ok:
        raise RuntimeError(
            tool_result.error.message if tool_result.error else "Retrieval tool failed."
        )
    return tool_result.result
