from __future__ import annotations

import logging
from collections import deque

import pytest
from pydantic import ValidationError

import app.ui as app_ui
from contracts import (
    AdvisorDraftResponse,
    EvaluationQuestionResult,
    EvaluationRunResult,
    GroundedAnswerResult,
    GroundingVerification,
)
from core.config import (
    Settings,
    clear_settings_cache,
    get_settings,
    validate_startup_settings,
)
from core.evaluation_runner import (
    run_hosted_citation_regression_smoke,
    run_hosted_latency_smoke,
)
from ops.observability import build_health_status


@pytest.fixture(autouse=True)
def reset_settings_cache() -> None:
    clear_settings_cache()
    yield
    clear_settings_cache()


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.groq_model == "openai/gpt-oss-120b"
    assert settings.deployment_mode == "public_mvp_demo"
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.top_k == 5


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TOP_K", "7")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DEPLOYMENT_MODE", "internal_production")
    monkeypatch.setenv("GROQ_MODEL", "custom/model")

    settings = Settings(_env_file=None)

    assert settings.deployment_mode == "internal_production"
    assert settings.top_k == 7
    assert settings.app_env == "test"
    assert settings.groq_model == "custom/model"


def test_invalid_app_env_fails() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, app_env="invalid")


def test_invalid_deployment_mode_fails() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, deployment_mode="public")


def test_invalid_log_level_fails() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, log_level="verbose")


@pytest.mark.parametrize("value", [0, -1, 20001])
def test_invalid_max_input_chars_fails(value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, max_input_chars=value)


@pytest.mark.parametrize("value", [0, -1, 21])
def test_invalid_top_k_fails(value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, top_k=value)


def test_blank_optional_strings_normalize_to_none() -> None:
    settings = Settings(
        _env_file=None,
        qdrant_url="   ",
        qdrant_api_key="   ",
        phoenix_endpoint="   ",
    )

    assert settings.qdrant_url is None
    assert settings.qdrant_api_key is None
    assert settings.phoenix_endpoint is None


def test_blank_required_strings_fail() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, embedding_provider="   ")


def test_startup_validation_accepts_phase_one_defaults() -> None:
    settings = Settings(_env_file=None)

    validated = validate_startup_settings(settings)

    assert validated is settings


def test_internal_production_mode_requires_non_development_env() -> None:
    settings = Settings(
        _env_file=None,
        deployment_mode="internal_production",
        app_env="development",
    )

    with pytest.raises(ValueError, match="DEPLOYMENT_MODE"):
        validate_startup_settings(settings)


def test_internal_production_mode_allows_non_development_env() -> None:
    settings = Settings(_env_file=None, deployment_mode="internal_production", app_env="staging")

    validated = validate_startup_settings(settings)

    assert validated is settings


def test_startup_validation_requires_enabled_provider_keys() -> None:
    settings = Settings(_env_file=None)

    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        validate_startup_settings(settings, require_groq=True)

    with pytest.raises(ValueError, match="QDRANT_URL"):
        validate_startup_settings(settings, require_qdrant=True)

    with pytest.raises(ValueError, match="PHOENIX_ENDPOINT"):
        validate_startup_settings(settings, require_phoenix=True)


def test_cached_settings_access_is_stable() -> None:
    first = get_settings()
    second = get_settings()

    assert first is second


def test_app_entrypoint_runs(
    capsys,
    caplog: pytest.LogCaptureFixture,
) -> None:
    built = False
    caplog.set_level(logging.INFO)

    class FakeApp:
        def launch(self) -> None:
            raise AssertionError("launch should not be called when launch=False")

    original_builder = app_ui.build_gradio_app
    original_get_settings = app_ui.get_settings

    def fake_build_gradio_app(**_kwargs):
        nonlocal built
        built = True
        return FakeApp()

    app_ui.build_gradio_app = fake_build_gradio_app
    app_ui.get_settings = lambda: Settings(
        _env_file=None,
        groq_api_key="test-groq-key",
        qdrant_url="https://qdrant.example.com",
        qdrant_api_key="test-qdrant-key",
        app_env="test",
    )
    try:
        exit_code = app_ui.main(launch=False)
    finally:
        app_ui.build_gradio_app = original_builder
        app_ui.get_settings = original_get_settings
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""
    assert built is True
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert "startup_diagnostics" in event_types
    assert "health_check_succeeded" in event_types
    assert "readiness_check_succeeded" in event_types


