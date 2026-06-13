# Requirements

## Title

Bias deductible-intent retrieval toward `DEDUCIBLE` evidence for
`MOVILIDAD/BICICLETAS Y PATINETAS`.

## Context

The `pv` document now contains a normalized `DEDUCIBLE` chunk, and the
retrieval pipeline now expands deductible-related queries. However, real
validation still shows that deductible questions can be answered from adjacent
or weaker evidence instead of prioritizing the explicit `DEDUCIBLE` section.

The next narrow slice should add a deterministic reranking bias that prefers
`DEDUCIBLE` chunks when the query intent is clearly about deductible behavior.

## Scope

This slice should:

- keep the existing retrieval contracts unchanged;
- add a narrow deterministic reranking bias for deductible-intent queries;
- preserve existing comparison-oriented and general query behavior.

This slice should not:

- redesign the whole ranking system;
- introduce model-based reranking;
- change chunk, embedding, or Qdrant schemas.

## Acceptance Criteria

- For a query such as
  `¿Cuál es el deducible del seguro de bicicletas y patinetas?`,
  a chunk with `section == "DEDUCIBLE"` outranks weaker non-deductible chunks
  when both are otherwise plausible candidates.
- Existing retrieval regressions continue to pass.
