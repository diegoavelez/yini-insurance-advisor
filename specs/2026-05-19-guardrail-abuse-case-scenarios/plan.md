# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Scenario Set Definition
   - Define a compact set of deterministic abuse and boundary prompts.
   - Keep the set tied to already-implemented guardrails only.

2. Guarded Outcome Assertions
   - Assert the expected refusal or downgrade behavior for each scenario.
   - Avoid vague pass/fail checks.

3. Benign Control Coverage
   - Add a small control set of supported benign prompts.
   - Confirm those still pass the normal path.

4. Regression Orientation
   - Keep the suite deterministic and easy to rerun.
   - Avoid expanding into the broader evaluation dataset.

5. Validation Coverage
   - Cover unsupported-query, prompt-injection, citation-presence, and confidence-consistency guardrails.
