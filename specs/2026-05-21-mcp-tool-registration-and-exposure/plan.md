# Plan

## Status

- Completed on `2026-05-21`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Tool Surface
   - Select a narrow initial MCP-visible tool set.
   - Keep mapping anchored to existing local seams.

2. Registration
   - Add explicit server-side tool registration and metadata.
   - Avoid client-roundtrip behavior in this slice.

3. Validation
   - Add deterministic validation for exposed tool metadata.
   - Confirm the slice stops before MCP client integration.
