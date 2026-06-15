# Validation

This slice is ready when PDF-conversion and markdown-cleaning helpers live
behind their own `rag` seam and validated ingestion behavior remains unchanged.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py rag/pdf_conversion.py tests/test_ingestion.py`
3. If the runtime is available, run one representative conversion-path smoke
   such as the existing Docling warm-up or a narrow sample-PDF conversion.

## Expected Evidence

- Docling-first and PDFium-fallback tests still pass;
- markdown cleanup/usability checks still pass;
- the seam boundary leaves ingestion orchestration unchanged.
