# Plan

## Objective

Restrict explicit financing-guide queries to the
`Manual Procedimiento Financiacion de polizas individuales` document family
through the existing curated query-filter seam.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-financiacion-guide-family-ranking-alignment/requirements.md`
- `specs/2026-06-14-movilidad-financiacion-guide-family-ranking-alignment/validation.md`

## Assumptions

- the financing guide now has a usable text surface and stable canonical
  `document_name`;
- the remaining miss is ranking/scope leakage rather than extraction failure;
- the existing `document_name` filter seam is sufficient for a first narrow fix.

## Risks

- over-constraining nearby mobility financing questions that should remain
  broader;
- missing local lexical exclusion coverage;
- choosing overly narrow guide-intent phrases for the trigger rule.

## Steps

1. Add a curated `document_name` filter rule for explicit financing-guide intent.
2. Add focused tests for normalization, Qdrant filter construction, and local lexical exclusion.
3. Update roadmap/spec validation to reflect the new remaining slice.
4. Run targeted tests and live retrieval reruns.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run the financing live retrieval queries.
