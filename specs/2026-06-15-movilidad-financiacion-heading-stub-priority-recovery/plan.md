# Plan

## Objective

Demote heading-only financing-guide chunks and prioritize contentful procedural
evidence within `Manual Procedimiento Financiacion de polizas individuales`.

## Affected Files

- `rag/evidence_selection.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-15-movilidad-financiacion-heading-stub-priority-recovery/requirements.md`
- `specs/2026-06-15-movilidad-financiacion-heading-stub-priority-recovery/validation.md`

## Assumptions

- financing-guide document-family scoping already works;
- the remaining retrieval miss is caused by weak intra-family ordering;
- a local deterministic reranking fix is sufficient before reopening
  extraction.

## Risks

- over-penalizing short but legitimate financing chunks;
- accidentally affecting suscripción financing policy flows;
- introducing duplicate-section behavior regressions inside the guide family.

## Steps

1. Add a narrow financing-guide reranking path in `rag/evidence_selection.py`.
2. Add focused tests proving heading stubs lose priority to richer procedural
   chunks.
3. Re-run targeted validation for the live financing query.
4. Update roadmap and MVP acceptance notes with the result.

## Verification Strategy

- run focused `pytest` coverage for financing retrieval tests;
- run `ruff check` on touched Python files;
- rerun live `retrieve-chunks` and `answer-query` for
  `¿Cómo funciona la financiación de pólizas individuales?`.
