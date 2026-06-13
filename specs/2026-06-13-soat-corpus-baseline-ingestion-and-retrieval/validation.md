# Validation

This slice is ready when `SOAT` has a stable baseline taxonomy and metadata
surface for later ingestion and retrieval runs.

## Acceptance Checks

- The spec bundle exists.
- `soat` aliases exist for query and product-filter normalization.
- SOAT queries classify as supported.
- The SOAT overlay entries exist for both source PDFs.
- Path-derived product inference can resolve `product=soat`.
- Focused tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_query_scope.py tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check core/query_scope.py tests/test_query_scope.py tests/test_ingestion.py rag/ingestion.py`

## Follow-on Runtime Validation

After this baseline lands, the operator should run:

- category-only ingestion for `MOVILIDAD/SOAT`
- category-only embeddings generation for `movilidad__soat__*.chunks.json`
- category-only Qdrant indexing for `movilidad__soat__*.embeddings.json`
- real validation for tariff and coverage questions
