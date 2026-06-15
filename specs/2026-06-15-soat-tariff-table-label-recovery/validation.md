# Validation

This slice is ready when SOAT tariff evidence preserves vehicle labels through
the live retrieval and grounded-answer path.

## Planned checks

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'soat_tariff_table'`
2. targeted rebuild of `MOVILIDAD/SOAT/tarifas soat 2026.pdf` ingestion,
   embeddings, and Qdrant indexing
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuáles son las tarifas SOAT 2026?' --product soat --document-type guide --top-k 5`
4. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuáles son las tarifas SOAT 2026?' --product soat --document-type guide --top-k 5`

## Expected evidence

- normalized SOAT tariff chunks contain labels such as `Motos`,
  `Autos familiares`, or equivalent vehicle-family text;
- live retrieval no longer returns bare numeric-only fragments in the leading
  tariff results;
- the live answer remains grounded in `tarifas soat 2026.pdf` while preserving
  usable vehicle labels.

## Recorded evidence

- `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'soat_tariff'` passed.
- `./.venv/bin/python -m ruff check rag/markdown_chunk_normalization.py tests/test_ingestion.py --ignore E501` passed.
- Targeted artifact rebuild succeeded for `MOVILIDAD/SOAT/tarifas soat 2026.pdf`:
  - `ingest-pdfs --glob 'MOVILIDAD/SOAT/tarifas soat 2026.pdf' --overwrite true`
  - `generate-embeddings --glob 'movilidad__soat__tarifas-soat-2026.chunks.json' --overwrite true`
  - `index-embeddings --glob 'movilidad__soat__tarifas-soat-2026.embeddings.json'`
- The rebuilt chunk artifact now preserves vehicle-family labels and tariff
  statements, for example:
  - `Motos / Código 10 / Ciclomotor: Prima: $ 80.100 ...`
  - `Autos familiares / Código 52 / Entre 1500 - 2500 c.c.: Prima: $ 356.800 ...`
- Live retrieval now returns labeled SOAT tariff chunks instead of raw
  numeric-only table fragments:
  - `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cuáles son las tarifas SOAT 2026?' --product soat --document-type guide --top-k 5`
- Live grounded answering now remains in `tarifas soat 2026.pdf` and surfaces
  labeled tariff categories in the answer table:
  - `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuáles son las tarifas SOAT 2026?' --product soat --document-type guide --top-k 5`
  - completed with `supported=true`, `confidence=high`, and citations only
    from `MOVILIDAD/SOAT/tarifas soat 2026.pdf`.
- Residual quality note:
  - some model-year subgroup labels remain approximate because the source PDF
    itself merges subgroup text awkwardly in a few rows, but the original P1
    blocker of unlabeled numeric-only tariff evidence is closed.
