# Plan

## Objective

Turn the closed manual MVP category-acceptance matrix into a typed,
deterministic smoke asset plus runner so the accepted corpus has regression
protection.

## Affected Files

- `contracts/evaluation.py`
- `core/evaluation_dataset.py`
- `core/evaluation_runner.py`
- `data/eval/mvp-acceptance-smokes.json`
- `tests/test_evaluation_dataset.py`
- `tests/test_evaluation_runner.py`
- `specs/roadmap.md`
- `specs/2026-06-18-mvp-current-category-acceptance-smoke-automation/requirements.md`
- `specs/2026-06-18-mvp-current-category-acceptance-smoke-automation/validation.md`

## Assumptions

- the current acceptance matrix is now accurate enough to serve as the source
  for a committed smoke asset;
- deterministic tests should validate contract logic through injected callables,
  not live Qdrant/Groq execution;
- the existing evaluation module is the correct home for this smoke asset.

## Risks

- overfitting the smoke asset to one exact citation layout instead of evidence
  family boundaries;
- duplicating matrix data inconsistently if the smoke asset diverges;
- pulling live-runtime concerns into local deterministic tests.

## Steps

1. Add typed contracts and a committed acceptance-smoke dataset.
2. Implement the deterministic smoke runner with injected runtime callables.
3. Add focused dataset and runner tests for matched and mismatched outcomes.
4. Sync the roadmap from manual-only acceptance toward smoke-backed
   acceptance.
5. Run targeted validation.

## Verification Strategy

- run focused evaluation dataset and runner tests;
- run Ruff on touched files;
- manually confirm the dataset mirrors the accepted category set from the
  matrix.
