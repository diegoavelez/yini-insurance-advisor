# Plan

## Objective

Turn the current evaluation assets and deterministic baseline results into a
durable Phase 15 report artifact that is useful for operators and reviewers.

## Affected Files

- `README.md`
- `docs/evaluation-report.md`
- `specs/roadmap.md`
- `specs/2026-06-18-phase-15-evaluation-report-baseline/requirements.md`
- `specs/2026-06-18-phase-15-evaluation-report-baseline/validation.md`

## Assumptions

- the committed datasets and deterministic runners already form the factual
  basis of the baseline report;
- a documentation artifact is sufficient for this slice, without needing a new
  report-generation tool.

## Risks

- overstating what the deterministic assets prove about fresh live runtime
  behavior;
- duplicating roadmap notes without producing a more useful report surface;
- omitting the current MVP exclusions and scope boundaries.

## Steps

1. Add a dated spec bundle for the evaluation-report baseline slice.
2. Create a durable evaluation report in `docs/` from the current datasets,
   deterministic baseline results, and accepted-category smoke coverage.
3. Link the new artifact from the README.
4. Sync the roadmap so Phase 15 explicitly records the report artifact.
5. Review the final diff for evidence fidelity and scope discipline.

## Verification Strategy

- execute the deterministic local evaluation runner and hosted citation smoke;
- run the focused evaluation/smoke test set used by this slice;
- review the report text against the committed dataset versions and counts.
