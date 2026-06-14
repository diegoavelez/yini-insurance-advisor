# Validation

This slice is ready when broad ARL remuneration overview queries lead with the
explanatory overview chunk while explicit percentage queries still lead with the
table chunk.

## Acceptance Checks

- The new spec bundle exists.
- Focused retrieval tests prove overview-first behavior for broad schema queries
  and table-first behavior for explicit percentage queries.
- Live retrieval confirms both behaviors against Qdrant Cloud.

## Baseline Gap Evidence

- The live broad query `¿Cuál es el esquema de remuneración del canal externo
  ARL?` currently leads with `Pago de comisiones por Atracción` instead of the
  explanatory `Clientes nuevos (venta) para el Canal Externo` chunk.

## Completion Evidence

- Added narrow ARL remuneration overview-vs-table intent handling in
  `rag/ingestion.py`, including exact overview-chunk detection for
  `Clientes nuevos (venta) para el Canal Externo`, explicit table-intent
  detection for percentage/sector prompts, and deterministic front-loading of
  the correct evidence family.
- Added focused retrieval coverage in `tests/test_retrieval.py` proving:
  - broad remuneration overview prompts rank the explanatory overview chunk
    first;
  - explicit percentage/sector prompts keep the table chunk first.
- Verified focused checks:
  - `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'arl_remuneration_policy_intent or arl_remuneration_table_intent'`
  - `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_retrieval.py`
- Live retrieval confirmation:
  - `retrieve-chunks --query '¿Cuál es el esquema de remuneración del canal externo ARL?' --product arl --document-type policy --top-k 5`
    now leads with
    `Clientes nuevos (venta) para el Canal Externo`.
  - `retrieve-chunks --query '¿Qué porcentajes de comisión por sector tiene ARL en el canal externo?' --product arl --document-type policy --top-k 5`
    continues to lead with
    `Pago de comisiones por Atracción`.
- Representative ARL verification also remains healthy for the other three
  documents:
  - `retrieve-chunks` and `answer-query` for the ARL/RUI normativity FAQ;
  - `retrieve-chunks` and `answer-query` for the commissions guide;
  - `retrieve-chunks` and `answer-query` for the account-update guide.
- Representative broad ARL remuneration `answer-query` now completes with
  `confidence=high` and starts from the overview-first evidence family.
