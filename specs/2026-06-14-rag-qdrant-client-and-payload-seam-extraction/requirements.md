# Requirements

## Slice

`rag-qdrant-client-and-payload-seam-extraction`

## Goal

Extract the stabilized Qdrant payload-mapping, filter-construction, and
collection-bootstrap helpers out of `rag/ingestion.py` into a dedicated `rag`
seam without changing current indexing or retrieval behavior.

## Context

After the lexical-normalization, ARL-remuneration, document-canonicalization,
and markdown/chunk-normalization extractions, `rag/ingestion.py` still owns one
cohesive Qdrant integration cluster covering:

- point id and payload construction for embedding bundles;
- typed retrieval-filter translation into Qdrant filter objects;
- source-document family filters used by targeted pruning paths;
- collection creation/validation and payload-index bootstrap.

That cluster is stable enough to stand behind its own seam and is now the next
reasonable coupling-reduction candidate.

## Requirements

1. Qdrant payload and collection helpers must move to a dedicated module under
   `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the Qdrant helper
   cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - deterministic point id generation from `chunk_id`;
   - payload field names and values used by indexing and retrieval;
   - retrieval filter semantics for `document_type`, `product`,
     `document_name`, and `version`;
   - collection bootstrap and payload-index compatibility behavior.
4. The slice must remain narrow: it should not change ranking logic,
   grounded-answer generation, or chunk/embedding contracts.

## Non-Goals

- changing Qdrant collection names, schemas, or payload field meanings;
- changing retrieval ranking heuristics or local lexical fusion;
- changing grounded-answer prompt construction;
- introducing a new storage backend abstraction beyond the dedicated Qdrant
  seam.
