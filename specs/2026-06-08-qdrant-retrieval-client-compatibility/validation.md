# Validation

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.

## Required Checks

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`

## Required Scenarios

- Retrieval works with the installed Qdrant client surface.
- Retrieval results still expose the original `chunk_id`.
- A real query can return ranked chunks from the indexed sample set.

## Evidence

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query "cobertura del plan PAC 60 más" --top-k 3`

## Recorded Outcome

- Retrieval now works with the installed Qdrant client by using
  `query_points()` when `search()` is not available.
- The real retrieval query returned ranked chunks from the indexed `PAC`
  document set, preserving the original `chunk_id` values from payloads.
