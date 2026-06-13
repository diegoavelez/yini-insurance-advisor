# Requirements

## Title

Align comparison-intent retrieval for `MOVILIDAD/MOTOS`.

## Context

The `MOTOS` category is now ingested, embedded, indexed, and usable for
coverage-style questions. Real validation showed a remaining retrieval gap for
the query `¿Qué diferencias hay entre los planes de motos?`.

The comparative artifact `comparativo motos.pdf` exists in the corpus, but the
current retrieval path does not prioritize it. Instead, answers are being
assembled mainly from `clausulado-plan motos.pdf`.

The narrowest next slice should activate the existing comparison-intent
retrieval machinery for `MOTOS` before opening deeper ingestion remediation.

## Scope

This slice should:

1. Add one operator-curated comparison query-expansion rule for `motos`.
2. Reuse the existing comparison candidate-pool, lexical-recall, and reranking
   path already implemented for comparison queries.
3. Add focused regression coverage for the new query-expansion rule.
4. Validate the real retrieval and answer path for the comparison query.

This slice should not:

- redesign chunking for `comparativo motos.pdf`;
- add a new retrieval algorithm;
- normalize the table structure unless this narrower rule-driven step fails.

## Required Behavior

### 1. MOTOS comparison-intent activation

Acceptance criteria:

- a query like `¿Qué diferencias hay entre los planes de motos?` matches a
  curated comparison rule;
- the expanded query appends `MOTOS`-specific comparison vocabulary already
  present in the comparative corpus.

### 2. Backward compatibility

Acceptance criteria:

- non-comparison behavior remains unchanged;
- existing comparison behavior for `AUTOS` remains unchanged.

### 3. Runtime validation

Acceptance criteria:

- the real `MOTOS` comparison query returns the comparative document more
  prominently than before, or clearly demonstrates that a deeper corrective
  slice is required next.
