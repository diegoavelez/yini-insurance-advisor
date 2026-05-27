# Plan — deployment-rollback-notes

## Objective

Add narrow, durable rollback notes for the current hosted demo deployment path.

## Affected Files

- `README.md`
- `specs/roadmap.md`
- `specs/2026-05-27-deployment-rollback-notes/requirements.md`
- `specs/2026-05-27-deployment-rollback-notes/plan.md`
- `specs/2026-05-27-deployment-rollback-notes/validation.md`

## Assumptions

- The current hosted path remains Hugging Face Spaces with `sdk: docker`.
- A rollback is operationally equivalent to pushing or restoring a previously
  known-good repo state to the Space repository.

## Risks

- Notes could overstate rollback guarantees that have not been hosted-tested.
- Notes could drift into hosted smoke expectations if not kept narrow.

## Verification Strategy

- Verify the documentation aligns with the current documented Spaces deployment
  path.
- Verify the notes remain limited to rollback guidance only.

## Status

- Completed.

## Completion Notes

- Added a dedicated rollback-notes section to `README.md`.
- Kept the guidance limited to reverting the hosted demo by restoring a
  previously known-good repo state for the current Hugging Face Spaces path.
