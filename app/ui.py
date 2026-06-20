"""Thin Gradio UI over the grounded QA pipeline."""

from __future__ import annotations

import importlib
import importlib.util
import logging
import re

from contracts import Citation, DocumentaryBasisItem, GroundedAnswerResult, RetrievalQuery
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
    "Asistente fundamentado sobre documentos de seguros para revisión del asesor. "
    "Las respuestas son borradores y deben mantenerse vinculadas a evidencia citada."
)
DEFAULT_ERROR_MESSAGE = "No es posible procesar la consulta en este momento."
DEFAULT_LOADING_MESSAGE = "Generando borrador de respuesta..."
UI_LOGGER = logging.getLogger("yini.ui")
APP_LOGGER = logging.getLogger("yini.app")
SAFE_TRACE_ITEM_PATTERN = re.compile(r"^[a-z0-9_:-]{1,40}$")
PUBLIC_TEXT_TRANSLATIONS = {
    "Please enter a question.": "Por favor, ingresa una pregunta.",
    "Advisor review required before external use.": (
        "Se requiere revisión del asesor antes del uso externo."
    ),
    "This response is a draft for advisor review.": (
        "Esta respuesta es un borrador para revisión del asesor."
    ),
    "Advisor review is still required.": "La revisión del asesor sigue siendo obligatoria.",
    (
        "I cannot answer that request within the supported insurance-document scope "
        "of this assistant."
    ): (
        "No puedo responder esa solicitud dentro del alcance soportado de documentos "
        "de seguros de este asistente."
    ),
    "This request is outside the supported insurance-document scope.": (
        "Esta solicitud está fuera del alcance soportado de documentos de seguros."
    ),
    (
        "I cannot follow instructions that attempt to override the assistant's "
        "grounded-use rules or reveal hidden system behavior."
    ): (
        "No puedo seguir instrucciones que intenten anular las reglas de uso "
        "fundamentado del asistente ni revelar comportamiento interno oculto."
    ),
    "This request triggered a prompt-injection guardrail and was refused conservatively.": (
        "Esta solicitud activó un guardrail de prompt injection y fue rechazada "
        "de forma conservadora."
    ),
}
SUPPORT_OUTCOME_TRANSLATIONS = {
    "prompt_guardrail_refusal": "rechazo por guardrail de prompt",
    "unsupported_scope_refusal": "rechazo por alcance no soportado",
    "limited_evidence_draft": "borrador con evidencia limitada",
    "grounded_draft_ready": "borrador fundamentado listo",
    "review_required_draft": "borrador que requiere revisión",
}
TRACE_ITEM_TRANSLATIONS = {
    "query_received": "consulta_recibida",
    "grounded_answer_drafted": "borrador_fundamentado_generado",
    "internal_step_redacted": "paso_interno_redactado",
    "grounding:supported": "fundamentacion:soportada",
    "grounding:limited": "fundamentacion:limitada",
}
CONFIDENCE_TRANSLATIONS = {
    "high": "alta",
    "medium": "media",
    "low": "baja",
}


def localize_public_text(text: str) -> str:
    """Translate stable user-visible public strings without changing backend seams."""

    return PUBLIC_TEXT_TRANSLATIONS.get(text.strip(), text)


def localize_support_outcome(outcome: str) -> str:
    """Translate support/debug outcome labels for the public UI."""

    return SUPPORT_OUTCOME_TRANSLATIONS.get(outcome, outcome)


def localize_trace_item(item: str) -> str:
    """Translate concise trace-summary tokens for the public UI."""

    if item in TRACE_ITEM_TRANSLATIONS:
        return TRACE_ITEM_TRANSLATIONS[item]
    if item.startswith("citations:"):
        return item.replace("citations:", "citas:", 1)
    if item.startswith("confidence:"):
        confidence = item.split(":", 1)[1]
        return f"confianza:{CONFIDENCE_TRANSLATIONS.get(confidence, confidence)}"
    return item


