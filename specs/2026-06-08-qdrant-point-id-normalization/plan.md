# Plan

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.
- Verification recorded in `validation.md`.

1. Normalize Physical Point Ids
   - Introduced a deterministic Qdrant-valid point-id mapping from `chunk_id`.
   - Kept `chunk_id` unchanged in payloads and downstream contracts.

2. Test Coverage
   - Added targeted tests for point-id validity and indexing behavior.
   - Preserved current retrieval expectations around `chunk_id`.

3. End-to-End Validation
   - Re-ran indexing against the current sample embedding artifacts.
   - Unblocked real retrieval/indexing by normalizing the physical Qdrant
     point id to a deterministic UUID.
