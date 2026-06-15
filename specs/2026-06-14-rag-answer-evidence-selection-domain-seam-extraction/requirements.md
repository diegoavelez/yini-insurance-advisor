# Requirements

## Slice

`rag-answer-evidence-selection-domain-seam-extraction`

## Goal

Extract the stabilized domain-specific retrieval reranking, answer-evidence
selection, and citation-evidence narrowing helpers out of `rag/ingestion.py`
into a dedicated `rag` seam without changing current retrieval or grounded
answer behavior.

## Context

After the grounded-answer seam extraction, `rag/ingestion.py` still owns one
cohesive domain-selection cluster covering:

- candidate-pool sizing for specific retrieval intents;
- domain-specific reranking and diversification of retrieved chunks;
- answer-evidence narrowing for movilidad suscripción financing prompts;
- citation-evidence narrowing for ARL commissions, ARL account-update,
  ARL/RUI normativity, and ARL remuneration overview prompts.

These helpers form a cohesive evidence-selection seam and are now the next
reasonable coupling-reduction candidate.

## Requirements

1. Domain-specific evidence-selection helpers must move to a dedicated module
   under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the helper
   cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - candidate-pool sizing for movilidad suscripción and ARL remuneration
     policy prompts;
   - reranking/diversification behavior for explicit coverage, movilidad PV,
     and movilidad suscripción prompts;
   - answer-evidence narrowing for movilidad suscripción financing prompts;
   - citation-evidence narrowing for ARL guide, RUI, and remuneration prompts.
4. The slice must remain narrow:
   - retrieval orchestration stays in `rag/ingestion.py`;
   - Qdrant, embedding, and grounded-answer assembly seams must not change;
   - query-normalization contracts must not change.

## Non-Goals

- changing the retrieved chunk contract or grounded-answer contract;
- changing lexical recall construction or local chunk-corpus loading;
- changing ARL remuneration domain helpers already extracted elsewhere;
- changing CLI command behavior or observability schemas.