def format_citations(citations: list[Citation]) -> str:
    """Render concise public-facing citations for the MVP UI."""

    if not citations:
        return "No hay citas disponibles."

    lines: list[str] = []
    for citation in citations:
        parts = [f"**{citation.document_name}**"]
        if citation.section:
            parts.append(f"sección: {citation.section}")
        if citation.page is not None:
            parts.append(f"página: {citation.page}")
        if citation.clause_id:
            parts.append(f"cláusula: {citation.clause_id}")
        line = "- " + " | ".join(parts)
        if citation.quote:
            line += f"\n  > {citation.quote}"
        lines.append(line)
    return "\n".join(lines)


def format_documentary_basis(documentary_basis: list[DocumentaryBasisItem]) -> str:
    """Render compact documentary basis for the review details panel."""

    if not documentary_basis:
        return "No hay base documental disponible."

    lines: list[str] = []
    for basis_item in documentary_basis:
        parts = [f"**{basis_item.document_name}**"]
        if basis_item.source_pdf_relative_path:
            parts.append(f"ruta fuente: {basis_item.source_pdf_relative_path}")
        if basis_item.document_type:
            parts.append(f"tipo: {basis_item.document_type}")
        if basis_item.product:
            parts.append(f"producto: {basis_item.product}")
        if basis_item.section:
            parts.append(f"sección: {basis_item.section}")
        if basis_item.page is not None:
            parts.append(f"página: {basis_item.page}")
        if basis_item.clause_id:
            parts.append(f"cláusula: {basis_item.clause_id}")
        line = "- " + " | ".join(parts)
        if basis_item.note:
            line += f"\n  > evidencia interna: {basis_item.note}"
        lines.append(line)
    return "\n".join(lines)


def format_operator_evidence_summary(result: GroundedAnswerResult) -> str:
    """Render a compact operator-facing summary of current grounded evidence."""

    document_names: list[str] = []
    document_types: list[str] = []
    products: list[str] = []

    def collect_unique(target: list[str], value: str | None) -> None:
        if value and value not in target:
            target.append(value)

    for citation in result.response.citations:
        collect_unique(document_names, citation.document_name)
        collect_unique(document_types, citation.document_type)
        collect_unique(products, citation.product)

    for basis_item in result.response.documentary_basis:
        collect_unique(document_names, basis_item.document_name)
        collect_unique(document_types, basis_item.document_type)
        collect_unique(products, basis_item.product)

    if not document_names and not document_types and not products:
        return "Sin evidencia resumida disponible."

    summary_parts: list[str] = []
    if document_names:
        summary_parts.append(f"documentos: {', '.join(document_names)}")
    if document_types:
        summary_parts.append(f"tipos: {', '.join(document_types)}")
    if products:
        summary_parts.append(f"productos: {', '.join(products)}")
    return " | ".join(summary_parts)


def format_limitations(limitations: list[str]) -> str:
    """Render limitations into a stable markdown block for the MVP UI."""

    if not limitations:
        return "No se registraron limitaciones adicionales."
    return "\n".join(f"- {localize_public_text(limitation)}" for limitation in limitations)


def format_trace_summary(result: GroundedAnswerResult) -> str:
    """Render a concise review-oriented trace summary for the current result."""

    explicit_trace = getattr(result, "trace_summary", None)
    if isinstance(explicit_trace, list) and explicit_trace:
        sanitized_items = sanitize_trace_items(explicit_trace)
        if sanitized_items:
            return " → ".join(localize_trace_item(item) for item in sanitized_items)

    response = result.response
    verification = result.verification
    steps = ["query_received", "grounded_answer_drafted"]
    if response.citations:
        steps.append(f"citations:{len(response.citations)}")
    else:
        steps.append("citations:0")
    steps.append(f"confidence:{response.confidence}")
    steps.append("grounding:supported" if verification.supported else "grounding:limited")
    return " → ".join(localize_trace_item(step) for step in steps)


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


