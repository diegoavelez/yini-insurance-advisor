# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to compare baseline versus optimized latency for query
classification using the selected target, the current optimization subset, and
the documented local baseline.

This slice should stay focused on latency comparison only. It should not yet
add cost comparison work.

## In Scope

- Run a measurable baseline-versus-optimized latency comparison for query
  classification.
- Report overall latency comparison results.
- Keep comparison anchored to the documented local baseline.
- Reuse the current optimization subset and optimization seam where relevant.

## Out of Scope

- Cost comparison.
- Production deployment changes.
- Broader workflow redesign.
- Non-query-classification optimization targets.

## Comparison Contract

The latency comparison should be explicit and reviewable.

At minimum:

- baseline and optimized timing should be measured over the same optimization
  subset;
- reporting should expose overall latency comparison results;
- the comparison should remain narrow enough to support the next cost slice
  without reopening the latency methodology.

## Acceptance Criteria

- A measurable latency comparison seam exists for query classification.
- The comparison reports explicit baseline and optimized latency results.
- The slice stops before cost comparison work.
- The methodology is narrow enough to support the next `Phase 11` slice
  directly.
