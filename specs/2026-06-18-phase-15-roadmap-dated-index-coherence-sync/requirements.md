# Requirements — phase-15-roadmap-dated-index-coherence-sync

## Context

The roadmap is globally consistent about all phases being complete, but the
`Phase 15` traceability surfaces are not fully aligned internally. Its `Dated
Slice Index` omits several PAC-related slices that already appear in the
`Completed slice index`, which weakens the roadmap's role as a complete
historical index.

There is also a minor formatting inconsistency in later phases where
`remaining in Phase ...` headings do not use the same bullet style as earlier
phases.

## Goal

Restore roadmap coherence by synchronizing the `Phase 15` dated slice index
with the already completed PAC slices and by normalizing the minor `remaining`
formatting across later phases.

## In Scope

- add missing completed PAC slice slugs to the `Phase 15` dated slice index;
- normalize the `remaining in Phase 16` through `Phase 19` formatting to match
  the earlier phase style;
- keep the fix strictly documentation-only.

## Out of Scope

- changing phase completion claims;
- reclassifying slices across phases;
- modifying runtime code, tests, or operational posture.

## Acceptance Criteria

1. Every PAC slice listed in the `Phase 15` completed index also appears in the
   `Phase 15` dated slice index.
2. The `remaining in Phase 16` through `Phase 19` headings use the same bullet
   style as earlier phases.
3. The roadmap remains truthful about all phases being complete.
