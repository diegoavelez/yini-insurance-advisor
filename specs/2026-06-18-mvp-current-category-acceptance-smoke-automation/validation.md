# Validation

This slice is ready when the currently accepted corpus is represented by a
typed smoke asset and a deterministic runner rather than only by manual matrix
notes.

## Acceptance Checks

- the new spec bundle exists;
- `data/eval/mvp-acceptance-smokes.json` exists and loads into typed contracts;
- the deterministic smoke runner returns typed per-case results from injected
  retrieval and grounded-answer callables;
- focused tests cover both matched and mismatched smoke outcomes;
- the roadmap records the new smoke automation state.

## Completion Evidence

- `./.venv/bin/python -m pytest tests/test_evaluation_dataset.py tests/test_evaluation_runner.py -q`
  passes;
- `./.venv/bin/python -m ruff check contracts/evaluation.py core/evaluation_dataset.py core/evaluation_runner.py tests/test_evaluation_dataset.py tests/test_evaluation_runner.py --ignore E501`
  passes;
- the committed smoke dataset mirrors the accepted category set from
  `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`;
- the roadmap no longer relies on the manual matrix alone to describe the
  current MVP acceptance posture.
