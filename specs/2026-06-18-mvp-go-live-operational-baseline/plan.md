# Plan — mvp-go-live-operational-baseline

## Objective

Consolidate the existing release, deployment, rollback, smoke, and operator
artifacts into one explicit go-live baseline for the current MVP.

## Likely Affected Files

- `README.md`
- `docs/evaluation-report.md`
- `docs/category-onboarding-playbook.md`
- `specs/roadmap.md`
- `specs/2026-06-18-mvp-go-live-operational-baseline/requirements.md`
- `specs/2026-06-18-mvp-go-live-operational-baseline/plan.md`
- `specs/2026-06-18-mvp-go-live-operational-baseline/validation.md`

## Assumptions

- No new runtime or corpus work is needed to define the baseline.
- The current MVP category set is already evidenced in the roadmap and smoke
  assets.
- This slice should converge documentation, not broaden scope.

## Risks

- Repeating existing documentation without creating a clearer operator path.
- Accidentally treating future category expansion as part of MVP go-live.

## Execution Steps

1. Consolidate the current MVP release and hosted-validation posture.
2. Name the supported category set for the shipped MVP.
3. Document the minimum update/rollback operator path.
4. Record the slice in the roadmap as the next follow-on operational closure.

## Verification Strategy

- Check that each go-live step already maps to an existing repo surface.
- Confirm the roadmap and README both point to the same next post-MVP slice.
