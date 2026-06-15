# Plan

## Objective

Reduce `rag/ingestion.py` coupling by extracting stabilized document
canonicalization helpers into a dedicated module while preserving behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/document_canonicalization.py`
- `tests/test_document_canonicalization.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-document-canonicalization-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-document-canonicalization-seam-extraction/plan.md`
- `specs/2026-06-14-rag-document-canonicalization-seam-extraction/validation.md`

## Assumptions

- The current canonicalization behavior is already correct and should be
  preserved.
- Reexport-by-import from `rag/ingestion.py` is acceptable for compatibility.

## Risks

- Hidden coupling between metadata extraction and chunking could accidentally
  shift behavior if imports or helper boundaries are incomplete.
- Duplicate stale definitions could remain in `rag/ingestion.py` if the
  extraction is only partial.

## Verification Strategy

- Add focused seam tests for document metadata extraction and path-derived
  canonical values.
- Run focused pytest and lint on touched files.
- Re-run the live ARL remuneration query to confirm the broader ingestion
  module still behaves correctly after the extraction.
