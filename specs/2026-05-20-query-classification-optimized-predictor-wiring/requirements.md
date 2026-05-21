# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to wire one real optimized query-classification predictor from the
current DSPy module and optimization subset into the existing quality,
latency, and cost comparison seams.

This slice should stay focused on producing a real optimized callable and
making it usable by the current comparison seams. It should not yet claim that
measurable improvement exists.

## In Scope

- Build one real optimized query-classification predictor from the current DSPy
  module and optimization subset.
- Expose that predictor through a narrow callable seam.
- Make the existing quality, latency, and cost comparison seams able to use the
  optimized callable.
- Keep the optimized predictor reviewable and local.

## Out of Scope

- Declaring success on measurable improvement.
- Production deployment changes.
- Broader workflow redesign.
- Non-query-classification optimization targets.

## Wiring Contract

The optimized predictor wiring should be explicit and narrow.

At minimum:

- the optimized predictor should be a real callable, not only a placeholder;
- the optimized predictor should accept the existing typed optimization input;
- the existing comparison seams should be able to consume it without contract
  changes;
- the slice should remain narrow enough to support the final validation slice
  without reopening the wiring model.

## Acceptance Criteria

- A real optimized query-classification callable exists.
- The callable is wired into the existing comparison seams.
- The slice stops before claiming measurable improvement.
- The wiring is narrow enough to support the next `Phase 11` slice directly.
