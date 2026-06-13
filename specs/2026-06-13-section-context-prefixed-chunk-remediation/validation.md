# Validation

This slice is ready when chunk text preserves governing section context for fragmented structured documents.

## Acceptance Checks

- The spec bundle exists.
- Chunk text gains deterministic prefixed section context when missing.
- Existing headings are not duplicated when already present.
- Focused chunking tests pass.
- The roadmap records the corrective slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué diferencias hay entre el plan básico y los otros planes de autos?' --top-k 8 --product auto`
