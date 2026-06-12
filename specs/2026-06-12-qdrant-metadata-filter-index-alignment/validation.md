# Validation

## Status

- Planned on `2026-06-12`.
- Code completed on `2026-06-12`.
- Live Qdrant verification remains pending until the operator reruns indexing
  against the target collection with the updated bootstrap code.

## Required Checks

- Qdrant collection bootstrap creates keyword payload indexes for supported
  metadata filter fields when the client supports it.
- Indexing still succeeds when payload-index creation is unavailable on the
  client surface.

## Required Scenarios

- A supported Qdrant client receives payload-index creation calls for
  `document_type` and `product`.
- A compatibility client without `create_payload_index` still indexes points
  successfully.
- Retrieval-focused tests remain green after the indexing bootstrap change.

## Merge Readiness

This slice is ready when the indexing bootstrap guarantees the current metadata
filter surface can be backed by payload indexes without breaking compatibility
with narrower client surfaces.

## Evidence

- Focused regression validation passed:
  - `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- A live filtered retrieval against Qdrant still returned:
  - `400 Bad Request`
  - `Index required but not found for "product"`
- That live result is consistent with the expected transitional state: the
  remote collection has not yet been reindexed with the updated bootstrap code.

## Operator Follow-up

- Rerun:
  - `make batch-index BATCH_VENV=/private/tmp/yini-fast-venv311 BATCH_PROCESSED_DIR=data/processed`
- Then verify:
  - `/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuál es la normatividad que rige el registro único de intermediarios en ARL?' --product arl --top-k 5`
