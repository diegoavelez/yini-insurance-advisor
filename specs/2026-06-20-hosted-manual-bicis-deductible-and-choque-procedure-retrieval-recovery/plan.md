# Plan

## Objective

Recover the two failing hosted manual MVP questions by tightening deterministic query-family routing in the operator-curated term-equivalence seam.

## Affected files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`
- `specs/2026-06-20-hosted-manual-bicis-deductible-and-choque-procedure-retrieval-recovery/requirements.md`
- `specs/2026-06-20-hosted-manual-bicis-deductible-and-choque-procedure-retrieval-recovery/validation.md`

## Assumptions

- The hosted Space path cannot depend on untracked local chunk artifacts for lexical recall.
- `pv bicis y patinetas v2` is the canonical guide-family `document_name` for deductible guidance.
- `EN EVENTOS DE CHOQUES` is the canonical guide-family `document_name` for the choque simple procedure guide.

## Risks

- Overmatching could capture broader movilidad deductible queries that are not about bicicletas/patinetas.
- Overmatching could capture choque simple photo queries if the procedure rule is not narrower than the existing photo/video rule.

## Steps

1. Add the two narrow query-filter rules ahead of the broader category defaults.
2. Add focused regression tests for repository-loaded hosted-style normalization.
3. Update roadmap and acceptance-matrix notes to record the hosted manual regression and the corrective slice.
4. Run focused retrieval tests.

## Verification strategy

- Run focused `pytest` coverage for bicicletas/patinetas deductible and choque simple procedure routing.
- Confirm the existing photo-intent and bicicletas/patinetas coverage tests still pass.
- Hand back the two hosted queries for manual Space revalidation after redeploy.
