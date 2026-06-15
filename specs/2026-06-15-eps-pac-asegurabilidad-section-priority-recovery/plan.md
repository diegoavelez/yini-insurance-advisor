# Plan

## Objective

Promote the direct asegurabilidad sections inside `politicas asegurabilidad pac 60 mas.pdf` for the explicit `PAC 60 Más` asegurabilidad smoke query.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-eps-pac-asegurabilidad-section-priority-recovery/requirements.md`
- `specs/2026-06-15-eps-pac-asegurabilidad-section-priority-recovery/validation.md`

## Assumptions

- The answer-bearing sections already exist in the indexed `PAC 60 Más` asegurabilidad family.
- The remaining gap is ranking/citation tightness, not missing corpus data.

## Risks

- Over-expansion could bias other PAC policy prompts toward the `GRUPOS ASEGURABLES` section.
- The top result may improve while still leaving some duplicate lower-ranked chunks in the evidence set.

## Steps

1. Add a narrow PAC 60 Más asegurabilidad expansion rule with direct section anchors.
2. Add regressions for query expansion and reranking.
3. Run focused tests and live retrieval/answer validation.
4. Update roadmap and MVP matrix based on the result.

## Verification strategy

- Run focused `pytest` coverage for PAC asegurabilidad.
- Run live `retrieve-chunks` and `answer-query` for `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`.
- Confirm the top evidence now comes from `GRUPOS ASEGURABLES` or direct age/admission sections.
