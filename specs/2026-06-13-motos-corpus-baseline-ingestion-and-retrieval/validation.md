# Validation

This slice is ready when `MOVILIDAD/MOTOS` has a stable metadata baseline for
ingestion artifacts and the repository records that baseline explicitly.

## Acceptance Checks

- The spec bundle exists.
- The `MOTOS` overlay entries exist for all four source PDFs.
- `comparativo` source paths infer `document_type=guide`.
- Focused ingestion tests pass.
- The roadmap records the slice.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
- `./.venv/bin/python -m ruff check tests/test_ingestion.py ops/document-metadata-overlays.json ops/term-equivalences.json`

## Follow-on Runtime Validation

After this slice lands, the operator should run:

- category-only ingestion for `MOVILIDAD/MOTOS`
- category-only embeddings generation for `movilidad__motos__*.chunks.json`
- category-only Qdrant indexing for `movilidad__motos__*.embeddings.json`
- real retrieval queries for coverage, comparison, and small-events assistance

Any ranking issue found there should open a separate narrow corrective spec.
