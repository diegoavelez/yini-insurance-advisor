# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Tool Wrapper
   - Add a thin drafting tool over typed upstream inputs only.
   - Keep the wrapper independently callable and reusable.

2. Draft Output
   - Reuse the existing advisor response contract.
   - Keep draft behavior conservative and explicitly limited when evidence is
     weak.

3. Error Contract
   - Define typed failure behavior for draft callers.
   - Treat insufficient information as a valid non-error outcome.

4. Observability Preservation
   - Preserve request correlation and structured tool execution logging.
   - Keep latency expectations visible through the current observability path.

5. Validation Coverage
   - Add tests for success, insufficient-information, and typed failure
     outcomes.
   - Cover traceability and correlated execution behavior.

6. Deferred Work Boundary
   - Stop before LangGraph orchestration work.
