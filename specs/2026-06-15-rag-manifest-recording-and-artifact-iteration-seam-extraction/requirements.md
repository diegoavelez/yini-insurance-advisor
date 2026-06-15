# Requirements

## Slice

`rag-manifest-recording-and-artifact-iteration-seam-extraction`

## Goal

Extract deterministic manifest-record builders, JSONL appenders, and source/chunk/embedding artifact iteration helpers out of `rag/ingestion.py` into a dedicated `rag` seam without changing batch command outcomes.

## Context

After the artifact-assembly seam extraction, `rag/ingestion.py` still owns one cohesive batch-artifact bookkeeping cluster covering:

- ingestion, embedding, and indexing manifest-record construction;
- JSONL appending for those manifest surfaces;
- deterministic iteration over source PDFs, chunk artifacts, and embedding artifacts.

These helpers are deterministic and file-system oriented, and they remain a reasonable next coupling-reduction candidate while the batch command loops stay in `rag/ingestion.py`.

## Requirements

1. Manifest-record builders and artifact-iteration helpers must move to a dedicated module under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - ingestion manifest records for succeeded, skipped, and failed documents;
   - embedding-generation manifest records and failed-artifact fallback behavior;
   - indexing manifest records and failed-artifact fallback behavior;
   - deterministic sorted iteration of matching source PDFs, chunk artifacts, and embedding artifacts.
4. The slice must remain narrow:
   - batch command orchestration stays in `rag/ingestion.py`;
   - artifact assembly, retrieval, and grounded-answer seams must not change;
   - manifest schemas and CLI flags must not change.

## Non-Goals

- changing ingestion, embedding, or indexing command semantics;
- changing JSONL manifest formats or artifact filenames;
- changing retrieval or answer generation behavior;
- extracting the full batch command loops themselves.
