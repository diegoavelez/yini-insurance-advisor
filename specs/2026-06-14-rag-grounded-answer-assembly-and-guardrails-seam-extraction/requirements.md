# Requirements

## Slice

`rag-grounded-answer-assembly-and-guardrails-seam-extraction`

## Goal

Extract the stabilized grounded-answer assembly, citation/basis derivation, and
guardrail-response helpers out of `rag/ingestion.py` into a dedicated `rag`
seam without changing current grounded-answer behavior.

## Context

After the Qdrant seam extractions, `rag/ingestion.py` still owns one cohesive
grounded-answer helper cluster covering:

- grounded prompt construction from retrieved chunks;
- citation and documentary-basis derivation from evidence chunks;
- grounding verification from evidence and citation availability;
- conservative typed refusal/limited-response builders for insufficient
  evidence, unsupported scope, prompt injection, and missing citations.

These helpers are stable enough to move behind their own seam while keeping
`generate_grounded_answer()` as the orchestration layer for retrieval,
selection, observability, and completion generation.

## Requirements

1. The grounded-answer assembly and guardrail helper cluster must move to a
   dedicated module under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the helper
   cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - prompt shape built from retrieved chunks;
   - citation and documentary-basis fields derived from chunks;
   - grounding confidence behavior for empty, weak, and citation-backed
     retrieval results;
   - conservative refusal/limited-response payloads for unsupported scope,
     prompt injection, insufficient evidence, and missing citations.
4. The slice must remain narrow:
   - `generate_grounded_answer()` may stay in `rag/ingestion.py`;
   - retrieval/reranking logic must not change;
   - Groq completion wiring and observability contracts must not change.

## Non-Goals

- changing retrieval ranking or evidence-selection heuristics;
- changing grounded-answer completion prompts beyond preserving existing shape;
- changing response contracts or observability event schemas;
- extracting the full `generate_grounded_answer()` orchestration path in this
  slice.
