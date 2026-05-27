# Plan — demo-runtime-and-dependency-constraints-notes

## Objective

Add narrow, durable notes covering only the hosted demo runtime and dependency
constraints.

## Affected Files

- `README.md`
- `specs/roadmap.md`
- `specs/2026-05-27-demo-runtime-and-dependency-constraints-notes/requirements.md`
- `specs/2026-05-27-demo-runtime-and-dependency-constraints-notes/plan.md`
- `specs/2026-05-27-demo-runtime-and-dependency-constraints-notes/validation.md`

## Assumptions

- The authoritative hosted path remains Hugging Face Spaces with `sdk: docker`.
- Existing container build/startup/readiness slices provide sufficient evidence
  for the documented runtime constraints.

## Risks

- Notes could drift beyond current evidence if they speculate about hosted
  behavior not yet validated.
- Notes could overlap with guardrail/scope limitations if not kept narrow.

## Verification Strategy

- Verify the documentation aligns with the current root `Dockerfile`.
- Verify the documentation aligns with the current root `README.md` Spaces
  config block and deployment procedure.
- Verify the notes remain limited to runtime/dependency constraints.

## Status

- Completed.

## Completion Notes

- Added a dedicated runtime/dependency constraints section to `README.md`.
- Kept the notes limited to:
  - Hugging Face Spaces runtime posture;
  - authoritative Docker/app entrypoint surfaces;
  - required runtime variables;
  - evidenced build/startup/readiness constraints.
