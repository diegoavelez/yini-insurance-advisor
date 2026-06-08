# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to localize the public Gradio demo UI into Spanish for the intended
Spanish-speaking user without changing backend retrieval, scope, or answer
generation behavior yet.

This slice must stay focused on user-visible UI localization only.

## In Scope

- Translate user-visible Gradio labels, headings, and status copy to Spanish.
- Translate deterministic UI-layer helper messages shown in the public demo.
- Keep the current UI structure and response surfaces intact.
- Update affected UI tests to assert the Spanish-visible behavior.

## Out of Scope

- Embedding-model changes.
- Retrieval behavior changes.
- Query-scope logic changes.
- Guardrail-policy redesign.
- Spanish evaluation datasets.

## Localization Expectations

At minimum:

- the public labels for readiness, trace summary, support context, debug
  metadata, answer quality, and error state should be presented in Spanish;
- user-visible status and helper copy should be presented in Spanish;
- the implementation should avoid changing typed backend contracts or internal
  observability field names;
- the slice should remain narrow enough to support the next retrieval-alignment
  slice directly.

## Acceptance Criteria

- The Gradio demo presents its public UI copy in Spanish.
- Existing response surfaces remain present and behaviorally equivalent.
- Tests covering the UI surface are updated for Spanish-visible text.
- The slice stops before retrieval, guardrail, and evaluation-alignment work.
