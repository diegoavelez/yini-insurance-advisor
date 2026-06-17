# Plan — phase-15-final-test-release-baseline

## Objective

Turn the repository's existing tests and smoke assets into one explicit MVP
release-verification baseline.

## Likely Affected Files

- `Makefile`
- `README.md`
- `docs/evaluation-report.md`
- `specs/roadmap.md`
- `specs/2026-06-18-phase-15-final-test-release-baseline/requirements.md`
- `specs/2026-06-18-phase-15-final-test-release-baseline/plan.md`
- `specs/2026-06-18-phase-15-final-test-release-baseline/validation.md`

## Assumptions

- The repo already contains enough focused coverage to define a release gate
  without inventing a large new suite.
- The final baseline should prefer deterministic local checks over fresh live
  provider calls.
- A small helper command such as `make test-release` is acceptable if it
  reduces ambiguity without broadening scope.

## Risks

- Choosing a gate that is too broad and slow for practical release use.
- Choosing a gate that is too narrow and misses a critical MVP surface.
- Duplicating information already present in `docs/evaluation-report.md` or the
  README instead of clarifying it.

## Execution Steps

1. Inventory the current deterministic release-relevant checks.
2. Select the minimum release-gate subset for the current MVP.
3. Document the baseline and, if needed, add one minimal helper target.
4. Update roadmap traceability and verify the documented commands are runnable.

## Verification Strategy

- Confirm every release-gate command already exists or is introduced minimally.
- Run the final documented subset if implementation proceeds beyond the spec.
- Verify the roadmap clearly marks the slice as pending until implemented.
