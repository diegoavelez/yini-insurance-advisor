# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- `./.venv/bin/python -m ruff check core/config.py tests/test_smoke.py`
- `./.venv/bin/python -m pytest tests/test_smoke.py -q`

## Required Scenarios

- Default settings resolve `groq_model` to `openai/gpt-oss-120b`.
- Hosted runtime contract notes include `GROQ_MODEL` in the minimum startup
  surface.
- No focused smoke/config regressions are introduced by the default change.

## Merge Readiness

This spec is ready when the default Groq runtime identifier, the hosted README
contract, and focused smoke/config coverage all agree on the same supported
model id.

## Evidence

- `./.venv/bin/python -m ruff check core/config.py tests/test_smoke.py`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ./.venv/bin/python -m pytest tests/test_smoke.py::test_settings_defaults tests/test_smoke.py::test_settings_env_override -q`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ./.venv/bin/python -m pytest tests/test_smoke.py::test_startup_validation_accepts_phase_one_defaults -q`
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 ./.venv/bin/python -m pytest tests/test_smoke.py -q`

## Recorded Outcome

- `Settings.groq_model` now defaults to `openai/gpt-oss-120b`.
- Hosted operator-facing startup notes now include `GROQ_MODEL` anywhere the
  minimum runtime variable surface is listed.
- Focused config/startup tests covering the changed behavior passed.
- The broader `tests/test_smoke.py` file still contains one pre-existing
  failure unrelated to this slice:
  - `test_hosted_latency_smoke_is_callable`
  - observed outcome: `payload["within_budget"]` was `False` instead of `True`.
