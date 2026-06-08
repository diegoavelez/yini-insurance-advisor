# Plan

## Status

- Completed on `2026-06-08`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Embedding Seam Audit
   - Confirm where the default embedding model is configured.
   - Identify tests and artifact expectations pinned to the current model name.

2. Multilingual Alignment
   - Switch the default embedding model to a multilingual
     sentence-transformers-compatible model.
   - Preserve provider, retrieval contracts, and Qdrant seams.

3. Validation
   - Update deterministic tests for the new model name.
   - Confirm no query-scope or guardrail behavior changed in this slice.
