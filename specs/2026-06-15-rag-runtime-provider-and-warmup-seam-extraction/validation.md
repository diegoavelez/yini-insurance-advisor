# Validation

This slice is ready when runtime/provider bridges and warmup support helpers live behind their own `rag` seam and the current runtime behavior remains unchanged.

## Status

- Completed on `2026-06-15`.
- Checks passed:
  - `./.venv/bin/python -m ruff check rag/ingestion.py rag/runtime_providers.py tests/test_embedding_generation.py tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py tests/test_ingestion.py specs/2026-06-15-rag-runtime-provider-and-warmup-seam-extraction --ignore E501`
  - `./.venv/bin/python -m pytest -q tests/test_embedding_generation.py tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py tests/test_ingestion.py`

## Planned Checks

1. `./.venv/bin/python -m pytest -q tests/test_embedding_generation.py tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py tests/test_ingestion.py`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/runtime_providers.py tests/test_embedding_generation.py tests/test_retrieval.py tests/test_grounded_answer_generation.py tests/test_observability.py tests/test_ingestion.py specs/2026-06-15-rag-runtime-provider-and-warmup-seam-extraction --ignore E501`

## Expected Evidence

- runtime backend failures remain unchanged for embedding, Qdrant, and Groq;
- `load_sentence_transformer` still supports offline cache enforcement and cache clearing;
- embedding warmup still loads the configured model with `local_files_only=False`;
- retrieval and grounded-answer flows still use the same embedding/completion bridges;
- `rag.ingestion.py` remains the top-level command surface with compatibility wrappers for tests.
