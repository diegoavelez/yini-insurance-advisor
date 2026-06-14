# Plan

## Objective

Bias explicit collective billing prompts toward the `14.6.*` suscripción
subsections instead of adjacent financing-individual content.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-subsection-lineage-normalization/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-intent-alignment/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-intent-alignment/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-collective-billing-intent-alignment/validation.md`

## Assumptions

- the main remaining issue is lexical-semantic confusion between
  `facturación colectiva` and `financiación individual`;
- the current document family scoping is already good enough;
- a narrow intent-aware reranking adjustment should be sufficient.

## Risks

- overfitting to one phrasing of `facturación colectiva`;
- demoting valid financing content for prompts that genuinely ask about
  financing;
- accidentally affecting non-suscripción mobility retrieval.

## Steps

1. Capture the current collective-billing live retrieval pattern.
2. Add the smallest deterministic intent-alignment rule.
3. Add focused retrieval coverage.
4. Re-run the live collective billing query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run at least one live collective billing query.
