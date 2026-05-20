# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to complete the curated evaluation question set to the 30-question
roadmap target while preserving typed validation, stable identifiers, and
balanced scenario coverage.

This slice should stay focused on closing the remaining question-count gap only.
It should not yet add golden outputs, runner execution, or hosted-like
regression machinery.

## In Scope

- Expand the curated evaluation dataset from its current size to 30 questions.
- Preserve stable question identifiers and deterministic dataset versioning.
- Fill remaining scenario gaps without changing the existing schema.
- Keep category and scenario coverage deliberate and reviewable.

## Out of Scope

- Golden expected outputs.
- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Completion Contract

The dataset must reach the roadmap target explicitly.

At minimum:

- the set should contain 30 curated questions;
- each question should remain valid under the existing typed schema;
- new questions should preserve stable IDs and metadata fields;
- additions should avoid shallow duplicates.

## Coverage Contract

The final 30-question set should improve completeness, not only raw count.

At minimum, new additions should strengthen:

- grounded insurance-document questions;
- unsupported or out-of-scope queries;
- prompt-injection prompts;
- citation-guardrail prompts;
- confidence-guardrail prompts.

The resulting set should remain compact enough for manual review.

## Acceptance Criteria

- The curated set reaches 30 total questions.
- The dataset remains valid against the existing schema.
- Added questions improve scenario completeness without drifting into golden-output work.
- The slice stops before runner execution or hosted-like regressions.
