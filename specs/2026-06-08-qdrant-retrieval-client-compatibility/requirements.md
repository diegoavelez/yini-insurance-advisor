# Requirements

## Feature Summary

This feature defines the next corrective slice of
`Phase 16 — Ingestion Runtime Remediation`.

The goal is to make retrieval compatible with the installed `qdrant-client`
surface so end-to-end retrieval no longer depends on a missing `search()`
method when the client exposes `query_points()` instead.

## In Scope

- Adapt the retrieval path to work with the installed Qdrant client API.
- Preserve the current retrieval result contract and payload mapping.
- Support deterministic retrieval with filters, vector queries, and payloads.
- Add or update tests for the compatible retrieval path.
- Revalidate real retrieval against the current indexed sample corpus.

## Out of Scope

- Query-scope expansion for Spanish product phrasing.
- Embedding-model changes.
- Qdrant point-id changes beyond the already separated corrective slice.

## Acceptance Criteria

- Retrieval no longer fails with `'QdrantClient' object has no attribute search'`.
- Retrieval still maps the original `chunk_id` from Qdrant payloads.
- Tests cover the active client compatibility path.
