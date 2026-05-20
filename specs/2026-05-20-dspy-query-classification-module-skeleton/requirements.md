# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to add a minimal DSPy module skeleton for query classification,
aligned to the existing deterministic classification seam and the selected
baseline documented in the roadmap.

This slice should stay focused on the DSPy module boundary and its explicit
input/output contract. It should not yet create the optimization dataset subset
or run before/after comparisons.

## In Scope

- Add a minimal DSPy module skeleton for query classification.
- Define the explicit input/output contract for that module.
- Keep the module narrow enough to plug into later optimization work.
- Preserve the current deterministic classification seam as the baseline.

## Out of Scope

- Optimization dataset subset authoring.
- Before/after optimization comparison.
- Production deployment changes.
- Broader workflow redesign.

## Module Contract

The DSPy module should be explicit and narrow.

At minimum:

- the module should target query classification only;
- the module should define a typed or explicit input surface for one user
  query;
- the module should define an explicit output surface that can be compared to
  the current `ExpectedBehavior`-oriented baseline;
- the module should not yet replace the current deterministic production seam.

## Acceptance Criteria

- A minimal DSPy module skeleton exists for query classification.
- The module boundary and I/O contract are explicit.
- The slice stops before optimization dataset or before/after comparison work.
- The module is narrow enough to support the next `Phase 11` slice directly.
