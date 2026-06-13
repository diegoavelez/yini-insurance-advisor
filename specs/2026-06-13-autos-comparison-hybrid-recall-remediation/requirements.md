# Requirements

## Title

Add deterministic hybrid recall for comparison-oriented retrieval misses.

## Context

The AUTOS comparative document still does not enter the semantic candidate pool after query expansion, candidate-pool growth, section-context prefixing, same-section aggregation, and comparison-table normalization. This shows the remaining bottleneck is recall, not only representation.

The next narrow slice should add a deterministic hybrid recall path for comparison-oriented queries by combining semantic retrieval with local lexical candidates from persisted chunk artifacts.

## Scope

This slice should:

1. Reuse existing comparison-intent expansion rules as the activation gate.
2. Retrieve a small lexical candidate set from local chunk artifacts.
3. Merge lexical and semantic candidates deterministically before final reranking.
4. Preserve existing typed retrieval contracts.

This slice should not:

- replace Qdrant semantic retrieval;
- introduce external search engines or BM25 infrastructure;
- change chunk, embedding, or response contracts;
- activate lexical recall for ordinary non-comparison queries.

## Required Behavior

### 1. Comparison-gated lexical recall

When one or more operator-curated comparison expansion rules match the query, retrieval may gather additional local lexical candidates from persisted chunk artifacts.

Acceptance criteria:

- activation stays tied to the existing matched comparison rules;
- non-comparison queries do not pay the extra local recall cost;
- lexical recall remains deterministic and local-only.

### 2. Filter-aware local candidates

Lexical candidates must respect the same typed retrieval filters as semantic candidates.

Acceptance criteria:

- `product`, `document_type`, `document_name`, and `version` filters are honored;
- mismatched local chunks are excluded.

### 3. Deterministic hybrid fusion

Semantic and lexical candidates should be merged and then pass through the existing deterministic reranking layer.

Acceptance criteria:

- duplicate chunk ids are merged deterministically;
- strong lexical comparison evidence can surface a comparative chunk even if Qdrant semantic recall misses it;
- final output remains a `DocumentRetrievalResult` with unchanged shape.

### 4. Backward compatibility

Acceptance criteria:

- existing semantic-only retrieval behavior remains unchanged for ordinary queries;
- focused retrieval tests pass;
- roadmap records the slice.
