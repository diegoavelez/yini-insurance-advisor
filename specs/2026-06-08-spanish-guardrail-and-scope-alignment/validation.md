# Validation

## Status

- Completed on `2026-06-08`.
- Checks passed:
  - `./.venv/bin/python -m ruff check core/query_scope.py core/prompt_guardrails.py tests/test_query_scope.py tests/test_prompt_guardrails.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_dspy_query_classification.py`
  - `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_prompt_guardrails.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py tests/test_dspy_query_classification.py -q`

## Required Checks

- `./.venv/bin/python -m ruff check core/query_scope.py core/prompt_guardrails.py tests/test_query_scope.py tests/test_prompt_guardrails.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py`
- `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_prompt_guardrails.py tests/test_app_ui.py tests/test_guardrail_abuse_cases.py -q`

## Required Scenarios

- Spanish insurance-document queries classify as supported where appropriate.
- Spanish prompt-injection formulations trigger conservative refusal.
- Existing English deterministic supported/refusal paths still pass.
- The slice remains scoped away from evaluation-dataset changes.

## Merge Readiness

This spec is ready when the deterministic Spanish scope and guardrail slice is
decision-complete for:

- Spanish supported-scope token coverage;
- Spanish prompt-injection signal coverage;
- preserved typed decisions and existing event surfaces.
