# Plan

## Objective

Ensure `Muévete Libre` coverage-intent retrieval returns a broader first-page
evidence set across distinct coverage sections instead of repeating one
dominant section.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-muevete-libre-coverage-breadth-evidence-balancing/requirements.md`
- `specs/2026-06-13-muevete-libre-coverage-breadth-evidence-balancing/validation.md`

## Assumptions

- The current corpus quality is adequate.
- The remaining issue is ordering breadth, not missing relevant chunks.

## Risks

- Over-diversifying could hide the single strongest chunk if breadth is applied
  too early or too broadly.
- Numeric section ordering may not be meaningful for every future product, so
  the rule must stay tightly scoped to explicit coverage-intent flows.

## Verification Strategy

- Add a focused retrieval test proving distinct coverage-section breadth.
- Run focused `pytest` and `ruff`.
- Re-run one real `retrieve-chunks` and one real `answer-query` for
  `Muévete Libre`.
