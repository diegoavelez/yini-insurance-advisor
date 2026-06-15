# Plan

## Objective

Create a narrow, operationally focused spec bundle that redirects work toward
MVP acceptance of the categories already onboarded in the current corpus and
defers non-blocking coupling refactors until that acceptance pass is complete.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/requirements.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/plan.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/validation.md`

## Assumptions

- The current roadmap status for `MOVILIDAD`, `ARL`, and `EPS/PAC` is already
  accurate enough to define the MVP acceptance surface.
- The remaining coupling slices are structural improvements, not current
  blockers, unless live MVP validation proves otherwise.
- The category-onboarding playbook is the correct contract for what counts as
  "ready" or "accepted" at the category level.

## Risks

- If the current category inventory is misstated, the acceptance matrix will
  start from the wrong scope.
- If the acceptance gates are too vague, the team may keep claiming readiness
  without comparable evidence across categories.

## Verification Strategy

- Update the roadmap so the next execution focus clearly points to MVP
  acceptance of current categories.
- Make the deferred status of remaining coupling slices explicit.
- Ensure the acceptance matrix uses the same operational readiness gates
  already documented in `docs/category-onboarding-playbook.md`.
- Define an execution-ready category matrix with representative retrieval and
  grounded-answer queries plus expected primary evidence families.
