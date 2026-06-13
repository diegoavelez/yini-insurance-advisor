# Requirements

## Feature Summary

This feature defines a corrective scope-classification slice under
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to align the deterministic query-scope classifier with the current
Spanish `MOVILIDAD/BICICLETAS Y PATINETAS` corpus so benign in-scope questions
about bicycle and scooter insurance are not rejected before retrieval and
grounded answering.

## In Scope

- Extend deterministic supported-query matching for the current Spanish
  bicycles and scooters vocabulary present in the corpus.
- Preserve the existing typed supported/unsupported scope contract.
- Add focused regression coverage for a benign bicycle/scooter coverage query
  that should pass scope validation.

## Out of Scope

- Broad query-classification redesign.
- New prompt-injection heuristics.
- Retrieval ranking or answer-generation logic changes.

## Acceptance Criteria

- A Spanish query such as
  `¿Qué cubre el seguro para bicicletas y patinetas?` is classified as
  supported.
- Existing unsupported non-insurance Spanish queries remain unsupported.
- The change remains a narrow deterministic scope-alignment remediation.
