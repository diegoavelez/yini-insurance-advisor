# Requirements

## Slice

`rag-qdrant-indexing-runtime-seam-extraction`

## Goal

Extract the remaining Qdrant-specific indexing runtime helpers out of
`rag/ingestion.py` and behind the existing `rag` Qdrant seam without changing
current indexing behavior or manifest outcomes.

## Context

After `rag-qdrant-client-and-payload-seam-extraction`, `rag/ingestion.py`
still owns one cohesive Qdrant indexing runtime cluster covering:

- transient-error classification for Qdrant upserts;
- retry/backoff behavior for point upserts;
- targeted prune of existing points for one `source_pdf_id`;
- operational smoke validation after indexing.

These helpers remain storage-runtime concerns rather than ingestion-contract
concerns and are the next narrow coupling reduction candidate.

## Requirements

1. The Qdrant indexing runtime helpers must move behind `rag/qdrant_store.py`.
2. `rag/ingestion.py` must consume those helpers through the seam rather than
   keep the runtime cluster inline.
3. Current behavior must remain unchanged for the validated indexing paths,
   especially:
   - retry/backoff behavior for transient upsert failures;
   - pruning existing points by `source_pdf_id` before reindexing;
   - smoke validation via Qdrant count after indexing;
   - indexing manifest success/failure outcomes.
4. The slice must remain narrow and must not change:
   - embedding bundle contracts;
   - retrieval ranking behavior;
   - manifest schemas or CLI arguments.

## Non-Goals

- changing the Qdrant payload contract or collection bootstrap rules;
- changing indexing manifest structures;
- introducing a new backend abstraction beyond the existing Qdrant seam;
- refactoring embedding generation or ingestion orchestration.
