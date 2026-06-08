# Validation

## Status

- Completed on `2026-06-08`.
- Checks passed:
  - `./.venv/bin/python -m ruff check core/evaluation_dataset.py core/evaluation_runner.py tests/test_evaluation_dataset.py tests/test_optimization_dataset.py tests/test_query_classification_quality.py tests/test_query_classification_improvement.py tests/test_query_classification_latency.py tests/test_hosted_query_classification_latency.py tests/test_query_classification_latency_budget.py tests/test_query_classification_cost.py tests/test_smoke.py`
  - `./.venv/bin/python -m pytest tests/test_evaluation_dataset.py tests/test_optimization_dataset.py tests/test_query_classification_quality.py tests/test_query_classification_improvement.py tests/test_query_classification_latency.py tests/test_hosted_query_classification_latency.py tests/test_query_classification_latency_budget.py tests/test_query_classification_cost.py tests/test_smoke.py -q`

## Required Checks

- `./.venv/bin/python -m ruff check core/evaluation_dataset.py core/evaluation_runner.py tests/test_evaluation_dataset.py tests/test_optimization_dataset.py tests/test_query_classification_quality.py tests/test_smoke.py`
- `./.venv/bin/python -m pytest tests/test_evaluation_dataset.py tests/test_optimization_dataset.py tests/test_query_classification_quality.py tests/test_smoke.py -q`

## Required Scenarios

- The curated evaluation dataset remains 30 questions with unchanged category balance.
- The translated optimization subset stays exactly aligned to the evaluation prompts.
- Local evaluation still marks current assets as matched.
- Hosted-like smoke still succeeds with Spanish-facing fixture coverage.

## Merge Readiness

This spec is ready when the Spanish evaluation-fixture slice is decision-complete for:

- Spanish-facing curated evaluation prompts;
- preserved expectation alignment across linked datasets;
- passing local evaluation and hosted-like smoke coverage.
