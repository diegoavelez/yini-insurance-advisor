# Requirements

## Feature Summary

This feature defines the fourth narrow implementation slice of
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to align the curated evaluation fixtures and hosted-like smoke
coverage with Spanish-speaking demo usage, now that the public UI, retrieval
defaults, and deterministic guardrail/scope seams have been aligned to Spanish.

This slice must stay focused on evaluation fixtures and smoke coverage only.

## In Scope

- Translate the curated local evaluation prompts to Spanish while preserving:
  - question ids;
  - category balance;
  - golden behavior expectations;
  - retrieval expectations;
  - citation expectations.
- Translate the linked query-classification optimization subset so it stays
  aligned to the evaluation question set.
- Update smoke coverage to exercise the Spanish-facing request path where
  appropriate.
- Update tests that pin dataset versions or rely on the translated fixture text.

## Out of Scope

- Embedding-model changes.
- Query-scope logic changes.
- Prompt-guardrail regex changes.
- UI-copy changes.
- Hosted deployment changes.

## Alignment Expectations

At minimum:

- the core curated evaluation dataset should no longer be English-only;
- the optimization subset should remain exactly aligned to the source question
  prompts;
- local evaluation and hosted-like smoke coverage should continue to pass with
  Spanish-facing fixture prompts.

## Acceptance Criteria

- The curated evaluation prompts are Spanish-facing.
- The optimization subset remains aligned to the updated evaluation prompts.
- Local evaluation still marks current assets as matched.
- Hosted-like smoke coverage includes the Spanish-facing request path.
