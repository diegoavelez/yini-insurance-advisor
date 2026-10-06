"""Keep test settings independent from developer dotenv and inherited values."""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest

from core.config import Settings, clear_settings_cache

# Conftest is loaded before test modules; an autouse fixture alone is too late
# for Settings instances created during collection.
_original_env_file = Settings.model_config["env_file"]
_settings_environment = {
    name: value for name, value in os.environ.items()
    if name.casefold() in Settings.model_fields
}
for _name in _settings_environment:
    os.environ.pop(_name)
Settings.model_config["env_file"] = None
clear_settings_cache()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-corpus-evaluation", action="store_true", default=False,
        help="Run real dataset/corpus checks only with separate source authorization.",
    )


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    if (collection_path.name in {"test_corpus_evaluation.py", "test_evaluation_dataset.py"}
            and not config.getoption("--run-corpus-evaluation")):
        return True
    return None


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    for item in items:
        if item.path.name == "test_evaluation_dataset.py":
            item.add_marker(pytest.mark.corpus_evaluation)
    if config.getoption("--run-corpus-evaluation"):
        return
    local_items = []
    corpus_items = []
    for item in items:
        (corpus_items if item.get_closest_marker("corpus_evaluation") else local_items).append(item)
    config.hook.pytest_deselected(items=corpus_items)
    items[:] = local_items


@pytest.fixture(autouse=True)
def isolate_settings(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for name in tuple(os.environ):
        if name.casefold() in Settings.model_fields:
            monkeypatch.delenv(name)
    clear_settings_cache()
    yield
    clear_settings_cache()


def pytest_unconfigure() -> None:
    Settings.model_config["env_file"] = _original_env_file
    clear_settings_cache()
    os.environ.update(_settings_environment)
