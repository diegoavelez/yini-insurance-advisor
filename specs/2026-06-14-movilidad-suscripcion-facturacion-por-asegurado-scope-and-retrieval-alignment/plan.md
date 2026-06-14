# Plan

## Objective

Recover supported scope and evidence alignment for suscripción `facturación por asegurado` queries.

## Affected Files

- `core/query_scope.py`
- `rag/ingestion.py`
- `tests/test_query_scope.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-facturacion-por-asegurado-scope-and-retrieval-alignment/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-facturacion-por-asegurado-scope-and-retrieval-alignment/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-facturacion-por-asegurado-scope-and-retrieval-alignment/validation.md`

## Assumptions

- the relevant answer text already exists in the current indexed suscripción corpus;
- the main failures are deterministic scope admission and narrow retrieval prioritization.

## Risks

- over-broadening scope admission with generic plural or billing tokens;
- overfitting retrieval to one phrase in a way that harms adjacent suscripción intents.

## Steps

1. Add the narrow spec bundle.
2. Admit the documented query pattern into supported scope.
3. Add a narrow retrieval-intent preference for `facturación por asegurado`.
4. Add focused regressions and rerun the live query.

## Verification Strategy

- run focused scope and retrieval tests;
- run Ruff on touched files;
- rerun live `retrieve-chunks` and `answer-query` for the documented query.
