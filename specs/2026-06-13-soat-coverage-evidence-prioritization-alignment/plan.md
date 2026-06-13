# Plan

## Objective

Improve SOAT coverage evidence ordering so the summary coverage section is
returned before more incidental policy chunks.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- The curated SOAT coverage expansion terms are already narrow enough to support
  stronger exact-heading prioritization.

## Risks

- An overly large bonus could overfit and distort other retrieval slices.

## Verification Strategy

- run focused retrieval tests;
- run lint on touched Python modules;
- rerun SOAT retrieval and answer commands against runtime dependencies.
