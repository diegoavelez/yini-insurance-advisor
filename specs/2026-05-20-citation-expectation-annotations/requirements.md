# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to add explicit citation expectations for the curated evaluation
set over the existing golden behavior and retrieval expectation assets.

This slice should stay focused on citation-oriented expectations only. It
should not yet add runner execution or hosted-like regression machinery.

## In Scope

- Add explicit citation expectation annotations where citation behavior is
  meaningful.
- Preserve deterministic linkage between each question and its citation
  expectation record.
- Distinguish grounded-answer cases from refusal or guardrail cases at the
  citation expectation level.
- Keep the annotations locally reviewable and versionable.

## Out of Scope

- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Citation Expectation Contract

Citation expectations must stay narrow and explicit.

At minimum:

- each annotated question should keep stable linkage by `question_id`;
- grounded-QA questions should carry explicit citation-oriented expectations;
- refusal cases should explicitly declare absent citation expectations;
- guardrail cases should explicitly encode the expected citation posture without
  adding evidence annotations yet;
- the dataset should remain deterministic and easy to diff.

## Acceptance Criteria

- A citation expectation dataset exists for the curated evaluation questions.
- The dataset preserves stable question linkage and deterministic structure.
- Grounded-QA, refusal, and guardrail cases are distinguishable at the citation
  expectation level.
- The slice stops before runner work.
