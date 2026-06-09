# Requirements

## Feature Summary

This feature defines the first narrow slice of
`Phase 17 — Runtime Compatibility Hardening`.

The goal is to formalize the validated Groq runtime configuration so the local
RAG pipeline can answer real user questions end-to-end without relying on
undocumented local fixes.

## In Scope

- Confirm the correct Groq model identifier for the current runtime.
- Synchronize tracked local configuration examples with the validated model id.
- Preserve the existing grounded-answer contract and retrieval path.
- Record end-to-end runtime evidence for a successful `answer-query` run.

## Out of Scope

- Changing LLM provider away from Groq.
- Prompt redesign.
- Retrieval or Qdrant architecture changes.
- Hosted deployment runtime changes.

## Acceptance Criteria

- The repo documents the validated Groq model identifier.
- Tracked configuration examples no longer drift from the working runtime.
- A real `answer-query` invocation succeeds end-to-end against the indexed
  sample corpus using the validated model id.
