# Validation

This slice is ready when the shared lexical term-equivalence helpers live in a
dedicated module and retrieval normalization still behaves identically.

## Acceptance Checks

- The new spec bundle exists.
- `rag/term_equivalences.py` owns the extracted lexical helper surface.
- Focused tests pass for the new helper module and existing retrieval
  normalization flows.
- Static verification passes for the touched Python files.

## Completion Evidence

- Focused tests pass with:
  - `./.venv/bin/python -m pytest tests/test_term_equivalences.py tests/test_retrieval.py -q -k 'term_equivalence or normalize_retrieval_query'`
- Static verification passes with:
  - `./.venv/bin/python -m ruff check rag/ingestion.py rag/term_equivalences.py tests/test_term_equivalences.py tests/test_retrieval.py`
- `rag/ingestion.py` imports the lexical helpers from `rag/term_equivalences.py`
  instead of defining them inline.
