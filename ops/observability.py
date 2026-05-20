"""Baseline observability helpers for startup diagnostics and request correlation."""

from __future__ import annotations

import importlib.util
import logging
import time
import uuid
from collections import deque
from collections.abc import Callable
from contextlib import contextmanager

from contracts.guardrails import GuardrailEventRecord, GuardrailSummary
from core.config import Settings

GUARDRAIL_EVENT_TYPES = {
    "query_scope_refusal",
    "prompt_injection_guardrail_triggered",
    "citation_presence_guardrail_triggered",
    "confidence_consistency_guardrail_triggered",
}
GUARDRAIL_EVENT_BUFFER: deque[GuardrailEventRecord] = deque(maxlen=200)


def generate_request_id(prefix: str = "req") -> str:
    """Generate a stable human-inspectable request identifier."""

    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def build_startup_diagnostics(
    settings: Settings,
    *,
    runtime_surface: str,
) -> dict[str, object]:
    """Build the non-secret startup diagnostics payload."""

    return {
        "event_type": "startup_diagnostics",
        "runtime_surface": runtime_surface,
        "deployment_mode": settings.deployment_mode,
        "app_env": settings.app_env,
        "groq_model": settings.groq_model,
        "embedding_provider": settings.embedding_provider,
        "embedding_model": settings.embedding_model,
        "qdrant_collection": settings.qdrant_collection,
        "top_k": settings.top_k,
    }


def log_startup_diagnostics(
    logger: logging.Logger,
    settings: Settings,
    *,
    runtime_surface: str,
) -> None:
    """Emit one startup diagnostics event."""

    logger.info(
        "Startup diagnostics emitted",
        extra=build_startup_diagnostics(settings, runtime_surface=runtime_surface),
    )


def phoenix_backend_is_available() -> bool:
    """Return whether the Phoenix backend is importable."""

    return importlib.util.find_spec("phoenix") is not None


def build_health_status(*, runtime_surface: str) -> dict[str, object]:
    """Build the narrow liveness payload for the current runtime surface."""

    return {
        "event_type": "health_check_succeeded",
        "runtime_surface": runtime_surface,
        "status": "ok",
    }


def log_health_status(logger: logging.Logger, *, runtime_surface: str) -> dict[str, object]:
    """Emit one health event and return the payload."""

    payload = build_health_status(runtime_surface=runtime_surface)
    logger.info("Health check succeeded", extra=payload)
    return payload


def maybe_activate_phoenix(
    logger: logging.Logger,
    settings: Settings,
    *,
    runtime_surface: str,
    activator: Callable[[Settings], None] | None = None,
    backend_available: bool | None = None,
) -> dict[str, object]:
    """Conditionally activate Phoenix tracing without breaking unconfigured runs."""

    if settings.phoenix_endpoint is None:
        payload = {
            "event_type": "phoenix_activation_skipped",
            "runtime_surface": runtime_surface,
            "status": "disabled",
            "reason": "not_configured",
        }
        logger.info("Phoenix activation skipped", extra=payload)
        return payload

    resolved_backend_available = (
        phoenix_backend_is_available() if backend_available is None else backend_available
    )
    if not resolved_backend_available:
        payload = {
            "event_type": "phoenix_activation_skipped",
            "runtime_surface": runtime_surface,
            "status": "skipped",
            "reason": "backend_unavailable",
            "phoenix_project_name": settings.phoenix_project_name,
        }
        logger.warning("Phoenix activation skipped", extra=payload)
        return payload

    try:
        if activator is not None:
            activator(settings)
    except Exception as exc:
        payload = {
            "event_type": "phoenix_activation_failed",
            "runtime_surface": runtime_surface,
            "status": "failed",
            "phoenix_project_name": settings.phoenix_project_name,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        logger.error("Phoenix activation failed", extra=payload)
        raise RuntimeError("Phoenix activation failed.") from exc

    payload = {
        "event_type": "phoenix_activation_enabled",
        "runtime_surface": runtime_surface,
        "status": "enabled",
        "phoenix_project_name": settings.phoenix_project_name,
    }
    logger.info("Phoenix activation enabled", extra=payload)
    return payload


def log_event(
    logger: logging.Logger,
    *,
    event_type: str,
    request_id: str | None = None,
    level: int = logging.INFO,
    message: str | None = None,
    **fields: object,
) -> None:
    """Emit one structured runtime event."""

    payload: dict[str, object] = {"event_type": event_type}
    if request_id is not None:
        payload["request_id"] = request_id
    payload.update(fields)
    if event_type in GUARDRAIL_EVENT_TYPES:
        record = GuardrailEventRecord(
            event_type=event_type,
            request_id=request_id,
            guardrail_surface=(
                fields.get("guardrail_surface")
                if isinstance(fields.get("guardrail_surface"), str)
                else None
            ),
            timestamp_ms=round(time.time() * 1000),
            details=dict(fields),
        )
        GUARDRAIL_EVENT_BUFFER.append(record)
    logger.log(level, message or event_type, extra=payload)


def clear_guardrail_event_buffer() -> None:
    """Clear the local in-memory guardrail event buffer."""

    GUARDRAIL_EVENT_BUFFER.clear()


def build_guardrail_summary(*, recent_limit: int = 10) -> GuardrailSummary:
    """Build a compact local summary of recent guardrail/refusal activity."""

    recorded_events = list(GUARDRAIL_EVENT_BUFFER)
    event_counts: dict[str, int] = {}
    for record in recorded_events:
        event_counts[record.event_type] = event_counts.get(record.event_type, 0) + 1
    return GuardrailSummary(
        total_events=len(recorded_events),
        event_counts=event_counts,
        recent_events=recorded_events[-recent_limit:],
    )


@contextmanager
def log_timed_event(
    logger: logging.Logger,
    *,
    event_type: str,
    request_id: str | None = None,
    start_message: str | None = None,
    success_message: str | None = None,
    failure_message: str | None = None,
    start_fields: dict[str, object] | None = None,
    success_fields_factory: Callable[[float], dict[str, object]] | None = None,
):
    """Emit start/success/failure events with duration."""

    log_event(
        logger,
        event_type=f"{event_type}_started",
        request_id=request_id,
        message=start_message,
        **(start_fields or {}),
    )
    started_at = time.perf_counter()
    try:
        yield
    except Exception as exc:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 3)
        failure_fields = {
            "duration_ms": duration_ms,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }
        log_event(
            logger,
            event_type=f"{event_type}_failed",
            request_id=request_id,
            level=logging.ERROR,
            message=failure_message,
            **failure_fields,
        )
        raise

    duration_ms = round((time.perf_counter() - started_at) * 1000, 3)
    success_fields = {"duration_ms": duration_ms}
    if success_fields_factory is not None:
        success_fields.update(success_fields_factory(duration_ms))
    log_event(
        logger,
        event_type=f"{event_type}_succeeded",
        request_id=request_id,
        message=success_message,
        **success_fields,
    )
