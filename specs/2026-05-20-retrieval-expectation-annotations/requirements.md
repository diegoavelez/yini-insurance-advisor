# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to add explicit retrieval expectations for the existing curated
evaluation set and golden behavior dataset.

This slice should stay focused on retrieval-oriented expectations only. It
should not yet add citation expectations, evaluation runner execution, or
hosted-like regression machinery.

## In Scope

- Add explicit retrieval expectation annotations where retrieval behavior is
  meaningful.
- Preserve deterministic linkage between each question and its retrieval
  expectation record.
- Distinguish questions that should retrieve grounded evidence from refusal or
  guardrail cases where retrieval expectations are limited or absent.
- Keep the annotations locally reviewable and versionable.

## Out of Scope

- Citation expectations.
- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Retrieval Expectation Contract

Retrieval expectations must stay narrow and explicit.

At minimum:

- each annotated question should keep stable linkage by `question_id`;
- grounded-QA questions should carry explicit retrieval-oriented expectations;
- refusal or guardrail questions may explicitly declare limited or absent
  retrieval expectations;
- the dataset should remain deterministic and easy to diff.

## Acceptance Criteria

- A retrieval expectation dataset exists for the curated evaluation questions.
- The dataset preserves stable question linkage and deterministic structure.
- Grounded-QA and guardrail/refusal cases are distinguishable at the retrieval
  expectation level.
- The slice stops before citation expectations or runner work.
