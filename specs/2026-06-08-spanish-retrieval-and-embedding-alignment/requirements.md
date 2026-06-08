# Requirements

## Feature Summary

This feature defines the second narrow implementation slice of
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to align retrieval embeddings with the Spanish-speaking demo and
Spanish insurance-document corpus by replacing the current English-only default
embedding model with a multilingual model that is compatible with the existing
`sentence-transformers` provider seam.

This slice must stay focused on embedding and retrieval alignment only.

## In Scope

- Replace the default embedding model with a multilingual model supported by the
  current `sentence-transformers` loading path.
- Keep the current embedding provider unchanged.
- Update deterministic tests and artifact expectations that currently pin the
  English-only embedding model name.
- Preserve the current retrieval/query contracts and Qdrant integration seam.

## Out of Scope

- Query-scope token logic changes.
- Guardrail-policy changes.
- Prompt or answer-generation changes.
- Hosted deployment changes.
- Spanish evaluation dataset creation.

## Model Selection Constraints

The selected model must:

- be multilingual;
- be loadable through the current `SentenceTransformer(model_name)` seam;
- avoid introducing a new embedding runtime or provider in this slice;
- be documented by a primary source as a sentence-transformers-compatible model.

## Acceptance Criteria

- The default embedding model is no longer English-only.
- The default embedding path remains `sentence-transformers`.
- Tests and artifact metadata expectations are updated to the selected
  multilingual model.
- The slice stops before query-scope, guardrail, and evaluation-alignment work.
