# Plan

## Status

- Completed on `2026-06-08`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. UI State Derivation Audit
   - Review the current UI helpers that infer degraded, refusal, and support
     outcomes.
   - Identify each place where English backend copy is used as a control signal.

2. Narrow Hardening
   - Switch derivation to typed fields or structured result signals where
     possible.
   - Keep the existing Spanish UI output contract stable.

3. Validation
   - Add targeted regression tests for Spanish-facing backend/refusal wording.
   - Verify no regressions in existing success, refusal, and degraded UI paths.
