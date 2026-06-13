# Validation

This slice is ready when ingestion persists canonical product metadata from source-relative paths whenever overlays are absent.

## Acceptance Checks

- The spec bundle exists.
- Ingestion infers `product` from source-relative path when overlay metadata is missing.
- Overlay `product` values still take precedence.
- Processed documents and chunk bundles persist the resolved product.
- Focused ingestion tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
