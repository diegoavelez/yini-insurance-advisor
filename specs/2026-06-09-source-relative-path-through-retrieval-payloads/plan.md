# Plan

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.
- Verification recorded in `validation.md`.

1. Contract Update
   - Extend the vector-payload and retrieved-chunk contracts with the relative
     source path field needed for retrieval-facing traceability.

2. Payload Propagation
   - Carry the field through embedding payload creation, Qdrant payload
     building, and search-hit mapping.

3. Regression Coverage
   - Update focused tests for indexing and retrieval, including compatibility
     with payloads that do not yet carry the field.
