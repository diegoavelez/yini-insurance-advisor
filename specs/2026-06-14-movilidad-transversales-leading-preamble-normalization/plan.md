# Plan

## Objective

Remove sectionless leading chunks from the two choque-simple process guides.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-transversales-leading-preamble-normalization/requirements.md`
- `specs/2026-06-14-movilidad-transversales-leading-preamble-normalization/plan.md`
- `specs/2026-06-14-movilidad-transversales-leading-preamble-normalization/validation.md`

## Assumptions

- the current raw PDFs remain unchanged;
- the defect is caused by document-specific leading preamble handling, not by
  missing OCR or missing corpus files.

## Risks

- over-normalizing unrelated choque-simple guides that already behave well;
- accidentally duplicating heading hierarchy after root-heading promotion.

## Steps

1. Capture the current sectionless-leading-chunk baseline.
2. Add narrow document-specific preamble normalization for the two affected
   process guides.
3. Add focused ingestion tests for root-heading promotion and section recovery.
4. Rebuild the affected chunks and verify the first chunk is semantic.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched files;
- inspect the rebuilt chunk bundles for both affected documents.
