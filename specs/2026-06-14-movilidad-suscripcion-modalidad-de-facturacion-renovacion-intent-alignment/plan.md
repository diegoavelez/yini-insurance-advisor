# Plan

## Objective

Prioritize collective-policy renewal billing-mode evidence over individual payment-change rules.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-modalidad-de-facturacion-renovacion-intent-alignment/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-modalidad-de-facturacion-renovacion-intent-alignment/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-modalidad-de-facturacion-renovacion-intent-alignment/validation.md`

## Assumptions

- the answer text already exists in the indexed suscripción corpus under `14.6.2`;
- the current issue is ranking precedence, not missing evidence or unsupported scope.

## Risks

- over-penalizing useful individual payment-change evidence for queries that are
  actually about individual plans;
- making the fix too broad by matching generic `renovación` or `forma de pago`
  language outside the collective-policy pattern.

## Steps

1. Capture the live renewal-query ranking baseline.
2. Add a narrow renewal-specific collective billing intent detector.
3. Prefer `14.6.2` renewal evidence over individual payment-change sections.
4. Add focused tests and rerun the live query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- rerun live `retrieve-chunks` and `answer-query` for the documented query.
