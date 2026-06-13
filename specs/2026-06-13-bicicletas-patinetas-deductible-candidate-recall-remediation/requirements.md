# Requirements

## Title

Improve local candidate recall scoring for deductible-intent mobility queries.

## Context

The current deductible retrieval gap is no longer caused by ingestion,
indexing, or final answer synthesis. Inspection shows the remaining issue is in
local lexical candidate scoring: deductible-intent queries still rank adjacent
`EXPEDICIÓN REQUISITOS` and loss-related chunks above the explicit
`DEDUCIBLE` chunk from the normalized `pv` document.

The next narrow slice should add a deterministic local scoring preference for
explicit deductible sections when the query intent is deductible-oriented.

## Scope

This slice should:

- keep retrieval contracts unchanged;
- add a narrow local lexical scoring preference for deductible-intent queries;
- preserve existing comparison and non-deductible query behavior.

This slice should not:

- redesign the full retrieval pipeline;
- introduce model-based reranking;
- change chunk or Qdrant payload schemas.

## Acceptance Criteria

- For deductible-intent mobility queries, local lexical candidate scoring
  prefers chunks whose label surface explicitly contains `deducible`.
- The normalized `pv` deductible chunk becomes a plausible top candidate.
- Existing retrieval regressions continue to pass.
