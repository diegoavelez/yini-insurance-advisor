# Plan

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.
- Verification recorded in `validation.md`.

1. Supported-Filter Review
   - Confirm which metadata fields are actually present in the current vector
     payload and retrieval seams.

2. Guardrail Implementation
   - Reject or otherwise explicitly block unsupported `document_type` and
     `product` filters before Qdrant filtering runs.

3. Focused Validation
   - Add tests that prove unsupported filters fail explicitly while supported
     filters remain functional.
