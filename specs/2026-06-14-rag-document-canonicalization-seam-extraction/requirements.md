# Requirements

## Slice

`rag-document-canonicalization-seam-extraction`

## Goal

Extract document-identity and metadata canonicalization helpers out of
`rag/ingestion.py` into a dedicated `rag` seam without changing ingestion or
retrieval behavior.

## Context

`rag/ingestion.py` still contains a mixed cluster of document canonicalization
logic covering:

- document-name and version extraction from cleaned markdown;
- safe heading selection for `document_name`;
- canonical `source_pdf_id` derivation and ingestion artifact paths;
- path-based product/document-type inference plus overlay precedence;
- deterministic `ProcessedDocument` construction.

That cluster is stable and shared across ingestion and retrieval-adjacent flows,
so it is a good next extraction target after the ARL remuneration seam.

## Requirements

1. Document canonicalization helpers must move to a dedicated module under
   `rag/`.
2. `rag/ingestion.py` must import and use that seam instead of keeping the
   canonicalization logic inline.
3. The extraction must preserve current behavior for:
   - document metadata extraction from headings/version lines;
   - `source_pdf_id` generation and artifact path naming;
   - overlay-first product/document-type resolution.
4. Focused seam tests and the current live ARL validation path must continue to
   pass.

## Non-Goals

- changing markdown normalization behavior;
- changing chunking semantics;
- changing retrieval ranking or UI contracts.
