# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Scope Boundary Definition
   - Define deterministic unsupported-query scope boundaries.
   - Keep the scope policy narrow and explicit.

2. Conservative Refusal Path
   - Add a typed refusal outcome for unsupported queries.
   - Preserve low-confidence and review-oriented messaging.

3. Workflow and UI Boundary Preservation
   - Keep supported queries on the normal path.
   - Surface refusal cleanly through the existing response path.

4. Observability
   - Record refusal decisions in structured events.
   - Preserve request correlation for refusal outcomes.

5. Validation Coverage
   - Add tests for supported vs unsupported behavior.
   - Add tests for typed refusal and refusal observability.
