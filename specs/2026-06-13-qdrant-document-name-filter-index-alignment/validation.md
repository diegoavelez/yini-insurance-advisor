# Validation

This slice is ready when Qdrant collection bootstrap creates a keyword payload
index for `document_name`, preserving compatibility with the existing indexing
seam.

## Acceptance Checks

- The new spec bundle exists.
- `rag/ingestion.py` includes `document_name` in the bootstrap payload-index
  field set.
- Focused indexing tests assert payload-index creation for
  `document_type`, `product`, and `document_name`.
- Compatibility-path tests still pass when `create_payload_index` is absent.
- Validation notes make clear that the live collection still needs an operator
  indexing rerun.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`

## Execution Notes

- `./.venv/bin/python -m pytest tests/test_qdrant_indexing.py tests/test_retrieval.py -q`
  passed locally.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_qdrant_indexing.py tests/test_retrieval.py`
  passed locally.
- The live collection still needs an operator indexing rerun so Qdrant can
  create the new `document_name` payload index.

## Expected Outcome

- The next indexing rerun can create the missing `document_name` payload index
  on the live Qdrant collection.
- Explicit PV document-family retrieval no longer fails with the `index
  required` runtime error after that rerun.
