# Requirements

## Feature Summary

This feature defines a corrective scope-classification slice under
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to align the deterministic query-scope classifier with the current
Spanish demo corpus so benign in-scope questions about autos coverage and
assistance are not rejected before retrieval and grounded answering.

## In Scope

- Extend deterministic supported-query matching for the current Spanish autos
  and assistance vocabulary present in the sample corpus.
- Preserve the existing typed supported/unsupported scope contract.
- Add focused regression coverage for a benign autos assistance query that
  should now pass scope validation.

## Out of Scope

- Broad query-classification redesign.
- New prompt-injection heuristics.
- Retrieval ranking or answer-generation logic changes.

## Acceptance Criteria

- A Spanish autos assistance query such as
  `¿Qué cubre la asistencia en pequeños eventos para autos?` is classified as
  supported.
- Existing unsupported non-insurance Spanish queries remain unsupported.
- The change remains a narrow deterministic scope-alignment remediation.
