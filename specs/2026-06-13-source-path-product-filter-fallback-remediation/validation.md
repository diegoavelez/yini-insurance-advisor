# Validation

This slice is ready when local filtered retrieval can keep chunks whose canonical product is recoverable from `source_pdf_relative_path`.

## Acceptance Checks

- The spec bundle exists.
- Product fallback inference works for missing `product` values.
- Explicit `product` values still take precedence.
- Focused retrieval tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 12 --product auto`
