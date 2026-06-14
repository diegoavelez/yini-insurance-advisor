# Plan

## Objective

Restore direct retrieval for suscripción financing-individual evidence in `13.11`.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-financiacion-individual-retrieval-recovery/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-financiacion-individual-retrieval-recovery/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-financiacion-individual-retrieval-recovery/validation.md`

## Assumptions

- the relevant financing evidence already exists in the current indexed chunk set;
- the main failure is candidate recovery / ranking, not missing corpus content.

## Risks

- over-biasing unrelated financing or payment-plan queries;
- accidentally re-prioritizing individual financing over collective billing slices.

## Steps

1. Capture the live zero-result baseline.
2. Add a narrow financing-individual intent detector and candidate recovery path.
3. Prefer `13.11` financing-individual evidence for the documented query type.
4. Add focused tests and rerun the live query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- rerun live `retrieve-chunks` and `answer-query` for the documented query.
