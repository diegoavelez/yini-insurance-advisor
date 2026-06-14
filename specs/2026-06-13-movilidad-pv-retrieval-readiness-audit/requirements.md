# Requirements

## Title

Audit retrieval readiness for the transversal mobility `PV` cohort.

## Context

The `PV` pair has already completed:

- baseline ingestion;
- structure and chunk-dedup remediation;
- applicability-overlap and inline-tail cleanup.

Before generating embeddings or indexing into Qdrant, the cohort needs an
explicit readiness audit to determine whether the remaining chunk shape is good
enough for retrieval or whether one more narrow remediation is justified.

## Scope

This slice should:

- inspect the final persisted chunk artifacts for:
  - chunk count;
  - applicability-chunk density;
  - merged benefit/applicability evidence;
  - duplicate chunk surfaces;
  - residual slogan noise;
- attempt one operational readiness signal through local embedding generation;
- conclude `go` or `no-go` for embeddings/indexing;
- update the roadmap with the next narrow slice if the cohort is not yet ready.

This slice should not:

- change retrieval or chunking logic;
- write to Qdrant;
- declare indexing readiness without evidence.

## Acceptance Criteria

### 1. Structural audit

- The final `PV` chunk artifacts are measured and summarized with explicit
  readiness indicators.

### 2. Operational signal

- Embedding generation is attempted or explicitly blocked with evidence.

### 3. Decision

- The audit ends with a documented `go/no-go` outcome and, if `no-go`, one
  narrow follow-up slice.
