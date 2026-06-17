# Validation

This slice is ready when Phase 15 has a durable evaluation report artifact that
truthfully summarizes the current deterministic evaluation posture and MVP
acceptance smoke coverage.

## Acceptance Checks

- `docs/evaluation-report.md` exists and summarizes the current evaluation
  asset set, baseline deterministic results, MVP acceptance smoke coverage, and
  scope boundaries;
- `README.md` points to the evaluation report artifact;
- `specs/roadmap.md` records the slice and the report deliverable status.

## Completion Evidence

- `./.venv/bin/python - <<'PY' ... run_local_evaluation() ... PY` reports
  `30` total results with `30` matched;
- `./.venv/bin/python - <<'PY' ... run_hosted_citation_regression_smoke() ... PY`
  reports `all_questions_covered = True`;
- `./.venv/bin/python -m pytest tests/test_evaluation_dataset.py tests/test_evaluation_runner.py tests/test_smoke.py -q`
  passes;
- the report explicitly distinguishes deterministic baseline evidence from
  fresh live Qdrant/Groq execution.
