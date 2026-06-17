# Requirements

## Title

Synchronize stale roadmap operational rollups with the already documented
completed category status.

## Context

The roadmap currently contains an internal status drift:

- the Phase 15 and Phase 16 operational category rollups still describe
  `MUEVETE LIBRE` as `partially completed`;
- the same rollups still describe `movilidad-suscripcion` as `active`;
- later in the roadmap, the Phase 18 operational rollup already records both
  category tracks as completed.

This is not a product or retrieval gap. It is a roadmap-traceability gap that
can mislead future slice selection.

## Scope

This slice should:

1. reconcile the stale Phase 15 and Phase 16 operational rollups with the
   later completed posture already documented in the roadmap;
2. record the documentation-only corrective slice in the relevant dated index;
3. add a brief note that the synchronized operational rollups now reflect the
   later completed category posture.

This slice should not:

- reopen any category ingestion or retrieval work;
- change completed-slice lists except for adding this documentation-only slice;
- alter technical implementation status beyond the stale rollup wording.

## Required Behavior

### 1. Rollup synchronization

Acceptance criteria:

- Phase 15 no longer marks `MUEVETE LIBRE` as partially completed;
- Phase 15 no longer marks `movilidad-suscripcion` as active;
- Phase 16 no longer marks `MUEVETE LIBRE` as partially completed;
- Phase 16 no longer marks `movilidad-suscripcion` as active.

### 2. Traceability

Acceptance criteria:

- the roadmap includes the dated slug
  `roadmap-operational-rollup-status-sync`;
- the slice is documented as a roadmap-only corrective sync.

### 3. Documentation-only safety

Acceptance criteria:

- the diff is limited to roadmap/spec documentation files;
- no runtime, test, ingestion, or retrieval code changes are introduced.
