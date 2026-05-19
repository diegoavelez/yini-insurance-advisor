"""Baseline observability helpers for startup diagnostics and request correlation."""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable
from contextlib import contextmanager

from core.config import Settings


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
    logger.log(level, message or event_type, extra=payload)


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
