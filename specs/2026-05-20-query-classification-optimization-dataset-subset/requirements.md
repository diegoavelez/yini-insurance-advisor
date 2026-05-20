# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to create a narrow optimization dataset subset for query
classification, aligned to the selected target, the existing evaluation assets,
and the baseline documented in the roadmap.

This slice should stay focused on dataset authoring and deterministic linkage.
It should not yet run before/after optimization comparisons.

## In Scope

- Create a narrow dataset subset for query classification optimization.
- Keep stable linkage to the existing evaluation question set where relevant.
- Preserve deterministic ids and typed validation.
- Cover the query-classification categories relevant to the current baseline.

## Out of Scope

- Before/after optimization comparison.
- Production deployment changes.
- Broader workflow redesign.
- Non-query-classification optimization targets.

## Dataset Contract

The optimization subset should be explicit and narrow.

At minimum:

- each example should map to one query-classification input;
- each example should expose an expected classification-compatible outcome;
- linkage to the existing evaluation assets should remain reviewable;
- the subset should remain small enough to support the next comparison slice
  without reopening dataset design.

## Acceptance Criteria

- A narrow optimization dataset subset exists for query classification.
- Dataset linkage to the current evaluation baseline is explicit.
- The slice stops before before/after comparison work.
- The subset is narrow enough to support the next `Phase 11` slice directly.
