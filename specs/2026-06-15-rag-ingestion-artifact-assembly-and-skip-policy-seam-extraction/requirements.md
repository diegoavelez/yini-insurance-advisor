# Requirements

## Slice

`rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction`

## Goal

Extract chunk-record assembly, chunk/embedding bundle construction, persisted
artifact compatibility checks, and artifact reuse/skip policy out of
`rag/ingestion.py` into a dedicated `rag` seam without changing ingestion or
embedding command behavior.

## Context

After the PDF-conversion seam extraction and the ingestion correctness
remediation, `rag/ingestion.py` still owns one cohesive artifact-management
cluster covering:

- chunk-record assembly from cleaned markdown;
- chunk-bundle and embedding-bundle construction;
- persisted chunk/embedding artifact loading and compatibility checks;
- per-document artifact reuse policy for `overwrite=false`.

These helpers form a cohesive artifact-assembly seam and are now the next
reasonable coupling-reduction candidate.

## Requirements

1. Artifact assembly and compatibility helpers must move to a dedicated module
   under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the cluster
   inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - chunk emission and section-context behavior;
   - propagated `document_type` and `product` metadata on chunk bundles;
   - embedding-bundle payload metadata and skip behavior;
   - `overwrite=false` reuse of compatible or legacy artifacts;
   - explicit metadata-refresh regeneration behavior.
4. The slice must remain narrow:
   - CLI/runtime orchestration stays in `rag/ingestion.py`;
   - PDF conversion, retrieval, and grounded-answer seams must not change;
   - manifest record schemas must not change.

## Non-Goals

- changing chunk contracts, embedding contracts, or Qdrant indexing contracts;
- changing markdown normalization or PDF conversion behavior;
- changing command-line flags or manifest formats;
- changing retrieval or answer generation behavior.
