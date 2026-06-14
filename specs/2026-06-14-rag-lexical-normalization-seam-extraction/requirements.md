# Requirements

## Title

Extract the shared lexical term-equivalence helpers from `rag/ingestion.py`.

## Context

The current retrieval stack is still onboarding additional categories, so a
large refactor across retrieval, chunking, and domain heuristics would add
unnecessary operational risk. However, graph inspection shows that the
lexical-equivalence helpers have become the narrowest high-leverage seam for
preventing further coupling growth while new categories continue to land.

This slice is therefore a preventive extraction, not a behavior rewrite.

## Scope

This slice should:

1. extract the shared lexical normalization helpers into a dedicated
   `rag` module;
2. preserve current retrieval behavior and existing imports from
   `rag.ingestion`;
3. add focused unit coverage for the extracted helper surface.

This slice should not:

- refactor retrieval orchestration or grounded-answer generation;
- move domain-specific ARL or movilidad ranking heuristics;
- change the accepted term-equivalence contract or operator JSON format.

## Required Behavior

### 1. Dedicated lexical seam

Acceptance criteria:

- a new dedicated module owns the shared lexical normalization helpers;
- `rag/ingestion.py` imports those helpers instead of defining them inline.

### 2. Behavioral stability

Acceptance criteria:

- query normalization and term-equivalence behavior remain unchanged;
- the existing retrieval tests that depend on term-equivalence normalization
  still pass without fixture rewrites.

### 3. Traceability

Acceptance criteria:

- the roadmap records this preventive corrective slice near the existing
  operator-curated term-equivalence work;
- the validation file names the focused commands that prove no regression.
