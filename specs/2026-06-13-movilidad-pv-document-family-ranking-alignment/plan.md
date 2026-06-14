# Plan

## Objective

Restrict explicit movilidad PV benefit-intent retrieval to the
`PROPUESTA DE VALOR MOVILIDAD` document family through the existing curated
query-filter seam.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-pv-document-family-ranking-alignment/requirements.md`
- `specs/2026-06-13-movilidad-pv-document-family-ranking-alignment/validation.md`

## Assumptions

- both PV documents already persist the same canonical `document_name`;
- the existing filter-normalization seam already supports `document_name`;
- the remaining leakage comes from shared lexical anchors across mobility guides.

## Risks

- over-constraining nearby queries that mention PV indirectly;
- forgetting to verify local lexical recall also honors the new filter;
- documenting the slice too broadly.

## Steps

1. Add a curated `document_name` filter rule for explicit PV benefit-intent queries.
2. Add focused tests for normalization, Qdrant filter construction, and local lexical exclusion.
3. Update the roadmap with the new corrective slice.
4. Run targeted tests and lint.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- rely on a post-change operator rerun for live Qdrant confirmation if needed.
