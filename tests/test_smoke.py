from app.ui import main
from core.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.top_k == 5


def test_app_entrypoint_runs(capsys) -> None:
    exit_code = main()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "foundation scaffold" in captured.out
