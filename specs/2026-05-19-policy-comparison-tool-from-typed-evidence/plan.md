# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Tool Wrapper
   - Add a thin comparison tool over typed evidence and extracted clauses only.
   - Keep the wrapper independently callable and reusable.

2. Comparison Output
   - Reuse the existing comparison contracts.
   - Keep comparison behavior conservative and explicitly insufficient when
     evidence is weak.

3. Error Contract
   - Define typed failure behavior for comparison callers.
   - Treat insufficient information as a valid non-error outcome.

4. Observability Preservation
   - Preserve request correlation and structured tool execution logging.
   - Keep latency expectations visible through the current observability path.

5. Validation Coverage
   - Add tests for success, insufficient-information, and typed failure
     outcomes.
   - Cover traceability and correlated execution behavior.

6. Deferred Work Boundary
   - Stop before citation verification, drafting, and orchestration work.
