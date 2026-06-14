# Plan

## Objective

Prefer the clean leading `14.6.2` billing chunk over later fragmentary
continuations.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-intent-alignment/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-leading-chunk-prioritization/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-leading-chunk-prioritization/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-leading-chunk-prioritization/validation.md`

## Assumptions

- the current top result is already in the correct subsection;
- the remaining issue is choosing the wrong chunk within that subsection;
- a narrow deterministic chunk-quality preference should be sufficient.

## Risks

- overfitting to one subsection continuation artifact;
- harming other good continuation chunks that are actually more complete;
- widening the fix beyond this documented collective billing pattern.

## Steps

1. Capture the current `14.6.2` chunk ordering pattern.
2. Add the smallest leading-chunk preference.
3. Add focused retrieval coverage.
4. Re-run the live collective billing query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run at least one live collective billing query.
