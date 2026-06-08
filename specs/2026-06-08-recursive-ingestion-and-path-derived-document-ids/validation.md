# Validation

## Status

- Planned on `2026-06-08`.
- Completed on `2026-06-08`.

## Required Checks

- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`

## Required Scenarios

- Nested PDFs under the raw input directory are discovered and processed.
- Duplicate basenames in different folders do not collide in generated
  artifacts.
- The resulting processed metadata preserves stable source-path traceability.

## Merge Readiness

This spec is ready when the repo supports nested local source trees without
manual flattening, while preserving deterministic ids and collision-safe
artifacts.

## Evidence

- `./.venv/bin/python -m ruff check contracts/ingestion.py contracts/documents.py rag/ingestion.py tests/test_ingestion.py tests/test_embedding_generation.py`
- `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_embedding_generation.py -q`
- `./.venv/bin/python -m rag.ingestion ingest-pdfs --input-dir data/raw --markdown-dir /tmp/yini-recursive-check-clean/markdown --processed-dir /tmp/yini-recursive-check-clean/processed --manifest-path /tmp/yini-recursive-check-clean/processed/ingestion-manifest.jsonl --overwrite true --fail-fast true --pdf-conversion-backend docling --docling-startup-timeout-seconds 300`

## Recorded Outcome

- Nested PDFs were discovered recursively under `data/raw`.
- Stable document ids were derived from the relative path, for example:
  - `AUTONOMIA/SOLUCIONES COLECTIVAS/VIDA GRUPO/ayudaventas vida grupo.pdf`
  - `autonomia__soluciones-colectivas__vida-grupo__ayudaventas-vida-grupo`
- Generated markdown and chunk artifact filenames were collision-safe and no
  longer depended on `Path.stem` alone.
- Processed metadata and chunk artifacts now include
  `source_pdf_relative_path` for stable source-tree traceability.
