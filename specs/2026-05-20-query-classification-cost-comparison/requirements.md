# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to compare baseline versus optimized cost for query classification
using the selected target, the current optimization subset, and the documented
zero-external-call baseline.

This slice should stay focused on cost comparison only.

## In Scope

- Run a measurable baseline-versus-optimized cost comparison for query
  classification.
- Report explicit baseline and optimized cost results.
- Keep comparison anchored to the documented zero-external-call baseline.
- Reuse the current optimization subset and optimization seam where relevant.

## Out of Scope

- Production deployment changes.
- Broader workflow redesign.
- Non-query-classification optimization targets.

## Comparison Contract

The cost comparison should be explicit and reviewable.

At minimum:

- baseline and optimized cost should be measured over the same optimization
  subset;
- reporting should expose explicit baseline and optimized cost results;
- the comparison should remain narrow enough to close `Phase 11` without
  reopening the cost methodology.

## Acceptance Criteria

- A measurable cost comparison seam exists for query classification.
- The comparison reports explicit baseline and optimized cost results.
- The methodology is narrow enough to close the remaining `Phase 11` work.
