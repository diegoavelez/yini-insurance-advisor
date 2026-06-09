# Validation

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.

## Required Checks

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Required Scenarios

- The derived Qdrant point id is valid and deterministic.
- Indexing succeeds against the configured Qdrant collection.
- Retrieval results still expose the original `chunk_id`.
- A real end-to-end query can run after indexing.

## Merge Readiness

This spec is ready when local end-to-end indexing and retrieval succeed without
changing the public `chunk_id` contract.

## Evidence

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`
- `./.venv/bin/python -u - <<'PY' ... client.upsert(...); print(client.count(...)) ... PY`
- `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir /tmp/yini-batch-test/processed/embeddings --manifest-path /tmp/yini-batch-test/processed/qdrant-indexing-manifest.jsonl --fail-fast true`

## Recorded Outcome

- Qdrant no longer rejects deterministic chunk-derived records with
  `400 Bad Request` for invalid point ids.
- The physical Qdrant point id is now a deterministic UUID derived from
  `chunk_id`.
- The logical `chunk_id` remains unchanged in the Qdrant payload and in
  downstream retrieval/citation contracts.
