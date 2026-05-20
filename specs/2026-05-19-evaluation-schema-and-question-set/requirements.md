# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of `Phase 10 — Evaluation Dataset`.

The goal is to establish the typed evaluation schema and the initial curated
question set that later evaluation and optimization work will rely on.

This slice should stay focused on schema definition and question authoring only.
It should not yet add golden outputs, runner execution, or hosted-like
regression machinery.

## In Scope

- Define typed evaluation schemas.
- Add an initial curated question set.
- Cover normal grounded-QA questions and guardrail-oriented questions.
- Keep the dataset deterministic and versionable.

## Out of Scope

- Golden expected outputs.
- Evaluation runner execution.
- Hosted-like regression scenarios.
- DSPy optimization.
- UI changes.

## Dataset Contract

The initial dataset must be explicit and typed.

At minimum:

- each question should have a stable identifier;
- each question should declare its category or purpose;
- each question should preserve enough metadata for later golden expectations;
- the schema should distinguish normal QA prompts from guardrail-oriented prompts.

## Scope of the Initial Question Set

The initial question set should be compact but representative.

At minimum, it should include:

- standard grounded insurance-document questions;
- unsupported/out-of-scope queries;
- prompt-injection-style prompts;
- guardrail-sensitive prompts for citation or confidence behavior.

The set should remain small enough to maintain manually in this slice.

## Acceptance Criteria

- Typed evaluation schemas exist.
- An initial curated question set exists and validates against the schema.
- The set covers both normal QA and guardrail-oriented prompts.
- The slice stops before golden-output or runner work.
