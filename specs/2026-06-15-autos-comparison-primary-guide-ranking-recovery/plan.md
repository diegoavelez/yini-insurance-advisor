# Plan

## Objective

Promote the main `DIFERENCIALES SURA` comparison guide for the broad AUTOS comparison smoke query using the existing operator-curated expansion seam.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-autos-comparison-primary-guide-ranking-recovery/requirements.md`
- `specs/2026-06-15-autos-comparison-primary-guide-ranking-recovery/validation.md`

## Assumptions

- `diferenciales planes autos.pdf` already contains the comparative evidence needed for the smoke query.
- The main gap is that the broad query does not activate the committed comparison rule set.

## Risks

- An overly broad `autos` comparison rule could affect non-comparison AUTOS prompts.
- The rule may improve document-family ranking but still leave section-level refinement for later.

## Steps

1. Add a broad AUTOS comparison expansion rule aligned to `DIFERENCIALES SURA` anchors.
2. Add regressions for query expansion and broad comparison reranking.
3. Run focused tests and live retrieval validation.
4. Update roadmap and MVP matrix to reflect whether the AUTOS row can move beyond `fail`.

## Verification strategy

- Run focused `pytest` coverage for broad AUTOS comparison queries.
- Run live `retrieve-chunks` for `¿Qué diferencia hay entre los planes de autos?`.
- Re-check that `¿Qué cubre el plan autos básico PT?` remains stable after the new rule.
