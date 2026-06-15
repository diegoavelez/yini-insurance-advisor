# Plan

## Objective

Route explicit bicicletas y patinetas coverage queries into the intended clausulado family without affecting the already-correct deductible path.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-15-bicicletas-patinetas-coverage-policy-family-recovery/requirements.md`
- `specs/2026-06-15-bicicletas-patinetas-coverage-policy-family-recovery/validation.md`

## Assumptions

- `SEGURO DE BICICLETA` is the canonical normalized `document_name` for the bicicletas/patinetas clausulado family.
- The current gap is routing/evidence-family alignment, not missing artifacts.

## Risks

- The canonical `document_name` mentions bicicleta singular even though the product family covers patinetas too.
- Overmatching could pull generic movilidad coverage queries away from transversales policy guidance.

## Steps

1. Add a narrow query-filter rule for explicit bicicletas/patinetas coverage intent.
2. Add repository and synthetic routing regressions.
3. Run focused tests and live retrieval/answer validation.
4. Update roadmap and matrix with the result.

## Verification strategy

- Run focused `pytest` coverage for bicicletas/patinetas coverage routing.
- Run live `retrieve-chunks` and `answer-query` for the coverage query.
- Re-run the deductible smoke query to confirm no regression.
