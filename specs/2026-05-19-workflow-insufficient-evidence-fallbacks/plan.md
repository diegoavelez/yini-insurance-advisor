# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Fallback Edge Definition
   - Define explicit insufficient-evidence fallback edges in the workflow.
   - Keep the fallback boundaries narrow and deterministic.

2. Conservative Outcome Preservation
   - Reuse typed workflow output for fallback results.
   - Keep confidence and limitations conservative.

3. State and Traceability
   - Preserve fallback traceability in workflow state.
   - Make fallback path visible in structured events.

4. Validation Coverage
   - Add tests for insufficient-evidence fallback routing and outputs.
   - Cover correlated fallback observability.

5. Deferred Work Boundary
   - Stop before retry logic and broader recovery policy work.
