# Plan — phase-15-roadmap-dated-index-coherence-sync

## Objective

Make the roadmap's Phase 15 traceability internally consistent without
changing project status semantics.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-18-phase-15-roadmap-dated-index-coherence-sync/requirements.md`
- `specs/2026-06-18-phase-15-roadmap-dated-index-coherence-sync/plan.md`
- `specs/2026-06-18-phase-15-roadmap-dated-index-coherence-sync/validation.md`

## Assumptions

- The PAC slices already belong to `Phase 15`; the gap is only that they are
  missing from the dated index.
- The formatting normalization is safe because it does not alter meaning.

## Risks

- Accidentally broadening into other roadmap edits.
- Moving or renaming slice slugs that are already stable.

## Execution Steps

1. Add the missing PAC slice slugs to the `Phase 15` dated slice index.
2. Normalize the `remaining in Phase 16` through `Phase 19` line format.
3. Re-run a focused consistency check against the updated roadmap sections.

## Verification Strategy

- Compare the `Phase 15` dated and completed indices after the patch.
- Check the later `remaining in Phase ...` blocks for consistent formatting.
