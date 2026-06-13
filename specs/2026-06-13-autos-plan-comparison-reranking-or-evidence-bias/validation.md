# Validation

This slice is ready when AUTOS comparison-intent queries use deterministic reranking over a larger candidate pool without changing the public retrieval contract.

## Acceptance Checks

- The new spec bundle exists.
- Comparison-intent queries trigger a larger candidate limit.
- Curated comparison-term matches can reorder final results deterministically.
- Non-comparison queries keep current retrieval-limit behavior.
- Focused retrieval tests pass.
- README and roadmap reflect the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 8 --product auto`

## Expected Outcome

- Comparison-oriented AUTOS queries can surface the comparative evidence set more reliably.
- The retrieval contract remains unchanged.
- The slice stops before broader reranker design or cross-product ranking policy work.
