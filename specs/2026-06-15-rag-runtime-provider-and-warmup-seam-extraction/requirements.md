# Requirements

## Slice

`rag-runtime-provider-and-warmup-seam-extraction`

## Goal

Extract runtime backend checks, provider bridges, model/client loading, offline asset warmup helpers, and embedding/completion generation helpers out of `rag/ingestion.py` into a dedicated `rag` seam without changing warmup, retrieval, or answer command behavior.

## Context

After the recent ingestion seam extractions, `rag/ingestion.py` still owns a cohesive runtime/provider cluster covering:

- embedding provider validation and backend availability checks;
- Qdrant and Groq backend availability checks;
- Groq client creation and completion generation;
- SentenceTransformer loading with offline Hugging Face resolution;
- embedding asset validation and embedding-vector generation;
- warmup-adjacent support helpers used by runtime commands.

This cluster is the next reasonable post-onboarding coupling-reduction candidate, but it should be extracted as one runtime/provider bundle rather than as several micro-slices.

## Requirements

1. Runtime/provider helpers must move to a dedicated module under `rag/`.
2. `rag/ingestion.py` must consume that seam rather than keep the runtime/provider cluster inline.
3. Current behavior must remain unchanged for the validated paths, especially:
   - `sentence-transformers` remains the only supported local embedding provider;
   - backend-unavailable failures remain loud and deterministic;
   - offline Hugging Face resolution remains enforced for cached embedding model loads;
   - embedding warmup and grounded completion behavior remain unchanged;
   - retrieval and answer generation still use the same embedding/completion semantics.
4. The slice must remain narrow:
   - warmup commands may delegate to the seam but stay orchestrated in `rag/ingestion.py`;
   - top-level CLI dispatch, retrieval orchestration, and grounded-answer orchestration must not move;
   - PDF conversion helpers already extracted into `rag/pdf_conversion.py` must not be reworked.

## Non-Goals

- changing provider choices or supported runtime dependencies;
- changing retrieval ranking or grounded-answer logic;
- changing CLI flags, environment contracts, or startup diagnostics;
- changing batch-loop behavior that was already extracted.
