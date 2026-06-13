# Validation

- Trivial `Page N` heading blocks are not emitted as standalone chunk content.
- The `pv` diagrammatic sections use semantic section labels when present.
- `COBERTURAS Y PLANES` content is rewritten into more semantic statement-style
  text.
- Existing ingestion regressions continue to pass.

## Suggested Checks

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir data/raw --markdown-dir data/markdown --processed-dir data/processed --manifest-path data/processed/ingestion-manifest.jsonl --glob 'MOVILIDAD/BICICLETAS Y PATINETAS/pv bicis y patinetas v2.pdf' --overwrite true --fail-fast true --docling-startup-timeout-seconds 20`
