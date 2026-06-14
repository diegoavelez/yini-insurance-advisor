# Validation

This slice is ready when the ARL commissions guide no longer carries obvious
portal boilerplate in its only retrieval chunk.

## Acceptance Checks

- The new spec bundle exists.
- Focused ingestion coverage proves the ARL commissions guide drops its UI
  boilerplate lines.
- Rebuilt chunk output keeps the procedural guide while removing the noisy
  `Capacidad ARL` and `sura` leftovers.
- Live retrieval still returns the commissions guide first for a representative
  commissions query.

## Baseline Gap Evidence

- The current cleaned markdown contains:
  - `C a p a c i d a d :   A R L`
  - `[   C a p a c i d a d   -   A R L ]`
  - `sura`
  - `sura sura`
- The current chunk surface includes those lines ahead of or between the real
  procedural bullets.

## Completion Evidence

- Focused ingestion coverage passes with:
  `./.venv/bin/python -m pytest tests/test_ingestion.py -q -k 'arl_commissions or arl_rui or rui'`
- Static verification passes with:
  `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
- Rebuilding the commissions guide artifact from cached markdown now yields one
  cleaner guide chunk without:
  - `C a p a c i d a d :   A R L`
  - `[   C a p a c i d a d   -   A R L ]`
  - standalone `sura`
  - standalone `sura sura`
- The rebuilt chunk still preserves the actual procedure:
  - enter `www.arlsura.com`
  - sign in
  - open `Intermediarios`
  - navigate to `Consultar Pago de Comisiones`
  - provide office + date range and generate
- Live indexing of the refreshed guide embedding artifact succeeds with:
  `./.venv/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl --glob 'arl__instructivos-consulta-de-comisiones-arl-sura-v2.embeddings.json' --fail-fast true`
- Live retrieval validation succeeds with:
  `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo consulto la liquidación de comisiones ARL?' --product arl --document-type guide --top-k 3`
- The live retrieval result now returns
  `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`
  first with the cleaned procedural surface and without the prior UI
  boilerplate.

## Follow-on Gap

- Live grounded-answer validation for
  `¿Cómo consulto la liquidación de comisiones ARL?` still cites the lateral
  guide `Actualización de cuenta bancaria para pago de comisiones ARL SURA` as
  secondary evidence even though the primary commissions guide already fully
  answers the question.
- The next narrow corrective slice is therefore
  `arl-comisiones-guide-family-answer-evidence-alignment`.
