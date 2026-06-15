# Requirements

## Slice

`rag-local-hybrid-recall-and-query-normalization-seam-extraction`

## Goal

Extract the stabilized retrieval-query normalization and local hybrid-recall
helpers out of `rag/ingestion.py` into a dedicated `rag` seam without changing
current retrieval behavior.

## Context

After the evidence-selection seam extraction, `rag/ingestion.py` still owns one
cohesive retrieval-preparation cluster covering:

- retrieval-query normalization with operator-curated term equivalences;
- domain-specific hybrid-recall term construction for stabilized movilidad
  billing and financing paths;
- local chunk filtering and deterministic lexical scoring for fallback recall;
- exact applicability deduplication for known PV retrieval paths.

These helpers form a cohesive local-recall seam and are now the next
reasonable coupling-reduction candidate.

## Requirements

1. Retrieval-query normalization and local hybrid-recall helpers must move to a
   dedicated module under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the helper
   cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - query normalization with term-equivalence expansion;
   - movilidad suscripción billing and financing lexical recall enrichment;
   - local lexical filtering and scoring behavior;
   - exact PV applicability deduplication.
4. The slice must remain narrow:
   - `retrieve_ranked_chunks` orchestration stays in `rag/ingestion.py`;
   - Qdrant, embedding, and grounded-answer seams must not change;
   - evidence-selection behavior must not change.

## Non-Goals

- changing the retrieved chunk contract or retrieval result contract;
- changing Qdrant retrieval or payload/index management;
- changing term-equivalence data files or operator-curated synonym content;
- changing CLI command behavior or observability schemas.
