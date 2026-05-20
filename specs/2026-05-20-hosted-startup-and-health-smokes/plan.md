# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Startup Smoke Definition
   - Define the narrow hosted-like startup smoke over the current app entrypoint.
   - Reuse the current startup path instead of adding deployment-specific code.

2. Health Smoke Coverage
   - Add narrow health/readiness smoke coverage over the current observability seam.
   - Keep the checks deterministic and locally executable.

3. Validation
   - Add local tests for startup and health smokes.
   - Keep verification scoped to startup/health only.
