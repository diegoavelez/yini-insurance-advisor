# Validation

This slice is ready when broad ARL remuneration-policy queries rank explicit
remuneration sections ahead of introductory policy sections.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval coverage proves broad remuneration intent reranks toward
  explicit remuneration sections.
- Live Qdrant retrieval for `¿Cuál es el esquema de remuneración del canal
  externo ARL?` returns remuneration sections before introductory channel
  sections.

## Baseline Gap Evidence

- The live broad remuneration query currently ranks:
  `Canales para la afiliación a ARL SURA`, document-title metadata, and
  `Canal externo:` ahead of `Clientes nuevos (venta) para el Canal Externo`.

## Completion Evidence

- Added narrow ARL remuneration-policy intent detection and reranking in
  `rag/ingestion.py`, including a slightly larger candidate-pool limit for this
  intent family and section-level prioritization toward explicit remuneration
  chunks.
- Added focused retrieval coverage in `tests/test_retrieval.py` proving that a
  broad remuneration query now ranks `Pago de comisiones por Atracción` and
  `Clientes nuevos (venta) para el Canal Externo` ahead of introductory ARL
  channel sections.
- Verified focused checks:
  - `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'arl_remuneration_policy_intent or collective_billing or retrieve_cli_prints_typed_result'`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- Live retrieval confirmation:
  - `retrieve-chunks --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`
    now returns remuneration sections first, led by
    `Pago de comisiones por Atracción`, followed by
    `Por cambio de intermediario`, `Política de designación de intermediarios
    en la Solución de Riesgos Laborales`, and
    `Clientes nuevos (venta) para el Canal Externo`.
  - The same live query with `--top-k 8` also keeps remuneration sections ahead
    of introductory channel sections.
