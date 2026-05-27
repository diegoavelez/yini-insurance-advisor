# Validation

## Status

- Completed.

## Required Checks

- the stale Spaces start artifact is removed or explicitly resolved
- `ruff check .` only if implementation changes Python files

## Required Scenarios

- The old secondary Spaces launch path is no longer implied by repo artifacts.
- The authoritative Spaces launch path remains intact.
- The slice remains scoped to cleanup only.

## Merge Readiness

This spec is ready when the repository no longer contains the stale start-command artifact that implied a second Hugging Face Spaces launch path, without drifting into entrypoint normalization, deployment docs, or hosted smoke validation.

## Executed Checks

- Verified the authoritative root `Dockerfile` still uses:
  - `CMD ["python", "-m", "app.ui"]`
- Verified `deploy/start.sh` was the only remaining stale Spaces start artifact.

## Outcome

- `deploy/start.sh` was removed.
- The old secondary Spaces launch path is no longer implied by repository
  artifacts.
- The authoritative root `Dockerfile` launch path remains intact.

## Skipped Checks

- No entrypoint normalization beyond stale-artifact cleanup was attempted.
- No hosted deployment validation was attempted.
