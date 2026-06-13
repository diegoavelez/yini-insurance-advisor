# Validation

This slice is ready when comparison-oriented retrieval can fuse local lexical candidates with Qdrant semantic candidates without changing retrieval contracts.

## Acceptance Checks

- The spec bundle exists.
- Comparison-gated lexical recall can add a local comparative chunk.
- Local lexical candidates respect typed filters.
- Duplicate candidates merge deterministically.
- Focused retrieval tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 12 --product auto`
