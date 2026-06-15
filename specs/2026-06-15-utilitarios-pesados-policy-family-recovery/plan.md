# Plan

## Objective

Route explicit utilitarios y pesados coverage queries into the dedicated clausulado family without changing the existing guide path.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/2026-06-15-utilitarios-pesados-policy-family-recovery/requirements.md`
- `specs/2026-06-15-utilitarios-pesados-policy-family-recovery/validation.md`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`

## Assumptions

- `SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS` is the canonical normalized `document_name` for the policy family.
- The live corpus already contains the dedicated clausulado chunks in Qdrant.

## Risks

- The new routing rule must remain narrow enough to avoid hijacking unrelated movilidad policy queries.
- The guide-family rule must remain unchanged.

## Verification Strategy

- Run focused `pytest` and `ruff` for retrieval rules.
- Run live policy answering for the matrix query.
- Update roadmap and matrix only if the row passes.
