# Requirements

## Title

Align movilidad PV benefit-intent retrieval with operator-curated query expansion and deterministic reranking.

## Context

The repository already supports:

- operator-curated query expansion rules;
- deterministic larger candidate pools when a curated expansion rule matches;
- deterministic lexical reranking over semantic and local lexical candidates.

The `PV` pair for `MOVILIDAD/TRANSVERSALES` is now indexed and retrievable, but
the real query `qué beneficios incluye la propuesta de valor de movilidad`
still surfaces weak evidence such as `Canales de atención` ahead of more
relevant benefit sections, and can still leak adjacent mobility guides into the
top results.

The next narrow corrective slice should align that query intent with the
already-implemented retrieval seams without redesigning the retrieval contract
or introducing probabilistic reranking.

## Scope

This slice should:

1. Add an operator-curated movilidad PV benefit-intent expansion rule.
2. Bias retrieval toward benefit-bearing PV sections through the existing
   deterministic expansion/reranking path.
3. Keep the retrieval API, payload contracts, and Qdrant schema unchanged.

This slice should not:

- introduce LLM-based reranking;
- add new Qdrant payload fields or filters;
- hardcode document ids in retrieval logic;
- redesign chunking for the PV corpus.

## Required Behavior

### 1. Curated PV benefit-intent expansion

Queries that clearly ask what the movilidad value proposition includes should
activate a curated expansion bundle with PV-specific benefit evidence.

Acceptance criteria:

- a query containing `propuesta de valor`, `movilidad`, and benefit-style
  wording such as `beneficios`, `incluye`, `diferenciales`, or `ventajas`
  matches a curated expansion rule;
- the expansion terms are curated evidence anchors from the PV corpus rather
  than generic mobility taxonomy terms;
- unmatched queries remain unchanged.

### 2. Deterministic ranking alignment

The existing deterministic reranking path should be able to lift PV benefit
sections ahead of weaker generic or lateral guide chunks when the curated rule
matches.

Acceptance criteria:

- matched PV benefit sections can outrank a generic `Canales de atención`
  section with a slightly higher base semantic score;
- adjacent mobility guides that do not match the curated PV anchors do not gain
  the same boost;
- the public retrieval result contract remains unchanged.

### 3. Backward compatibility

Existing retrieval behavior outside this narrow intent should stay stable.

Acceptance criteria:

- current retrieval tests outside this scenario still pass;
- the candidate-pool widening remains rule-driven and does not become global;
- if the rule file is absent or the query does not match, retrieval ordering
  falls back to the current behavior.

### 4. Documentation and roadmap

The roadmap should record that this is a narrow PV benefit-intent alignment
slice, not a general-purpose semantic reranker.

Acceptance criteria:

- the new slice is listed in the roadmap;
- the implementation note describes the scope as operator-curated and narrow.
