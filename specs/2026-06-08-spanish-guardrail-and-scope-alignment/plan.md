# Plan

## Status

- Completed on `2026-06-08`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Deterministic Scope Audit
   - Review supported-scope token matching.
   - Identify the minimum Spanish insurance vocabulary needed for the demo.

2. Deterministic Guardrail Audit
   - Review current prompt-injection regex patterns.
   - Add the minimum Spanish override/reveal phrasing needed for the demo.

3. Validation
   - Add targeted tests for Spanish supported-scope and prompt-injection paths.
   - Confirm English deterministic behavior remains intact.
