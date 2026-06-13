# Requirements

## Title

Add deterministic comparison-aware reranking for AUTOS plan-difference retrieval.

## Context

The repository already supports:

- operator-curated query alias expansion;
- operator-curated AUTOS comparison-term expansion;
- stable retrieval contracts over Qdrant-ranked chunks.

Real retrieval validation still shows that the AUTOS comparison query `¿Qué diferencias hay entre el plan básico y los otros planes de autos?` is dominated by the Plan Básico FAQ even after expansion, while the comparative `DIFERENCIALES SURA` document remains absent from the top results.

The next narrow slice should improve evidence selection for these comparison-intent queries without redesigning the retrieval contract or introducing probabilistic reranking.

## Scope

This slice should:

1. Detect when curated comparison-expansion rules matched a query.
2. Fetch a larger deterministic candidate pool for those queries only.
3. Apply a deterministic lexical reranking bias from the curated appended terms.
4. Keep non-comparison retrieval behavior unchanged.

This slice should not:

- change retrieval input/output contracts;
- introduce LLM-based reranking;
- redesign Qdrant payload shape;
- add broad product heuristics outside curated rule-driven behavior.

## Required Behavior

### 1. Comparison-aware candidate pool

When a query matches one or more curated comparison-expansion rules, retrieval should query a larger candidate pool before returning the final top-k.

Acceptance criteria:

- the final public `top_k` contract remains unchanged;
- non-comparison queries continue using the current Qdrant limit;
- comparison-aware queries use a deterministic larger candidate limit.

### 2. Deterministic reranking bias

Retrieved candidates should be reranked with a deterministic bias toward chunks that match curated comparison terms.

Acceptance criteria:

- reranking only applies when a curated comparison-expansion rule matched;
- bias is derived from the curated appended terms, not from hardcoded document ids;
- chunks with stronger matches in document-level labels or section labels can outrank weaker base hits;
- final outputs remain typed and ordered.

### 3. Backward compatibility

Existing retrieval behavior outside this narrow scenario should stay stable.

Acceptance criteria:

- current retrieval normalization tests still pass;
- current filter behavior still passes;
- missing rule files or unmatched rules leave retrieval ordering unchanged.

### 4. Documentation and roadmap

The repository should document that this is a narrow comparison-oriented retrieval bias.

Acceptance criteria:

- the new slice is recorded in the roadmap;
- the docs avoid claiming universal reranking or full semantic ranking control.
