# Plan

## Status

- Completed on `2026-05-21`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Policy Surface
   - Define the narrow MCP interface version policy.
   - Keep it tied to the current exposed surface.

2. Operational Rules
   - Add explicit naming and bump rules.
   - Avoid detailed compatibility-matrix work.

3. Validation
   - Add deterministic validation for the version policy seam.
   - Confirm the slice stops before compatibility-boundary work.
