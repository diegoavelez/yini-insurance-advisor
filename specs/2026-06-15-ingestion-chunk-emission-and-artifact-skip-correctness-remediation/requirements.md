# Requirements

## Slice

`ingestion-chunk-emission-and-artifact-skip-correctness-remediation`

## Goal

Restore the intended ingestion behavior for minimal converted markdown,
follow-on section-context chunk splitting, and `overwrite=false` reuse of
legacy artifacts without broadening into another architectural refactor.

## Context

Focused `tests/test_ingestion.py` currently expose two root-cause-sized
regressions:

- chunk emission can drop all chunks for minimal heading-only converted
  markdown and can under-split follow-on chunks because section-path prefix
  length is not reflected in chunk assembly;
- `overwrite=false` can re-run ingestion against older artifacts that lack the
  newer metadata fields, instead of treating those legacy artifacts as
  reusable when no stronger metadata signal was explicitly requested.

These failures break ingestion determinism more directly than the next planned
seam extraction and should be corrected first.

## Requirements

1. `build_chunk_records()` must emit at least one valid chunk for minimal
   converted markdown surfaces that still carry useful heading context.
2. `build_chunk_records()` must split follow-on chunks using effective chunk
   size that reflects injected section-path heading prefix context.
3. Chunk bundles produced during ingestion must again contain propagated chunk
   records for the success-path tests that assert `document_type` and `product`
   on the first chunk.
4. `overwrite=false` must treat legacy artifacts with missing metadata fields
   as reusable when no explicit overlay-driven metadata refresh was requested.
5. Explicit metadata-refresh scenarios must still regenerate stale artifacts
   when the operator provides the overlay path or another stronger metadata
   signal.

## Non-Goals

- extracting another seam or changing roadmap refactor sequencing;
- changing document canonicalization rules or metadata overlay content;
- changing chunk contract fields or embedding/indexing contracts;
- changing Docling/PDFium runtime behavior.
