# Plan

## Status

- Completed on `2026-05-21`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Client Seam
   - Define the narrow local MCP client seam.
   - Keep it aligned with the current server contract.

2. Roundtrip
   - Add end-to-end local roundtrip over the registered MCP surface.
   - Avoid interface-versioning work in this slice.

3. Validation
   - Add deterministic validation for initialize, list, and call roundtrip.
   - Confirm the slice stops before interface versioning.
