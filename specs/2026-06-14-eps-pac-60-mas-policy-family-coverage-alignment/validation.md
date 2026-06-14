# Validation

This slice is ready when PAC stale artifacts no longer survive incremental
reruns and PAC policy-family queries resolve to the intended document family.

## Observed initial evidence

- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el PAC 60 Más?' --product 'pac' --document-type policy --top-k 5`
  returned `politicas asegurabilidad pac 60 mas.pdf` chunks only.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el clausulado PAC 60 Más?' --product 'pac' --document-type policy --top-k 5`
  also returned `politicas asegurabilidad pac 60 mas.pdf` chunks only.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product 'pac' --document-type policy --top-k 5`
  correctly returned asegurabilidad-family chunks.
- Artifact inspection then showed the first persisted `clausulado` PAC outputs
  had stale metadata (`document_type=None`, `product=None`) because they had
  been created before overlays existed and later skipped by `overwrite=false`.

## Corrective checks

- focused `pytest` for stale-artifact refresh and PAC family routing:
  - `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_embedding_generation.py tests/test_retrieval.py tests/test_query_scope.py -q -k 'pac or stale or skips_existing_artifact'`
- live retrieval for:
  - `¿Qué cubre el PAC 60 Más?`
  - `¿Qué cubre el clausulado PAC 60 Más?`
  - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`

## Closure evidence

- `./.venv/bin/python -m pytest tests/test_ingestion.py tests/test_embedding_generation.py tests/test_retrieval.py tests/test_query_scope.py -q -k 'pac or stale or skips_existing_artifact'` passed.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el PAC 60 Más?' --product 'pac' --document-type policy --top-k 5` now retrieves `clausulado pac 60 mas sura v1.pdf` first, anchored at `9. COBERTURA`.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué cubre el clausulado PAC 60 Más?' --product 'pac' --document-type policy --top-k 5` now retrieves `clausulado pac 60 mas sura v1.pdf` first, also anchored at `9. COBERTURA`.
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Qué condiciones de asegurabilidad tiene PAC 60 Más?' --product 'pac' --document-type policy --top-k 5` now retrieves `politicas asegurabilidad pac 60 mas.pdf` first.
