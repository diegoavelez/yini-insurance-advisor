# Plan — hosted-smoke-expectations-and-operator-notes

## Objective

Add narrow hosted smoke expectations and post-deploy operator notes for the
current hosted demo deployment path.

## Affected Files

- `README.md`
- `specs/roadmap.md`
- `specs/2026-05-27-hosted-smoke-expectations-and-operator-notes/requirements.md`
- `specs/2026-05-27-hosted-smoke-expectations-and-operator-notes/plan.md`
- `specs/2026-05-27-hosted-smoke-expectations-and-operator-notes/validation.md`

## Assumptions

- The current hosted path remains Hugging Face Spaces with `sdk: docker`.
- The current container startup/readiness validations and current UI surface
  provide sufficient evidence for defining minimal hosted smoke expectations.

## Risks

- Notes could overstate hosted guarantees that have not been directly executed
  in a real Space deployment.
- Notes could drift into rollback or demo-constraint guidance if not kept
  narrow.

## Verification Strategy

- Verify the documentation aligns with the current documented deployment path,
  readiness posture, and public UI surface.
- Verify the notes remain limited to hosted smoke expectations and operator
  checks only.

## Status

- Completed.

## Completion Notes

- Added a dedicated hosted-smoke-and-operator-notes section to `README.md`.
- Kept the notes limited to minimum post-deploy expectations derived from the
  current documented deployment path, local readiness validation, and public UI
  surface.
