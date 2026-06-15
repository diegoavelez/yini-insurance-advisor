# Plan

## Objective

Normalize the `Muévete Libre` clausulado heading hierarchy so chunk structure,
citations, and roadmap status can reflect a semantically complete onboarding.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-muevete-libre-heading-hierarchy-normalization/requirements.md`
- `specs/2026-06-14-muevete-libre-heading-hierarchy-normalization/plan.md`
- `specs/2026-06-14-muevete-libre-heading-hierarchy-normalization/validation.md`

## Assumptions

- The current `Muévete Libre` retrieval ranking is already good enough; the
  remaining gap is structural chunk quality, not unsupported scope.
- A narrow document-specific markdown normalization is acceptable because this
  PDF has a stable, known heading pattern.

## Risks

- Over-normalizing heading levels could hide meaningful labels if the source PDF
  uses inconsistent numbering later in the document.
- If the new hierarchy changes chunk boundaries too aggressively, it could
  perturb existing retrieval behavior.

## Verification Strategy

- Add focused ingestion tests for normalized markdown and chunk assembly.
- Run focused `pytest` coverage for the new normalization plus existing
  `Muévete Libre` retrieval behavior.
- Run one real `retrieve-chunks` and one real `answer-query` validation for
  `¿Qué cubre Muévete Libre?`.
