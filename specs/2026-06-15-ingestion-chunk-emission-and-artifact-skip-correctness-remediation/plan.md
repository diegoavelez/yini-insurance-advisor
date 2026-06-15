# Plan

## Objective

Fix the current ingestion regressions around chunk emission, overlap splitting,
and legacy-artifact skipping while keeping the recent seam extractions intact.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-15-ingestion-chunk-emission-and-artifact-skip-correctness-remediation/requirements.md`
- `specs/2026-06-15-ingestion-chunk-emission-and-artifact-skip-correctness-remediation/plan.md`
- `specs/2026-06-15-ingestion-chunk-emission-and-artifact-skip-correctness-remediation/validation.md`

## Assumptions

- The existing failing ingestion tests encode the intended contract.
- The recent `rag` seam modules should remain unchanged unless a bug fix
  clearly belongs there.
- Legacy artifacts without metadata should remain reusable unless the operator
  explicitly asks for refreshed metadata through the overlay path.

## Risks

- Chunking changes can alter downstream chunk counts and section-context
  surfaces.
- Skip-logic changes can accidentally retain truly stale artifacts if the
  compatibility rule is too permissive.

## Verification Strategy

- Re-run the six failing ingestion tests first.
- Re-run a broader focused ingestion subset covering chunk emission and skip
  behavior.
- Run focused lint on touched files.
