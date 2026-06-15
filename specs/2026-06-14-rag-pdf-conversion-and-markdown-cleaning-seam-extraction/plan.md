# Plan

## Objective

Reduce `rag/ingestion.py` coupling by moving PDF conversion and markdown
cleanup helpers behind a dedicated `rag` seam while preserving current
ingestion behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/pdf_conversion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-pdf-conversion-and-markdown-cleaning-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-pdf-conversion-and-markdown-cleaning-seam-extraction/plan.md`
- `specs/2026-06-14-rag-pdf-conversion-and-markdown-cleaning-seam-extraction/validation.md`

## Assumptions

- The current Docling/PDFium routing behavior is already correct enough to
  preserve as-is.
- Existing ingestion tests cover the critical timeout/fallback and markdown
  cleanup behavior well enough to catch drift.
- Keeping top-level ingestion orchestration in `rag/ingestion.py` preserves the
  intended seam boundary for now.

## Risks

- Conversion helpers touch runtime imports and fallback logic, so partial
  extraction could leave hidden state or duplicated checks behind.
- Small markdown-cleanup drift could affect downstream chunk boundaries.
- Pulling full ingestion orchestration into the seam would make the slice too
  broad.

## Verification Strategy

- Run focused ingestion and lint checks on touched files.
- Re-run targeted conversion-path tests covering Docling-first behavior and
  PDFium fallback boundaries.
- Optionally validate one representative local warm-up or conversion smoke if
  the runtime is available.