def infer_support_outcome(
    result: GroundedAnswerResult,
    *,
    override: str | None = None,
) -> str:
    """Infer a concise support outcome label from structured grounded-result fields."""

    if override is not None:
        return override
    if result.verification.supported and result.response.confidence != "low":
        return "grounded_draft_ready"
    if result.response.confidence == "low" or not result.verification.supported:
        if result.response.citations or not result.verification.unsupported_claims:
            return "limited_evidence_draft"
    return "review_required_draft"


def format_support_context(
    result: GroundedAnswerResult,
    *,
    request_id: str,
    runtime_surface: str,
    support_outcome: str | None = None,
) -> str:
    """Render concise demo-safe support context for the current request."""

    outcome = infer_support_outcome(result, override=support_outcome)
    return "\n".join(
        [
            f"- ID de solicitud: {request_id}",
            f"- Superficie de ejecución: {runtime_surface}",
            f"- Resultado de soporte: {localize_support_outcome(outcome)}",
            "- Seguimiento: comparte el ID de solicitud al pedir revisión de soporte.",
        ]
    )


def format_debug_metadata(
    result: GroundedAnswerResult,
    *,
    request_id: str,
    runtime_surface: str,
    query_length: int,
    top_k: int | None,
    support_outcome: str | None = None,
) -> str:
    """Render compact operator-facing debug metadata for the current request."""

    response = result.response
    outcome = infer_support_outcome(result, override=support_outcome)
    return "\n".join(
        [
            f"- ID de solicitud: {request_id}",
            f"- Superficie de ejecución: {runtime_surface}",
            f"- Longitud de la consulta: {query_length}",
            f"- Top K de recuperación: {top_k if top_k is not None else 'n/a'}",
            "- Nivel de confianza: "
            + CONFIDENCE_TRANSLATIONS.get(response.confidence, response.confidence),
            f"- Cantidad de citas: {len(response.citations)}",
            f"- Cantidad de limitaciones: {len(response.limitations)}",
            f"- Resumen de evidencia: {format_operator_evidence_summary(result)}",
            f"- Resultado de depuración: {localize_support_outcome(outcome)}",
        ]
    )


def format_loading_state(*, is_loading: bool) -> str:
    """Render concise loading-state feedback for the current demo UI."""

    if is_loading:
        return DEFAULT_LOADING_MESSAGE
    return "Borrador listo para revisión."


def format_error_state(
    *,
    error_kind: str | None,
    detail: str | None = None,
) -> str:
    """Render a concise user-visible error-state message."""

    if error_kind is None:
        return "No hay errores activos."
    if error_kind == "input":
        return (
            "Error de entrada — "
            + (detail or "Revisa la pregunta e inténtalo de nuevo.")
        )
    if error_kind == "runtime":
        return (
            "Error de ejecución — "
            + (detail or "La solicitud no se puede procesar en este momento.")
        )
    return detail or "Estado de error desconocido."


def format_readiness_state(*, status: str, detail: str | None = None) -> str:
    """Render concise demo-safe readiness messaging for the public UI."""

    if status == "ready":
        return "Estado del servicio — Listo para generar borradores fundamentados."
    if status == "degraded":
        return (
            "Estado del servicio — Degradado. "
            + (
                detail
                or (
                    "Las dependencias de ejecución requeridas no están disponibles. "
                    "La generación del borrador puede fallar hasta que el servicio se restablezca."
                )
            )
        )
    return detail or "Estado del servicio — Desconocido."


def is_degraded_answer_quality(
    result: GroundedAnswerResult,
    *,
    support_outcome: str | None = None,
) -> bool:
    """Return whether the current grounded result should surface degraded quality."""

    outcome = infer_support_outcome(result, override=support_outcome)
    return (
        result.response.confidence == "low"
        or not result.verification.supported
        or bool(result.verification.missing_citations)
        or outcome
        in {
            "prompt_guardrail_refusal",
            "unsupported_scope_refusal",
            "limited_evidence_draft",
        }
    )


