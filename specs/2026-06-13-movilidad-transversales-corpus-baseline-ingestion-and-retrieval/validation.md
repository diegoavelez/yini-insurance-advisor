# Validation

Planned checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check tests/test_ingestion.py`
3. `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir data/raw --markdown-dir data/markdown --processed-dir data/processed --manifest-path data/processed/ingestion-manifest.jsonl --glob 'MOVILIDAD/TRANSVERSALES/*.pdf' --metadata-overlay-path ops/document-metadata-overlays.json --overwrite false --fail-fast true`
