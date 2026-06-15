# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving artifact assembly and per-document
reuse policy behind a dedicated `rag` seam while preserving ingestion and
embedding behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/ingestion_artifacts.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction/requirements.md`
- `specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction/plan.md`
- `specs/2026-06-15-rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction/validation.md`

## Assumptions

- The current ingestion tests encode the intended bundle-construction and skip
  policy behavior.
- Recent fixes to chunk emission and legacy-artifact skipping should be
  preserved exactly.
- Keeping command orchestration in `rag/ingestion.py` preserves the intended
  seam boundary for now.

## Risks

- Moving bundle helpers can accidentally break test-time `monkeypatch`
  behavior if wrappers are not preserved.
- Small compatibility-check changes can alter when `overwrite=false` skips or
  regenerates artifacts.

## Verification Strategy

- Run focused ingestion tests covering chunk bundles, metadata propagation,
  skip behavior, and stale-artifact refresh.
- Run focused lint on touched files.
- Preserve `monkeypatch` compatibility through thin wrappers where tests rely
  on patching `rag.ingestion` names.
