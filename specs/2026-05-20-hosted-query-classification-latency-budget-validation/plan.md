# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Hosted-Like Seam
   - Define a narrow product-facing latency-validation seam.
   - Reuse current query-classification helpers where possible.

2. Decision Reporting
   - Add explicit within-budget / over-budget reporting.
   - Keep the hosted-like budget threshold visible in the result.

3. Validation
   - Add deterministic tests for the hosted-like latency-budget decision.
   - Confirm the slice stops before broader productionization.
