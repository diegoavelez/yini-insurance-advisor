# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to execute a repeatable local evaluation runner over the curated
evaluation assets and produce typed run results.

This slice should stay focused on local deterministic execution only. It should
not yet add hosted-like regression scenarios or DSPy optimization.

## In Scope

- Execute a local evaluation run over the curated evaluation question set.
- Use the existing golden behavior, retrieval expectation, and citation
  expectation assets.
- Produce typed `EvaluationRunResult` outputs.
- Keep execution deterministic and locally reviewable.

## Out of Scope

- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Runner Execution Contract

The runner should remain narrow and explicit.

At minimum:

- execution should iterate deterministically over the curated question set;
- each question should produce one typed per-question result;
- the run should produce one typed run-level result;
- result linkage by `question_id` should remain explicit;
- execution should stay local and reviewable.

## Acceptance Criteria

- A local evaluation runner execution seam exists.
- The runner produces typed `EvaluationRunResult` outputs.
- Execution is deterministic over the current evaluation assets.
- The slice stops before hosted regression smoke work.
