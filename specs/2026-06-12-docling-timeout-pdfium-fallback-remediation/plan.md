# Plan

## Objective

Keep Docling as the primary local converter while preventing a single timeout
from blocking a batch ingestion run.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-12-docling-timeout-pdfium-fallback-remediation/requirements.md`
- `specs/2026-06-12-docling-timeout-pdfium-fallback-remediation/validation.md`

## Assumptions

- the main observed failure mode is a per-document Docling timeout;
- PDFium remains an acceptable local fallback for that isolated case;
- preserving explicit failure for non-timeout Docling errors is still the safer
  contract.

## Risks

- accidentally broadening fallback behavior too far;
- hiding genuine Docling parsing defects that should stay visible;
- leaving the AUTOS differential document unresolved if the fallback is not
  covered by tests.

## Verification Strategy

- add focused tests for timeout fallback under `backend="docling"`;
- add a focused negative test for non-timeout Docling errors;
- run targeted ingestion tests and lint checks.
