# Plan

> Superseded in canonical classification by
> `specs/2026-06-14-movilidad-utilitarios-pesados-category-reclassification-remediation/plan.md`.
> The guide-family rule remains valid, but the cohort no longer belongs to
> `MOVILIDAD/TRANSVERSALES`.

## Objective

Restrict explicit `utilitarios y pesados` guide-intent retrieval to the
`Seguro de Autos Utilitarios y Pesados` document family through the existing
curated query-filter seam.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-utilitarios-pesados-guide-family-ranking-alignment/requirements.md`
- `specs/2026-06-14-movilidad-utilitarios-pesados-guide-family-ranking-alignment/validation.md`

## Assumptions

- the cohort guide already persists the canonical
  `document_name = Seguro de Autos Utilitarios y Pesados`;
- the existing retrieval normalization seam already supports
  `document_name` query filter rules;
- the observed leakage is caused by overlapping commercial-guide anchors with
  `PROPUESTA DE VALOR MOVILIDAD`.

## Risks

- over-constraining nearby movilidad queries that mention utilitarios
  indirectly;
- applying the filter too broadly to policy intent;
- documenting the gap without preserving the live evidence that triggered it.

## Steps

1. Add a curated `document_name` filter rule for explicit cohort guide intent.
2. Add focused tests for normalization, Qdrant filter construction, and local lexical exclusion.
3. Update the roadmap with the corrective slice and completed baseline status.
4. Run targeted tests and lint.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run the two live cohort queries after implementation.
