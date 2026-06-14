# Plan

## Objective

Improve the semantic structure of `choque simple` circular chunks so retrieval
and answer generation can cite more meaningful evidence sections.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-choque-simple-evidence-structuring-remediation/requirements.md`
- `specs/2026-06-13-movilidad-choque-simple-evidence-structuring-remediation/validation.md`

## Assumptions

- The current retrieval path already reaches the right document.
- The remaining problem is chunk structure and section readability.

## Risks

- Overfitting the circular normalization could affect unrelated official
  documents if the rules are too broad.

## Verification Strategy

- Add focused split-block tests.
- Run focused `pytest` and `ruff`.
- Re-run real `retrieve-chunks` for `choque simple` to verify better section
  readability.
