# Validation

This slice is ready when `Muévete Libre` keeps its current live answer behavior
while no longer exposing flattened duplicate heading scaffolds.

## Planned Checks

1. `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_retrieval.py -q -k 'muevete_libre or muevete libre'`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py tests/test_retrieval.py`
3. `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'`
4. `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'`

## Expected Evidence

- normalized `Muévete Libre` markdown promotes a root heading plus nested
  section-group and clause headings;
- representative chunk records preserve parent-child lineage like
  `PLAN MUÉVETE LIBRE -> 2. Gastos de defensa judicial -> 2.1. Cobertura`;
- Qdrant indexing can prune legacy points for the same `source_pdf_id` once the
  collection also has a keyword index for that payload field;
- live coverage retrieval and grounded answering remain successful.

## Recorded Evidence

- `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_retrieval.py tests/test_qdrant_indexing.py -q -k 'muevete or libre or qdrant_indexing or prunes_legacy_points'` passed.
- `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py tests/test_qdrant_indexing.py` still fails only on pre-existing `E501` violations elsewhere in `tests/test_ingestion.py`; no new lint failure was introduced by this slice.
- `make batch-ingest BATCH_VENV=.venv BATCH_INPUT_DIR=data/raw BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/MUEVETE LIBRE/clausulado muevete libre v2.pdf' BATCH_OVERWRITE=true` passed.
- Local rebuilt `section_path` evidence now preserves hierarchy such as `PLAN MUÉVETE LIBRE -> SECCIÓN 1 Coberturas principales -> 2. Gastos de defensa judicial -> 2.1. Cobertura`.
- `make batch-index BATCH_VENV=.venv BATCH_PROCESSED_DIR=data/processed BATCH_EMBEDDING_GLOB='movilidad__muevete-libre__clausulado-muevete-libre-v2.embeddings.json'` now succeeds after adding the `source_pdf_id` payload index and pruning legacy points for that source.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'` now returns only normalized hierarchical chunks for the leading results, without the previous stale duplicate `1.2. Cobertura a la moto` payload.
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Qué cubre Muévete Libre?' --top-k 5 --product 'muevete libre'` succeeds with `confidence=high` and cites the normalized coverage sections `1.2`, `2.1`, `4.1`, `5.1`, and `6.1`.
