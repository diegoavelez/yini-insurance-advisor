# Validation

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.

## Required Checks

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`

## Required Scenarios

- The default local ingestion path prefers Docling.
- A Docling warm-up path exists and can be invoked intentionally.
- A fallback mode remains available when explicitly selected or allowed.
- The timeout behavior is configurable for local runs.

## Merge Readiness

This spec is ready when the repo provides a clear local ingestion policy with:

- Docling-first default behavior;
- explicit asset warm-up support;
- configurable timeout behavior;
- verified backend selection paths.

## Evidence

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m rag.ingestion warmup-docling-assets --sample-pdf "data/raw/clausulado poliza de complicaciones esteticas.pdf" --docling-startup-timeout-seconds 300`
- `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir /tmp/yini-docling-check/raw --markdown-dir /tmp/yini-docling-check/markdown --processed-dir /tmp/yini-docling-check/processed --manifest-path /tmp/yini-docling-check/processed/ingestion-manifest.jsonl --overwrite true --fail-fast true`

## Notes

- The policy keeps Docling as the preferred local backend and gives it enough
  time to initialize and download required assets.
- `pypdfium2` remains available as an explicit recovery path rather than
  silently replacing Docling when the operator requests Docling-only behavior.
