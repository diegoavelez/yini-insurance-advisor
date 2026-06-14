# Requirements

## Title

Balance `Muévete Libre` coverage evidence breadth across distinct coverage
sections.

## Context

The previous `muevete-libre-coverage-retrieval-alignment` slice fixed the
worst retrieval issue: generic sections such as `Glosario` or `Prima` no longer
outrank actual coverage sections.

Runtime evidence now shows a narrower remaining problem. Coverage-intent
queries still over-concentrate the final top-k on repeated chunks from one
stronger coverage section, especially `4.1. Cobertura`, even when the corpus
contains multiple relevant sibling coverage sections such as `1.1`, `2.1`,
`3.1`, `5.1`, `6.1`, and `7.1`.

The next narrow slice should improve evidence breadth without changing the
public retrieval contract or introducing probabilistic reranking.

## Scope

This slice should:

- keep retrieval, answer, citation, and chunk schemas unchanged;
- add a deterministic post-reranking breadth preference for explicit coverage
  sections;
- avoid repeating the same explicit coverage section before showing other
  available explicit coverage sections.

This slice should not:

- redesign semantic search;
- change embedding generation;
- force a product-specific hardcoded list of section ids inside the retrieval
  engine;
- introduce LLM reranking or summarization.

## Acceptance Criteria

### 1. Coverage breadth preference

- For coverage-intent queries, the final top-k prefers distinct explicit
  coverage sections before repeating a second chunk from the same section.

### 2. Deterministic ordering

- Explicit coverage sections can still be ordered deterministically using their
  numeric section labels when available.

### 3. Backward compatibility

- Existing SOAT and deductible retrieval tests continue to pass.
- The balancing rule stays scoped to coverage-intent queries and does not alter
  unrelated retrieval flows.
