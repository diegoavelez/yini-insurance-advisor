# Plan

## Status

- Completed on `2026-05-20`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Predictor Construction
   - Build the real optimized query-classification callable.
   - Keep the callable aligned to the current typed optimization input/output.

2. Seam Wiring
   - Make the current comparison seams able to consume the optimized callable.
   - Avoid changing their external comparison contracts.

3. Validation
   - Add deterministic validation that the optimized callable is real and
     consumable.
   - Confirm the slice stops before measurable-improvement claims.
