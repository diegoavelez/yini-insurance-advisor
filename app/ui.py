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
APP_CSS = """
.gradio-container {
  max-width: 1400px !important;
  margin: 0 auto !important;
  padding: 24px 24px 64px !important;
  background:
    radial-gradient(circle at top, rgba(27, 36, 54, 0.35), transparent 32%),
    linear-gradient(180deg, #0f1115 0%, #12161d 100%);
  color: #f5f7fa;
}

.yini-shell {
  padding: 28px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 28px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02));
  box-shadow: 0 24px 80px -40px rgba(0, 0, 0, 0.75);
  margin-bottom: 20px;
}

.yini-shell-kicker {
  margin: 0 0 10px;
  font-size: 0.8rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #8ba3c7;
}

.yini-shell h1 {
  margin: 0;
  font-size: 2.75rem;
  line-height: 1;
  letter-spacing: -0.04em;
  color: #f8fafc;
}

.yini-shell p {
  margin: 14px 0 0;
  max-width: 72ch;
  line-height: 1.65;
  color: #c9d3df;
}

.yini-shell-status {
  margin-top: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.yini-shell-status-label,
.yini-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid rgba(104, 174, 255, 0.24);
  background: rgba(104, 174, 255, 0.1);
  color: #dceafe;
  font-size: 0.9rem;
}

.yini-shell-status-copy {
  color: #e6edf6;
  font-size: 0.95rem;
}

.yini-composer,
.yini-main-surface,
.yini-side-surface,
.yini-evidence-surface,
.yini-detail-surface,
.yini-tech-surface {
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.03);
  box-shadow: 0 18px 60px -36px rgba(0, 0, 0, 0.72);
}

.yini-composer {
  padding: 8px 8px 0;
  margin-bottom: 18px;
}

.yini-query-input textarea {
  min-height: 132px !important;
  border-radius: 18px !important;
  background: rgba(10, 13, 18, 0.78) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #f8fafc !important;
  box-shadow: none !important;
}

.yini-primary-button button {
  min-height: 56px;
  border-radius: 18px !important;
  border: 1px solid rgba(129, 178, 255, 0.3) !important;
  background: linear-gradient(180deg, #5c6780 0%, #51596d 100%) !important;
  color: #f8fafc !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  box-shadow: 0 12px 36px -24px rgba(92, 103, 128, 0.85);
}

.yini-primary-button button:active {
  transform: translateY(1px) scale(0.99);
}

.yini-example-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 14px 4px 16px;
}

.yini-section-title {
  margin: 0 0 10px;
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #f5f7fa;
}

.yini-section-subtitle {
  margin: 0 0 14px;
  color: #aeb9c7;
  font-size: 0.92rem;
}

.yini-answer-block,
.yini-documentary-block,
.yini-citations-block {
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 8px;
  scrollbar-width: thin;
  scrollbar-color: rgba(140, 159, 184, 0.75) rgba(255, 255, 255, 0.06);
}

.yini-answer-block,
.yini-citations-block,
.yini-documentary-block,
.yini-status-card,
.yini-confidence-card,
.yini-quality-card,
.yini-limitations-card,
.yini-trace-card,
.yini-support-card,
.yini-debug-card,
.yini-error-card,
.yini-loading-card {
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 20px;
  background: rgba(8, 11, 17, 0.66);
  padding: 16px 18px;
}

.yini-answer-block h1,
.yini-answer-block h2,
.yini-answer-block h3,
.yini-answer-block h4,
.yini-citations-block h1,
.yini-citations-block h2,
.yini-citations-block h3,
.yini-documentary-block h1,
.yini-documentary-block h2,
.yini-documentary-block h3 {
  letter-spacing: -0.03em;
}

.yini-answer-block table,
.yini-documentary-block table,
.yini-citations-block table {
  display: block;
  width: max-content;
  min-width: max-content;
  max-width: none;
  overflow-x: auto;
  overflow-y: hidden;
  table-layout: auto;
  border-collapse: collapse;
}

.yini-answer-block th,
.yini-answer-block td,
.yini-documentary-block th,
.yini-documentary-block td,
.yini-citations-block th,
.yini-citations-block td {
  white-space: nowrap;
  overflow-wrap: normal;
  word-break: normal;
  hyphens: none;
  font-variant-numeric: tabular-nums;
  min-width: 7.5rem;
  vertical-align: top;
}

.yini-answer-block th:first-child,
.yini-answer-block td:first-child,
.yini-documentary-block th:first-child,
.yini-documentary-block td:first-child,
.yini-citations-block th:first-child,
.yini-citations-block td:first-child {
  min-width: 14rem;
}

.yini-answer-block th p,
.yini-answer-block td p,
.yini-documentary-block th p,
.yini-documentary-block td p,
.yini-citations-block th p,
.yini-citations-block td p {
  margin: 0;
  white-space: nowrap;
  overflow-wrap: normal;
}

.yini-answer-block::-webkit-scrollbar,
.yini-documentary-block::-webkit-scrollbar,
.yini-citations-block::-webkit-scrollbar {
  height: 10px;
}

.yini-answer-block::-webkit-scrollbar-track,
.yini-documentary-block::-webkit-scrollbar-track,
.yini-citations-block::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 999px;
}

.yini-answer-block::-webkit-scrollbar-thumb,
.yini-documentary-block::-webkit-scrollbar-thumb,
.yini-citations-block::-webkit-scrollbar-thumb {
  background: rgba(143, 160, 183, 0.8);
  border-radius: 999px;
}

.yini-table-hint {
  margin: 10px 0 14px;
  color: #8fa0b7;
  font-size: 0.86rem;
}

.yini-accordion .label-wrap,
.yini-accordion button,
.yini-accordion {
  border-radius: 18px !important;
}

.yini-accordion {
  margin-top: 14px;
  border: 1px solid rgba(255, 255, 255, 0.07) !important;
  background: rgba(255, 255, 255, 0.02) !important;
}

.yini-review-column > .wrap,
.yini-answer-column > .wrap {
  gap: 14px;
}

@media (max-width: 767px) {
  .gradio-container {
    padding: 16px 16px 40px !important;
  }

  .yini-shell {
    padding: 22px 18px;
    border-radius: 22px;
  }

  .yini-shell h1 {
    font-size: 2.2rem;
  }
}
"""
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

    def compact_quote_preview(quote: str) -> str:
        normalized_quote = " ".join(quote.split())
        if len(normalized_quote) <= 220:
            return normalized_quote
        return normalized_quote[:217].rstrip() + "..."

    lines: list[str] = []
    for index, citation in enumerate(citations, start=1):
        parts = [f"**{citation.document_name}**"]
        if citation.section:
            parts.append(f"sección: {citation.section}")
        if citation.page is not None:
            parts.append(f"página: {citation.page}")
        if citation.clause_id:
            parts.append(f"cláusula: {citation.clause_id}")
        line = f"{index}. " + " | ".join(parts)
        if citation.quote:
            line += f"\n   Vista previa: {compact_quote_preview(citation.quote)}"
        lines.append(line)
    return "\n".join(lines)


