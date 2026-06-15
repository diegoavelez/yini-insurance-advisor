# Plan

## Objective

Route explicit `Autos Básico PT` coverage queries into the intended plan-specific guide family without changing broader AUTOS retrieval behavior.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-autos-basico-pt-evidence-family-alignment/requirements.md`
- `specs/2026-06-15-autos-basico-pt-evidence-family-alignment/validation.md`

## Assumptions

- `Plan Autos Básico Pérdidas Totales` is the canonical `document_name` for explicit `Básico PT` guide intent.
- The current failure is driven by mixed guide-family retrieval, not by missing corpus artifacts.

## Risks

- Overmatching short `PT` phrasing could over-constrain broader AUTOS queries.
- Fixing the explicit plan query does not automatically resolve comparative AUTOS ranking.

## Steps

1. Add a narrow operator-curated `document_name` filter rule for explicit `Autos Básico PT` phrasing.
2. Add a narrow coverage-oriented query-expansion rule so the `Coberturas principales` table is recallable inside that family.
3. Add normalization/query-expansion regressions for synthetic and repository-loaded term-equivalence sets.
4. Run focused retrieval tests plus live retrieval/answer validation.
5. Update roadmap and MVP matrix with the partial remediation status.

## Verification strategy

- Run focused `pytest` coverage for the new AUTOS rule.
- Run live `retrieve-chunks` and `answer-query` for `¿Qué cubre el plan autos básico PT?`.
- Re-run the comparative AUTOS smoke query to determine whether the matrix row can be promoted or should remain partially open.
