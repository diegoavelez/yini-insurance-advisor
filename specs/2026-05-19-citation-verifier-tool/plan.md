# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Tool Wrapper
   - Add a thin citation verifier over drafted text and typed cited evidence
     only.
   - Keep the wrapper independently callable and reusable.

2. Verification Output
   - Reuse existing verification contracts where possible.
   - Keep verification behavior conservative and explicitly partial or
     unsupported when evidence is weak.

3. Error Contract
   - Define typed failure behavior for verifier callers.
   - Treat weak or unsupported support as a valid non-error outcome.

4. Observability Preservation
   - Preserve request correlation and structured tool execution logging.
   - Keep latency expectations visible through the current observability path.

5. Validation Coverage
   - Add tests for success, weak-support, unsupported, and typed failure
     outcomes.
   - Cover traceability and correlated execution behavior.

6. Deferred Work Boundary
   - Stop before drafting and orchestration work.
