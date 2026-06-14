# Plan

## Objective

Ensure repeated `Muévete Libre` coverage sections prefer the chunk that best
explains the insured event or benefit, not the chunk that mostly contains
activation or reminder language.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-muevete-libre-intrasection-coverage-chunk-prioritization/requirements.md`
- `specs/2026-06-13-muevete-libre-intrasection-coverage-chunk-prioritization/validation.md`

## Assumptions

- The retrieval pool already contains the right section.
- The remaining problem is choosing the best representative chunk for that
  section.

## Risks

- A descriptive heuristic that is too broad could penalize legitimate
  conditions or limit details in other products.

## Verification Strategy

- Add a focused unit test for repeated `4.1. Cobertura` candidates.
- Run focused `pytest` and `ruff`.
- Re-run one real `retrieve-chunks` and one real `answer-query`.
