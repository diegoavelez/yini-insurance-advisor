# Requirements

## Slice

`rag-batch-command-loop-and-failure-handling-seam-extraction`

## Goal

Extract the repeated ingestion, embedding-generation, and Qdrant-indexing batch-loop plus per-artifact failure-handling orchestration out of `rag/ingestion.py` into a dedicated `rag` seam without changing CLI command behavior.

## Context

After the artifact-assembly and manifest-recording seam extractions, `rag/ingestion.py` still owns one cohesive orchestration cluster across three batch commands:

- iterate matching source PDFs, chunk artifacts, or embedding artifacts;
- execute one per-artifact operation under `try/except`;
- recover failed records deterministically;
- append one manifest record per artifact;
- respect `fail_fast` and return stable command exit codes.

This repeated loop/failure-handling shape is now the next narrow coupling-reduction candidate.

## Requirements

1. Shared batch-loop and per-artifact failure-handling helpers must move to a dedicated module under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the repeated loop logic inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - ingestion continues to append one processed-document manifest record per source PDF;
   - embedding generation continues to recover failed records from either a loaded chunk bundle or a fallback artifact path;
   - indexing continues to recover failed records from either a loaded embedding bundle or a fallback artifact path;
   - `fail_fast=true` still stops on the first failed artifact;
   - `fail_fast=false` still records failures and continues;
   - no-match and missing-directory exits remain unchanged.
4. The slice must remain narrow:
   - artifact builders/loaders stay in their current seams;
   - retrieval, grounded answers, and warmup commands must not change;
   - CLI argument surface and manifest schemas must not change.

## Non-Goals

- changing ingestion/embedding/indexing artifact semantics;
- changing warmup flows or top-level CLI dispatch;
- changing manifest record schemas or artifact file naming;
- changing retrieval or answer-generation behavior.
