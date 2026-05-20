# Requirements

## Feature Summary

This feature defines a corrective narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to remediate the current evaluation seam so the local evaluation
runner no longer validates duplicated fixture labels against themselves and
instead provides a defensible behavioral evaluation seam.

This slice should stay focused on correcting the evaluation seam, ownership of
expected behavior labels, and explicit expectation-dataset linkage. It should
not start `Phase 11` or add broader analytics.

## In Scope

- Remove tautological behavior comparison from the local evaluation runner.
- Make the ownership of golden expected behavior explicit and non-duplicative.
- Ensure run-level results explicitly identify the expectation dataset versions
  they depend on.
- Keep the corrected seam deterministic and locally reviewable.

## Out of Scope

- DSPy optimization.
- Broader hosted benchmarking.
- New UI behavior.
- New retrieval or citation heuristics.

## Remediation Contract

The corrected evaluation seam must be materially stronger than asset-alignment
only.

At minimum:

- the question set should not be the source of truth for golden behavior labels
  if a separate golden dataset exists;
- the local runner should not derive `actual_behavior` from the same fixture
  label it is meant to validate;
- run-level results should expose explicit question-set and expectation-set
  versions as structured fields rather than only burying them in `run_id`;
- the corrected seam should remain deterministic and testable.

## Acceptance Criteria

- The duplication or ambiguity between question fixtures and golden behavior
  ownership is resolved.
- The local evaluation runner no longer performs tautological behavior checks.
- Run results explicitly carry the expectation dataset linkage they depend on.
- The slice stops before `Phase 11`.
