# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Guardrail Boundary Definition
   - Define where confidence consistency is enforced in the response path.
   - Keep the intervention narrow and deterministic.

2. Conservative Downgrade Behavior
   - Downgrade mismatched confidence into a typed conservative outcome.
   - Preserve review messaging and limitations.

3. Workflow and UI Preservation
   - Keep already-consistent responses on the normal path.
   - Surface downgraded outcomes through the existing response path.

4. Observability
   - Record confidence-consistency guardrail decisions in structured events.
   - Preserve request correlation for guardrail outcomes.

5. Validation Coverage
   - Add tests for consistent vs inconsistent confidence behavior.
   - Add tests for typed downgraded outcomes and guardrail observability.
