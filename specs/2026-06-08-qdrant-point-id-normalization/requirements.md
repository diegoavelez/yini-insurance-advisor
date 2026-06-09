# Requirements

## Feature Summary

This feature defines the next corrective slice of
`Phase 16 — Ingestion Runtime Remediation`.

The goal is to normalize Qdrant point ids so end-to-end indexing works with the
current deterministic chunk contract, without changing the user-facing
`chunk_id` contract used by retrieval, citations, and grounded-answer flows.

## In Scope

- Replace the current Qdrant physical point id derivation when it produces
  values that Qdrant rejects.
- Preserve `chunk_id` as the stable logical identifier in payloads and
  downstream response surfaces.
- Use a deterministic mapping from `chunk_id` to a Qdrant-valid point id.
- Add or update tests for Qdrant point-id generation and indexing behavior.
- Revalidate local end-to-end indexing and retrieval against the current sample
  ingestion artifacts.

## Out of Scope

- Redesign of `chunk_id` itself.
- Retrieval-ranking changes.
- Embedding-model changes.
- Qdrant collection schema redesign beyond valid point-id normalization.

## Alignment Expectations

At minimum:

- Qdrant receives valid point ids for every upserted embedding record;
- retrieval payloads still expose the original `chunk_id`;
- the deterministic local chunk contract remains stable for citations and
  review flows.

## Acceptance Criteria

- Indexing no longer fails with `400 Bad Request` for invalid point ids.
- The Qdrant point id is deterministic across reruns for the same `chunk_id`.
- Retrieval results still surface the original `chunk_id`.
- Targeted tests cover valid Qdrant point-id generation and successful
  indexing.
