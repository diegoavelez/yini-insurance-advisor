# Validation

## Status

- Completed.

## Required Checks

- one local container startup command against the validated image
- `ruff check .` only if implementation changes Python files

## Required Scenarios

- The local container can start the current app entrypoint.
- The startup command is captured explicitly.
- The slice remains scoped to startup validation only.

## Merge Readiness

This spec is ready when the locally built image has been validated through one successful local container startup using the current app entrypoint, with the exact startup command captured, without drifting into readiness or hosted deployment work.

## Executed Checks

- `docker run -d --name yini-startup-check-<timestamp> -e GROQ_API_KEY=dummy -e QDRANT_URL=http://qdrant:6333 -e QDRANT_API_KEY=dummy yini-insurance-advisor:local`

## Outcome

- The temporary validation container reached `running` state.
- Container logs showed the app process launched and Gradio bound to
  `http://0.0.0.0:7860`.
- The container was removed after inspection.

## Skipped Checks

- No explicit readiness probe was executed as part of this slice.
- No hosted deployment validation was attempted.
