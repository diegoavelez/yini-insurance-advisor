# Plan

## Status

- Completed on `2026-06-07`.
- Implemented directly on `main`.
- Verification status is tracked in `validation.md`.

1. UI Surface Audit
   - Identify public user-visible strings in the Gradio demo.
   - Separate UI copy from backend/internal trace fields.

2. Spanish Localization
   - Translate public labels and deterministic helper/status messages.
   - Preserve current layout and result-surface structure.

3. Validation
   - Update UI tests for Spanish-visible copy.
   - Confirm no retrieval or scope behavior changed in this slice.
