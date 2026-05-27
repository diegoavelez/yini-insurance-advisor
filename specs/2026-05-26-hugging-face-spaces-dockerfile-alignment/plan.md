# Plan

## Status

- Completed.

1. Artifact Inspection
   - Inspect the current root and `deploy/` Dockerfiles.
   - Determine which one should be authoritative for Hugging Face Spaces.

2. Alignment Change
   - Apply the minimal repository change needed to remove ambiguity.
   - Keep the scope limited to Dockerfile artifact alignment.

3. Documentation
   - Update validation notes with the selected Dockerfile artifact.
   - Defer start-command alignment to the next slice.

## Completion Notes

- Inspected both candidate launch artifacts:
  - root `Dockerfile`
  - `deploy/Dockerfile`
- Selected the root `Dockerfile` as the authoritative Hugging Face Spaces
  launch artifact because it is the only Dockerfile already validated through:
  - local image build
  - local container startup
  - local container readiness checks
- Removed `deploy/Dockerfile` to eliminate repository ambiguity for the
  `sdk: docker` Spaces runtime.
- Deferred start-command normalization to the next slice.
