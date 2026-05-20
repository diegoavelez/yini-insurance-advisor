# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Signal Rule Definition
   - Define a small deterministic injection-signal rule set.
   - Keep the rules explicit and narrow.

2. Conservative Refusal Path
   - Add a typed refusal outcome for triggered injection signals.
   - Preserve low-confidence and review-oriented messaging.

3. Workflow and UI Boundary Preservation
   - Keep benign supported queries on the normal path.
   - Surface injection-triggered refusals through the existing response path.

4. Observability
   - Record prompt-injection guardrail decisions in structured events.
   - Preserve request correlation for guardrail outcomes.

5. Validation Coverage
   - Add tests for benign vs triggered query behavior.
   - Add tests for typed refusal and guardrail observability.
