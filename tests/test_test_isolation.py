"""Exercise test configuration in a fresh process with invented inputs only."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_settings_are_isolated_during_collection_and_execution(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    conftest = repository / "tests" / "conftest.py"
    if conftest.exists():
        (tmp_path / "conftest.py").write_text(conftest.read_text(encoding="utf-8"))
    (tmp_path / ".env").write_text(
        "TOP_K=19\nGROQ_API_KEY=invented-dotenv-key\n"
        "QDRANT_API_KEY=invented-dotenv-key\nQDRANT_URL=https://dotenv.example.invalid\n",
        encoding="utf-8",
    )
    (tmp_path / "test_probe.py").write_text(
        "from core.config import Settings, clear_settings_cache, get_settings\n"
        "collected = get_settings()\n"
        "assert collected.top_k == 5\n"
        "assert collected.app_env == 'development'\n"
        "assert collected.groq_api_key is None\n"
        "assert collected.qdrant_api_key is None\n"
        "assert collected.qdrant_url is None\n"
        "def test_runtime(monkeypatch):\n"
        "    clear_settings_cache()\n"
        "    current = get_settings()\n"
        "    assert current.top_k == 5\n"
        "    assert current.groq_api_key is None\n"
        "    assert current.qdrant_api_key is None\n"
        "    assert current.qdrant_url is None\n"
        "    assert current is get_settings()\n"
        "    monkeypatch.setenv('TOP_K', '7')\n"
        "    clear_settings_cache()\n"
        "    assert get_settings().top_k == 7\n"
        "    assert Settings(_env_file=None).top_k == 7\n",
        encoding="utf-8",
    )
    environment = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(tmp_path),
        "TMPDIR": str(tmp_path),
        "PYTHONPATH": str(repository),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "TOP_K": "18",
        "APP_ENV": "production",
        "GROQ_API_KEY": "invented-inherited-key",
        "QDRANT_API_KEY": "invented-inherited-key",
        "QDRANT_URL": "https://inherited.example.invalid",
    }
    # No inherited values are copied, including credentials unrelated to Settings.
    result = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-p", "no:cacheprovider", "-q",
         "--basetemp", str(tmp_path / "pytest-tmp"), "test_probe.py"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_local_retrieval_collection_and_execution_do_not_read_corpus(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[1]
    for name in ("conftest.py", "test_retrieval.py", "test_corpus_evaluation.py",
                 "test_evaluation_dataset.py"):
        source = repository / "tests" / name
        if source.exists():
            (tmp_path / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    # The audit boundary is installed before pytest imports conftest/test modules.
    # Every data path is forbidden, including absent temporary dataset paths.
    probe = (
        "import sys, pathlib\n"
        "def guard(event, args):\n"
        "    if event in ('open', 'os.listdir', 'os.scandir'):\n"
        "        value = args[0]\n"
        "        if isinstance(value, (str, bytes)):\n"
        "            candidate = pathlib.Path(value).resolve()\n"
        "            if 'data' in candidate.parts or candidate.name == '.env':\n"
        "                raise AssertionError('FORBIDDEN_DATA_READ')\n"
        "    if event in ('socket.connect', 'socket.getaddrinfo'):\n"
        "        raise AssertionError('FORBIDDEN_NETWORK')\n"
        "sys.addaudithook(guard)\n"
        "import pytest\n"
        "raise SystemExit(pytest.main(sys.argv[1:]))\n"
    )
    environment = {
        "PATH": "/usr/bin:/bin", "HOME": str(tmp_path), "TMPDIR": str(tmp_path),
        "PYTHONPATH": str(repository), "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    }
    common = [sys.executable, "-B", "-c", probe, "-p", "no:cacheprovider",
              "--basetemp", str(tmp_path / "pytest-tmp"), "-q"]
    collection = subprocess.run(
        [*common, "--collect-only", "."], cwd=tmp_path, env=environment,
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert collection.returncode == 0, collection.stdout + collection.stderr
    execution = subprocess.run(
        [*common, ".", "-k",
         "invented_queries_normalize_to_expected_filters or "
         "retrieve_ranked_chunks_maps_search_hits_in_ranked_order or "
         "retrieve_cli_prints_typed_result"],
        cwd=tmp_path, env=environment, capture_output=True, text=True,
        timeout=30, check=False,
    )
    assert execution.returncode == 0, execution.stdout + execution.stderr
    assert "4 passed" in execution.stdout
