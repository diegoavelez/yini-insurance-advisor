from __future__ import annotations

import pytest
from pydantic import ValidationError

import app.ui as app_ui
from contracts import AdvisorDraftResponse, GroundedAnswerResult, GroundingVerification
from core.config import (
    Settings,
    clear_settings_cache,
    get_settings,
    validate_startup_settings,
)


@pytest.fixture(autouse=True)
def reset_settings_cache() -> None:
    clear_settings_cache()
    yield
    clear_settings_cache()


def test_settings_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.deployment_mode == "public_mvp_demo"
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.top_k == 5


def test_settings_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TOP_K", "7")
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DEPLOYMENT_MODE", "internal_production")

    settings = Settings(_env_file=None)

    assert settings.deployment_mode == "internal_production"
    assert settings.top_k == 7
    assert settings.app_env == "test"


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


def test_app_entrypoint_runs(capsys) -> None:
    built = False

    class FakeApp:
        def launch(self) -> None:
            raise AssertionError("launch should not be called when launch=False")

    original_builder = app_ui.build_gradio_app

    def fake_build_gradio_app(**_kwargs):
        nonlocal built
        built = True
        return FakeApp()

    app_ui.build_gradio_app = fake_build_gradio_app
    try:
        exit_code = app_ui.main(launch=False)
    finally:
        app_ui.build_gradio_app = original_builder
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""
    assert built is True


def test_hosted_request_smoke_path_runs_without_crashing() -> None:
    def grounded_answer_fn(*_args, **_kwargs):
        return GroundedAnswerResult(
            query="What is covered?",
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

    answer, citations, confidence, limitations, status = handler("What is covered?")

    assert "Coverage applies" in answer
    assert citations == "No citations available."
    assert confidence == "HIGH"
    assert limitations == "No additional limitations noted."
    assert status == "Advisor review required before external use."
