# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to add explicit golden expected behavior annotations for the
curated 30-question evaluation set, with clear expected guardrail or refusal
outcomes where applicable.

This slice should stay focused on behavior-level expectations only. It should
not yet add retrieval evidence annotations, citation expectations, runner
execution, or hosted-like regression machinery.

## In Scope

- Add explicit golden expected behavior records for the curated question set.
- Preserve deterministic linkage between each question and its expected outcome.
- Cover both normal grounded-answer behavior and current guardrail/refusal cases.
- Keep the golden dataset locally reviewable and versionable.

## Out of Scope

- Retrieval evidence expectations.
- Citation expectations.
- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Golden Behavior Contract

Golden expectations must stay narrow and explicit.

At minimum:

- each question should map to one explicit expected behavior outcome;
- guardrail-sensitive questions should map to the corresponding refusal or
  guarded outcome;
- normal grounded-QA questions should remain distinguishable from guardrail
  cases;
- the dataset should remain deterministic and easy to diff.

## Acceptance Criteria

- A golden behavior dataset exists for the curated evaluation questions.
- The dataset preserves stable question linkage and deterministic structure.
- Guardrail and refusal expectations are explicit.
- The slice stops before retrieval/citation evidence annotations or runner work.
