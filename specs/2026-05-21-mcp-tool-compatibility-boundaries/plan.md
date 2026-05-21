# Plan

## Status

- Completed on `2026-05-21`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Boundary Surface
   - Define the narrow compatibility boundary for the current MCP-visible
     surface.
   - Keep it aligned with the version policy.

2. Operational Expectations
   - Add explicit forward/backward compatibility expectations.
   - Avoid runtime negotiation or broader deployment work.

3. Validation
   - Add deterministic validation for the compatibility-boundary seam.
   - Confirm the slice stops before broader runtime or deployment work.
