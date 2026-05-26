# Validation

## Status

- Completed.

## Required Checks

- one local container startup for the readiness check
- one explicit local readiness check command against the running container
- `ruff check .` only if implementation changes Python files

## Required Scenarios

- The local container reaches a ready state for the current app surface.
- The readiness check command is captured explicitly.
- The slice remains scoped to readiness validation only.

## Merge Readiness

This spec is ready when the locally built image has been validated through one successful local readiness check against the running app surface, with the exact readiness command captured, without drifting into hosted deployment or broader operations work.

## Executed Checks

- `docker run -d --name yini-readiness-check-<timestamp> -p 7861:7860 -e GROQ_API_KEY=dummy -e QDRANT_URL=http://qdrant:6333 -e QDRANT_API_KEY=dummy yini-insurance-advisor:local`
- `curl -sfI http://127.0.0.1:7861/`

## Outcome

- The temporary validation container reached and remained in `running` state.
- The readiness probe returned `HTTP/1.1 200 OK`.
- Container logs also showed the app's internal readiness event:
  - `readiness_check_succeeded`
- The container was removed after inspection.

## Skipped Checks

- No hosted deployment validation was attempted.
- No broader rollback or operator documentation work was added.
