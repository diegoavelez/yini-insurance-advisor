# Requirements

## Status

- Drafted.

## Objective

Add the next `Phase 14` deployment slice by aligning the repository's Docker launch artifact with the configured Hugging Face Spaces runtime.

## Scope

This slice must cover only:

- selecting the repository-side Dockerfile artifact that should represent the Spaces launch surface;
- removing or reconciling ambiguity between the current Docker build files for the Spaces target;
- explicit alignment between the chosen Spaces runtime config and the selected Dockerfile.

This slice must not include:

- start-command normalization work;
- broader deployment guide prose;
- rollback notes;
- hosted smoke validation.

## Functional Requirements

1. Dockerfile Selection
   - Identify which Dockerfile should be the authoritative launch artifact for Hugging Face Spaces.
   - The selected artifact must align with the current `sdk: docker` Spaces runtime config.

2. Ambiguity Removal
   - Resolve the current ambiguity between the root `Dockerfile` and `deploy/Dockerfile` for the Spaces target.
   - The repo should clearly indicate which Dockerfile the Spaces deployment is expected to use.

3. Narrow Artifact Alignment
   - Keep the change limited to Dockerfile artifact alignment.
   - Do not normalize start commands or broader deployment behavior in this slice.

## Acceptance Criteria

- The repo clearly identifies one Dockerfile artifact as the Spaces launch surface.
- The selection is consistent with the current Spaces runtime config in `README.md`.
- The slice remains scoped to Dockerfile alignment only.