def test_hosted_request_smoke_path_runs_without_crashing() -> None:
    def grounded_answer_fn(*_args, **_kwargs):
        return GroundedAnswerResult(
            query="¿Qué cobertura aplica?",
            response=AdvisorDraftResponse(
                suggested_answer="Coverage applies after the waiting period.",
                documentary_basis=[],
                citations=[],
                confidence="high",
                limitations=[],
                advisor_review_notice="Advisor review required before external use.",
            ),
            verification=GroundingVerification(
                supported=True,
                confidence="high",
                unsupported_claims=[],
                missing_citations=[],
            ),
        )

    handler = app_ui.build_query_handler(
        settings=Settings(
            _env_file=None,
            groq_api_key="test-groq-key",
            qdrant_url="https://qdrant.example.com",
            qdrant_api_key="test-qdrant-key",
            app_env="test",
        ),
        grounded_answer_fn=grounded_answer_fn,
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
    ) = handler(
        "¿Qué cobertura aplica?"
    )

    assert "Coverage applies" in answer
    assert citations == "No hay citas disponibles."
    assert confidence == "HIGH"
    assert limitations == "No se registraron limitaciones adicionales."
    assert "consulta_recibida" in trace_summary
    assert "ID de solicitud: ui-" in support_context
    assert "Resultado de depuración: borrador fundamentado listo" in debug_metadata
    assert answer_quality_state == "Calidad de la respuesta — Calidad estándar del borrador."
    assert error_state == "No hay errores activos."
    assert status == "Se requiere revisión del asesor antes del uso externo."


def test_hosted_health_smoke_payload_is_callable() -> None:
    payload = build_health_status(runtime_surface="gradio_ui")

    assert payload["event_type"] == "health_check_succeeded"
    assert payload["status"] == "ok"


def test_hosted_readiness_smoke_payload_is_callable() -> None:
    payload = app_ui.build_readiness_status(
        Settings(
            _env_file=None,
            groq_api_key="test-groq-key",
            qdrant_url="https://qdrant.example.com",
            qdrant_api_key="test-qdrant-key",
            app_env="test",
        ),
        runtime_surface="gradio_ui",
        gradio_available=True,
        groq_available=True,
        qdrant_available=True,
        embedding_available=True,
    )

    assert payload["event_type"] == "readiness_check_succeeded"
    assert payload["status"] == "ready"


def test_hosted_latency_smoke_is_callable() -> None:
    payload = run_hosted_latency_smoke(latency_budget_ms=5000.0)

    assert payload["event_type"] == "hosted_latency_smoke_succeeded"
    assert payload["question_count"] == 30
    assert payload["duration_ms"] >= 0
    assert payload["latency_budget_ms"] == 5000.0


def test_hosted_latency_smoke_reports_within_budget_deterministically() -> None:
    timeline = deque([0.0, 4.0])
    run_result = EvaluationRunResult(
        run_id="local-eval:test",
        question_set_version="questions-v1",
        golden_behavior_version="golden-v1",
        retrieval_expectation_version="retrieval-v1",
        citation_expectation_version="citations-v1",
        results=[
            EvaluationQuestionResult(
                question_id=f"q-{index}",
                status="matched",
                actual_behavior="normal_answer",
                expected_behavior="normal_answer",
            )
            for index in range(30)
        ],
    )

    payload = run_hosted_latency_smoke(
        latency_budget_ms=5000.0,
        evaluation_runner=lambda: run_result,
        timer=lambda: timeline.popleft(),
    )

    assert payload["question_count"] == 30
    assert payload["duration_ms"] == 4000.0
    assert payload["within_budget"] is True


def test_hosted_latency_smoke_reports_over_budget_deterministically() -> None:
    timeline = deque([0.0, 6.25])
    run_result = EvaluationRunResult(
        run_id="local-eval:test",
        question_set_version="questions-v1",
        golden_behavior_version="golden-v1",
        retrieval_expectation_version="retrieval-v1",
        citation_expectation_version="citations-v1",
        results=[
            EvaluationQuestionResult(
                question_id=f"q-{index}",
                status="matched",
                actual_behavior="normal_answer",
                expected_behavior="normal_answer",
            )
            for index in range(30)
        ],
    )

    payload = run_hosted_latency_smoke(
        latency_budget_ms=5000.0,
        evaluation_runner=lambda: run_result,
        timer=lambda: timeline.popleft(),
    )

    assert payload["question_count"] == 30
    assert payload["duration_ms"] == 6250.0
    assert payload["within_budget"] is False


def test_hosted_citation_regression_smoke_is_callable() -> None:
    payload = run_hosted_citation_regression_smoke()

    assert payload["event_type"] == "hosted_citation_regression_smoke_succeeded"
    assert payload["question_count"] == 30
    assert payload["all_questions_covered"] is True
    assert payload["expectation_counts"] == {
        "citations_required": 6,
        "no_citations_expected": 12,
        "guardrail_citation_posture": 12,
    }