def format_answer_quality_state(
    result: GroundedAnswerResult,
    *,
    support_outcome: str | None = None,
) -> str:
    """Render concise user-visible messaging for degraded draft quality."""

    degraded = is_degraded_answer_quality(result, support_outcome=support_outcome)
    if degraded:
        return (
            "Calidad de la respuesta — Degradada. Este borrador tiene menor "
            "confianza o soporte fundamentado limitado y requiere revisión adicional del asesor."
        )
    return "Calidad de la respuesta — Calidad estándar del borrador."


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
) -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
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
            "",
            format_error_state(
                error_kind="input",
                detail=localize_public_text("Please enter a question."),
            ),
            localize_public_text("Please enter a question."),
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
            support_outcome_override="prompt_guardrail_refusal",
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
            support_outcome_override="unsupported_scope_refusal",
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
            "",
            format_error_state(
                error_kind="runtime",
                detail="No es posible procesar la consulta en este momento. Inténtalo de nuevo.",
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
    support_outcome_override: str | None = None,
) -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
    """Render the typed grounded result into UI output fields."""

    response = result.response
    support_outcome = infer_support_outcome(result, override=support_outcome_override)
    answer = localize_public_text(response.suggested_answer)
    citations = format_citations(response.citations)
    documentary_basis = format_documentary_basis(response.documentary_basis)
    confidence = response.confidence.upper()
    limitations = format_limitations(response.limitations)
    trace_summary = format_trace_summary(result)
    support_context = format_support_context(
        result,
        request_id=request_id,
        runtime_surface=runtime_surface,
        support_outcome=support_outcome,
    )
    debug_metadata = format_debug_metadata(
        result,
        request_id=request_id,
        runtime_surface=runtime_surface,
        query_length=query_length,
        top_k=top_k,
        support_outcome=support_outcome,
    )
    answer_quality_state = format_answer_quality_state(
        result,
        support_outcome=support_outcome,
    )
    error_state = format_error_state(error_kind=None)
    status = localize_public_text(response.advisor_review_notice)
    return (
        answer,
        citations,
        documentary_basis,
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

    def handle_query(
        query: str,
    ) -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
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
            "",
            "No hay errores activos.",
            format_loading_state(is_loading=True),
            "",
        )
        (
            answer,
            citations,
            documentary_basis,
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
            documentary_basis,
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
        gr.Markdown(readiness_message, label="Estado del servicio")

        query_input = gr.Textbox(
            label="Pregunta del asesor",
            lines=3,
            placeholder="Pregunta por coberturas, exclusiones, procedimientos o requisitos.",
        )
        submit_button = gr.Button("Generar borrador de respuesta")

        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown("### Respuesta sugerida")
                answer_output = gr.Markdown(label="Respuesta sugerida")
                gr.Markdown("### Citas clave")
                citations_output = gr.Markdown(label="Citas clave")
            with gr.Column(scale=2):
                status_output = gr.Textbox(label="Estado de revisión", interactive=False)
                confidence_output = gr.Textbox(label="Confianza", interactive=False)
                answer_quality_output = gr.Textbox(
                    label="Calidad de la respuesta",
                    value="Calidad de la respuesta — Calidad estándar del borrador.",
                    interactive=False,
                )
                gr.Markdown("### Limitaciones para revisión")
                limitations_output = gr.Markdown(label="Limitaciones para revisión")

        with gr.Accordion("Detalles de revisión", open=False):
            trace_output = gr.Textbox(label="Resumen de trazabilidad", interactive=False)
            gr.Markdown("### Base documental")
            documentary_basis_output = gr.Markdown(label="Base documental")
            gr.Markdown("### Contexto de soporte")
            support_output = gr.Markdown(label="Contexto de soporte")

        with gr.Accordion("Diagnóstico técnico", open=False):
            gr.Markdown("### Metadatos de depuración")
            debug_output = gr.Markdown(label="Metadatos de depuración")
            error_output = gr.Textbox(
                label="Estado de error",
                value=format_error_state(error_kind=None),
                interactive=False,
            )
            loading_output = gr.Textbox(
                label="Estado de carga",
                value=format_loading_state(is_loading=False),
                interactive=False,
            )

        submit_button.click(
            fn=handler,
            inputs=[query_input],
            outputs=[
                answer_output,
                citations_output,
                documentary_basis_output,
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
