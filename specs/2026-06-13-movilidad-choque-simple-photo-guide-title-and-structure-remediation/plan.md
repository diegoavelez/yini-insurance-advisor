# Plan

## Objective

Improve citation and chunk readability for the `como tomar fotos choque
simple` guide without changing retrieval contracts.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-choque-simple-photo-guide-title-and-structure-remediation/requirements.md`
- `specs/2026-06-13-movilidad-choque-simple-photo-guide-title-and-structure-remediation/validation.md`

## Assumptions

- Retrieval already reaches the intended guide.
- The current issue is readability of persisted title/chunk text, not category
  scope or indexing coverage.

## Risks

- If heading rejection becomes too broad, legitimate titles could fall back to
  filename stems unnecessarily.

## Verification Strategy

- Add focused tests for noisy promotional title rejection.
- Add focused tests for section-prefix duplicate-heading suppression.
- Rebuild the affected guide artifacts and verify live retrieval output.
