# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 10 — Evaluation Dataset`.

The goal is to expand the initial curated question set toward the 30-question
target while keeping category coverage balanced across normal QA and guardrail
scenarios.

This slice should stay focused on dataset expansion and category balance only.
It should not yet add golden outputs, runner execution, or hosted-like
regression machinery.

## In Scope

- Expand the curated evaluation question set beyond the initial seed set.
- Move the dataset toward the 30-question roadmap target.
- Preserve stable question identifiers and deterministic versioning.
- Improve category balance across supported QA and guardrail scenarios.

## Out of Scope

- Golden expected outputs.
- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Dataset Expansion Contract

The expanded dataset must remain explicit and typed.

At minimum:

- every question should keep a stable identifier;
- every question should preserve category and expected-behavior metadata;
- dataset versioning should remain explicit;
- added questions should avoid near-duplicate coverage.

## Category Balance Contract

The expanded set should improve coverage balance across the current categories.

At minimum, it should broaden:

- standard grounded insurance-document questions;
- unsupported or out-of-scope queries;
- prompt-injection-style prompts;
- citation-guardrail-sensitive prompts;
- confidence-guardrail-sensitive prompts.

Balance should be deliberate rather than uniform for its own sake.

## Acceptance Criteria

- The question set is materially expanded from the initial seed set.
- The dataset remains valid against the existing typed schema.
- Category coverage is broader and more balanced than before.
- The slice stops before golden-output or runner work.
