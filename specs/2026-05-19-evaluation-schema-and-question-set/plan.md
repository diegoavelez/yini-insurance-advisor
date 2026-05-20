# Plan

## Status

- Completed on `2026-05-19`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. Schema Definition
   - Define the typed schema for evaluation questions.
   - Keep the contract narrow and future-proof for later slices.

2. Initial Question Authoring
   - Add a compact curated set of representative questions.
   - Cover both normal QA and guardrail-oriented prompts.

3. Validation Coverage
   - Add tests that validate the dataset against the schema.
   - Keep verification deterministic and local.
