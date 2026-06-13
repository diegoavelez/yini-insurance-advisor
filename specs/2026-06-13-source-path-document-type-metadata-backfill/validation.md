# Validation

This slice is ready when ingestion persists canonical document type metadata from source-relative paths whenever overlays are absent.

## Acceptance Checks

- The spec bundle exists.
- Ingestion infers `document_type` from path/filename when overlay metadata is missing.
- Overlay `document_type` values still take precedence.
- Processed documents and chunk bundles persist the resolved document type.
- Focused ingestion tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
