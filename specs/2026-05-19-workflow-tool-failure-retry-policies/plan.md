# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Retry Boundary Definition
   - Define which workflow stages allow bounded retries.
   - Keep retry scope narrow and deterministic.

2. Typed Retry Execution
   - Add bounded retry execution for selected retryable failures.
   - Preserve immediate failure for non-retryable conditions.

3. Terminal Failure Preservation
   - Return typed workflow failure after retry exhaustion.
   - Preserve existing workflow contracts for callers.

4. State and Observability
   - Record retry attempts and exhaustion in structured events.
   - Keep retry behavior traceable by request id and workflow state.

5. Validation Coverage
   - Add tests for retry success, retry exhaustion, and non-retryable failure.
   - Cover structured retry and terminal-failure observability.