def render_shell_header(readiness_message: str) -> str:
    """Render the branded shell header for the Gradio MVP."""

    return (
        '<section class="yini-shell">'
        '<p class="yini-shell-kicker">Asistente de revisión fundamentada</p>'
        f"<h1>{APP_TITLE}</h1>"
        f"<p>{APP_DESCRIPTION}</p>"
        '<div class="yini-shell-status">'
        '<span class="yini-shell-status-label">Estado del servicio</span>'
        f'<span class="yini-shell-status-copy">{readiness_message}</span>'
        "</div>"
        "</section>"
    )


def render_example_query_strip() -> str:
    """Render compact example prompts to orient the MVP user."""

    examples = [
        "Coberturas y exclusiones",
        "Procedimientos operativos",
        "Requisitos y asegurabilidad",
        "Tarifas y comparativos",
    ]
    chips = "".join(f'<span class="yini-chip">{example}</span>' for example in examples)
    return f'<div class="yini-example-strip">{chips}</div>'


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
    with gr.Blocks(title=APP_TITLE, css=APP_CSS) as app:
        gr.HTML(render_shell_header(readiness_message))

        query_input = gr.Textbox(
            label="Pregunta del asesor",
            lines=3,
            placeholder="Pregunta por coberturas, exclusiones, procedimientos o requisitos.",
            elem_classes=["yini-query-input", "yini-composer"],
        )
        gr.HTML(render_example_query_strip())
        submit_button = gr.Button(
            "Generar borrador de respuesta",
            elem_classes=["yini-primary-button"],
        )

        with gr.Row():
            with gr.Column(scale=8, elem_classes=["yini-answer-column"]):
                gr.HTML(
                    (
                        '<div class="yini-main-surface">'
                        '<p class="yini-section-title">Respuesta sugerida</p>'
                        '<p class="yini-section-subtitle">'
                        "Borrador fundamentado para revisión del asesor. "
                        "Si la salida incluye tablas anchas, desplázalas horizontalmente."
                        "</p>"
                        "</div>"
                    )
                )
                answer_output = gr.Markdown(
                    label="Respuesta sugerida",
                    show_label=False,
                    elem_classes=["yini-answer-block"],
                )
            with gr.Column(scale=4, elem_classes=["yini-review-column"]):
                gr.HTML(
                    (
                        '<div class="yini-side-surface">'
                        '<p class="yini-section-title">Panel de revisión</p>'
                        '<p class="yini-section-subtitle">'
                        "Evalúa estado, confianza y limitaciones antes de reutilizar el borrador."
                        "</p>"
                        "</div>"
                    )
                )
                gr.Markdown("#### Estado de revisión")
                status_output = gr.Markdown(
                    label="Estado de revisión",
                    show_label=False,
                    elem_classes=["yini-status-card"],
                )
                gr.Markdown("#### Confianza")
                confidence_output = gr.Markdown(
                    label="Confianza",
                    show_label=False,
                    elem_classes=["yini-confidence-card"],
                )
                gr.Markdown("#### Calidad de la respuesta")
                answer_quality_output = gr.Markdown(
                    label="Calidad de la respuesta",
                    show_label=False,
                    value="Calidad de la respuesta — Calidad estándar del borrador.",
                    elem_classes=["yini-quality-card"],
                )
                gr.Markdown("#### Limitaciones para revisión")
                limitations_output = gr.Markdown(
                    label="Limitaciones para revisión",
                    show_label=False,
                    elem_classes=["yini-limitations-card"],
                )

        with gr.Accordion(
            "Citas clave y evidencia",
            open=False,
            elem_classes=["yini-accordion"],
        ):
            gr.HTML(
                '<p class="yini-table-hint">Usa esta sección para contrastar la respuesta con la evidencia recuperada.</p>'
            )
            gr.Markdown("### Citas clave")
            citations_output = gr.Markdown(
                label="Citas clave",
                show_label=False,
                elem_classes=["yini-citations-block"],
            )
            gr.Markdown("### Base documental")
            documentary_basis_output = gr.Markdown(
                label="Base documental",
                show_label=False,
                elem_classes=["yini-documentary-block"],
            )

        with gr.Accordion(
            "Detalles de revisión",
            open=False,
            elem_classes=["yini-accordion"],
        ):
            gr.Markdown("### Resumen de trazabilidad")
            trace_output = gr.Markdown(
                label="Resumen de trazabilidad",
                show_label=False,
                elem_classes=["yini-trace-card"],
            )
            gr.Markdown("### Contexto de soporte")
            support_output = gr.Markdown(
                label="Contexto de soporte",
                show_label=False,
                elem_classes=["yini-support-card"],
            )

        with gr.Accordion(
            "Diagnóstico técnico",
            open=False,
            elem_classes=["yini-accordion"],
        ):
            gr.Markdown("### Metadatos de depuración")
            debug_output = gr.Markdown(
                label="Metadatos de depuración",
                show_label=False,
                elem_classes=["yini-debug-card"],
            )
            gr.Markdown("### Estado de error")
            error_output = gr.Markdown(
                label="Estado de error",
                show_label=False,
                value=format_error_state(error_kind=None),
                elem_classes=["yini-error-card"],
            )
            gr.Markdown("### Estado de carga")
            loading_output = gr.Markdown(
                label="Estado de carga",
                show_label=False,
                value=format_loading_state(is_loading=False),
                elem_classes=["yini-loading-card"],
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
