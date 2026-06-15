# Requirements

## Slice

`rag-pdf-conversion-and-markdown-cleaning-seam-extraction`

## Goal

Extract the stabilized PDF-conversion backend selection and markdown-cleaning
helpers out of `rag/ingestion.py` into a dedicated `rag` seam without changing
current ingestion behavior.

## Context

After the local hybrid-recall seam extraction, `rag/ingestion.py` still owns a
cohesive ingestion-preparation cluster covering:

- PDF-conversion backend availability checks;
- offline Hugging Face module resolution for Docling;
- Docling and PDFium conversion execution plus fallback selection;
- markdown usability checks before accepting converted output;
- conservative markdown cleanup before chunk building.

These helpers form a cohesive conversion/cleanup seam and are now the next
reasonable coupling-reduction candidate.

## Requirements

1. PDF-conversion and markdown-cleaning helpers must move to a dedicated module
   under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the helper
   cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - Docling-first conversion behavior;
   - PDFium fallback boundaries;
   - offline asset resolution behavior;
   - markdown-usability and cleanup outcomes used by chunking.
4. The slice must remain narrow:
   - ingestion orchestration stays in `rag/ingestion.py`;
   - chunk-building, embedding, and retrieval seams must not change;
   - CLI command contracts and observability schemas must not change.

## Non-Goals

- changing Docling timeout policy or warm-up commands;
- changing chunking, embeddings, or Qdrant indexing contracts;
- changing supported input formats beyond the current PDF flow;
- changing batch operator commands or deployment behavior.
