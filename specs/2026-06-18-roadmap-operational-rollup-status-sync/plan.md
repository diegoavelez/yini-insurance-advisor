# Plan

## Objective

Remove stale status drift inside the roadmap so early operational rollups match
the later authoritative completed category posture.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-18-roadmap-operational-rollup-status-sync/requirements.md`
- `specs/2026-06-18-roadmap-operational-rollup-status-sync/validation.md`

## Assumptions

- the later Phase 18 operational rollup is the authoritative status source for
  the current category posture;
- no implementation work is needed because the categories were already closed
  in prior slices.

## Risks

- updating the wrong rollup lines could create a different inconsistency;
- broad roadmap edits could exceed the intended documentation-only scope.

## Steps

1. Confirm the stale Phase 15 and Phase 16 operational rollup lines.
2. Add a dated documentation-only spec bundle for the sync slice.
3. Update the stale rollup entries so they match the later completed posture.
4. Review the diff to ensure the slice remains documentation-only.

## Verification Strategy

- manually compare the synchronized Phase 15/16 rollups against the later
  completed Phase 18 rollup;
- review `git diff --stat` to confirm only roadmap/spec files changed.
