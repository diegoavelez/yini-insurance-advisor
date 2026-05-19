# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Guardrail Boundary Definition
   - Define where citation presence is enforced in the answer path.
   - Keep the intervention narrow and deterministic.

2. Conservative Guarded Outcome
   - Downgrade citationless answerable responses into a typed limited outcome.
   - Preserve review messaging and avoid fabricated citations.

3. Workflow and UI Preservation
   - Keep cited answerable responses on the normal path.
   - Surface guarded outcomes through the existing response path.

4. Observability
   - Record citation-presence guardrail decisions in structured events.
   - Preserve request correlation for guardrail outcomes.

5. Validation Coverage
   - Add tests for cited vs citationless answer behavior.
   - Add tests for typed guarded outcomes and guardrail observability.
