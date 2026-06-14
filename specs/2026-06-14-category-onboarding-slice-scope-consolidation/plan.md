# Plan

## Objective

Reduce future spec-bundle sprawl during category onboarding by tightening the
documented slicing policy and making the roadmap easier to scan.

## Affected Files

- `docs/category-onboarding-playbook.md`
- `specs/roadmap.md`
- `specs/2026-06-14-category-onboarding-slice-scope-consolidation/requirements.md`
- `specs/2026-06-14-category-onboarding-slice-scope-consolidation/plan.md`
- `specs/2026-06-14-category-onboarding-slice-scope-consolidation/validation.md`

## Assumptions

- the current baseline onboarding flow is still correct;
- the main issue is post-onboarding remediation granularity, not the existence
  of specs themselves.

## Risks

- over-correcting into slices that are too broad to validate cleanly;
- making the roadmap shorter but less traceable.

## Steps

1. Rewrite the playbook policy around root-cause-sized bundle boundaries.
2. Add an explicit active-bundle cap and default bundle families per category.
3. Add compact cohort rollups in the roadmap and relabel the long slug lists as
   traceability indexes.

## Verification Strategy

- inspect the updated playbook rules for bundle-boundary language;
- inspect the roadmap for the new rollup summary and index wording;
- confirm no historical slice status is changed by the consolidation.
