# Requirements

## Feature Summary

This feature defines the next corrective implementation slice of
`Phase 11 — DSPy Optimization`.

The goal is to remediate the current mismatch between `Phase 11` success
criteria and the implemented query-classification optimization seam by making
measurable improvement defensible on the documented evaluation surface, or by
narrowing the success claim if improvement is not yet supported.

This slice should stay focused on measurable-improvement remediation only. It
should not yet validate hosted-like latency budget.

## In Scope

- Reassess the current optimized query-classification predictor against the
  documented evaluation surface.
- Eliminate any misleading “improvement” framing that is not backed by the
  current implementation.
- Either:
  - wire a real optimized path that demonstrates measurable improvement; or
  - narrow the success claim and validation semantics so the repository no
    longer overstates optimization success.
- Keep the result explicit and reviewable.

## Out of Scope

- Hosted-like latency-budget validation.
- Broader productionization.
- New optimization targets.
- General workflow redesign.

## Remediation Contract

The remediation should resolve the current truth gap.

At minimum:

- the optimized path and the reported improvement state must be technically
  consistent;
- the comparison surface used for the decision must align with the documented
  `Phase 11` baseline or explicitly document the narrower surface in use;
- the resulting roadmap/spec state must no longer overstate measurable
  improvement if the implementation does not show it.

## Acceptance Criteria

- The repository no longer overstates measurable improvement for
  query-classification optimization.
- The optimized path and the improvement-validation result are technically
  aligned.
- The evaluation surface used by the improvement decision is explicit and
  defensible.
- The slice stops before hosted-like latency-budget validation.
