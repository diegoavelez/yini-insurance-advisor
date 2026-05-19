# Plan

## Status

- Completed on `2026-05-18`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Tool Wrapper
   - Add a thin retrieval tool wrapper over the current retrieval seam.
   - Keep the wrapper reusable and independently callable.

2. Error Contract
   - Define the typed retrieval-tool failure surface.
   - Distinguish expected tool failure classes without inventing new runtime behavior.

3. Observability Preservation
   - Preserve request correlation and structured tool execution logging.
   - Keep latency expectations visible through the existing observability path.

4. Validation Coverage
   - Add tests for success, empty-result, and typed failure outcomes.
   - Cover correlated execution behavior when request ids are provided.

5. Deferred Work Boundary
   - Stop before clause extraction, comparison, citation verification, and
     drafting tools.
