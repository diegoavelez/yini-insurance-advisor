# Requirements

## Status

- Drafted.

## Objective

Add the next `Phase 14` deployment slice by removing or explicitly resolving stale start-command artifacts that still imply a second Hugging Face Spaces launch path.

## Scope

This slice must cover only:

- identifying stale start-command artifacts related to the old Spaces launch path;
- removing or explicitly resolving those artifacts;
- preserving the currently selected authoritative Spaces launch path.

This slice must not include:

- new entrypoint normalization work;
- Dockerfile selection work;
- broader deployment docs or rollback notes;
- hosted smoke validation.

## Functional Requirements

1. Stale Artifact Identification
   - Inspect the current deployment artifacts for any remaining file that implies a second Spaces launch path.
   - The cleanup target must be directly related to start-command ambiguity.

2. Narrow Cleanup
   - Remove or explicitly resolve the stale artifact while preserving the selected Spaces launch path.
   - The cleanup must not alter broader runtime behavior beyond resolving artifact ambiguity.

3. Narrowness
   - Stop after stale-artifact cleanup.
   - Entry-point normalization belongs to the next slice.

## Acceptance Criteria

- The repo no longer contains the stale start-command artifact that implied a second Spaces launch path.
- The authoritative Spaces launch path remains intact.
- The slice remains scoped to cleanup only.
