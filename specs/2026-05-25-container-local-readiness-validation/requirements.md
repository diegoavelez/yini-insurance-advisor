# Requirements

## Status

- Drafted.

## Objective

Add the next `Phase 14` deployment slice by validating the current readiness surface from a successfully started local container.

## Scope

This slice must cover only:

- local readiness validation for the current started container image;
- explicit confirmation that the app's current readiness surface is reachable and succeeds;
- narrow capture of the exact readiness check command used during validation.

This slice must not include:

- new container startup validation work;
- Hugging Face Spaces or other hosted deployment wiring;
- broader deployment docs or rollback guidance.

## Functional Requirements

1. Local Readiness Validation
   - Start a temporary container from the validated local image as needed for the check.
   - Execute one narrow readiness check against the running container's current public surface.

2. Narrow Readiness Contract
   - The slice must confirm that the current app surface reports ready after startup.
   - The slice must stop before broader hosted smoke or deployment work.

3. Documentation of Readiness Command
   - The exact local readiness check command used for validation must be captured in the slice validation notes.

4. Narrowness
   - No hosted deployment configuration, rollback notes, or broader operating guidance should be added in this slice.

## Acceptance Criteria

- The locally started container satisfies one explicit readiness validation check.
- The readiness command is documented in the slice validation notes.
- The slice remains scoped to readiness validation only.
