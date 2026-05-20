# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to define typed local evaluation result contracts and deterministic
result-schema expectations over the curated evaluation assets.

This slice should stay focused on contracts and result shape only. It should
not yet execute the local runner or add hosted-like regression scenarios.

## In Scope

- Add typed contracts for local evaluation runs and per-question results.
- Define deterministic result fields over the existing evaluation assets.
- Preserve clear linkage to question ids and current expectation datasets.
- Keep result structures locally reviewable and versionable.

## Out of Scope

- Runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Result Contract

The evaluation result shape must stay narrow and explicit.

At minimum:

- one run-level result contract should exist;
- one per-question result contract should exist;
- per-question results should keep stable linkage by `question_id`;
- result fields should be sufficient to compare actual vs expected behavior at a
  contract level;
- the schema should remain deterministic and easy to diff.

## Acceptance Criteria

- Typed evaluation runner result contracts exist.
- The result schema is deterministic and linked to the existing evaluation
  assets.
- The slice stops before executing the runner.
