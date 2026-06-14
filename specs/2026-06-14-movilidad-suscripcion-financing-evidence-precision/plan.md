# Plan

## Objective

Tighten financing-individual evidence precision inside the suscripción policy family.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-financing-evidence-precision/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-financing-evidence-precision/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-financing-evidence-precision/validation.md`

## Assumptions

- the current indexed suscripción corpus already contains enough direct
  financing evidence in `13.11` and adjacent financing sections;
- the remaining issue is ranking / evidence-selection precision, not missing
  corpus coverage.

## Risks

- over-pruning context that is still useful for financing answers;
- making the fix too broad and accidentally suppressing legitimate collective
  policy evidence for other suscripción intents.

## Steps

1. Capture the live financing precision baseline.
2. Add a narrow precision preference for direct financing sections.
3. Reduce lateral sections when direct financing evidence is already sufficient.
4. Add focused tests and rerun the live financing query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- rerun live `retrieve-chunks` and `answer-query` for the documented financing
  query.
