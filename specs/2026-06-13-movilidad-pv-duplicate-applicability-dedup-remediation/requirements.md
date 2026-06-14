# Requirements

## Title

Deduplicate exact standalone `PV` applicability chunks.

## Context

The `PV` readiness audit found that `pv portafolio movilidad v2` still
contained exact duplicate chunk surfaces, all of them under standalone
`PLANES QUE APLICA` sections. Those duplicates are not useful extra evidence;
they only dilute retrieval and spend vector budget.

## Scope

This slice should:

- deduplicate exact standalone `PLANES QUE APLICA` chunks for the mobility `PV`
  corpus after chunk assembly;
- keep merged benefit + applicability chunks intact;
- preserve deterministic chunk ordering and identifiers after deduplication.

This slice should not:

- deduplicate across unrelated section families;
- remove non-exact near-duplicates;
- change retrieval scoring or indexing behavior.

## Acceptance Criteria

### 1. Exact applicability dedup

- Exact duplicate standalone `PLANES QUE APLICA` chunk texts are emitted only
  once per document.

### 2. Narrow scope

- Non-standalone chunks and merged benefit/applicability chunks are preserved.

### 3. Regression coverage

- Focused tests verify exact duplicate removal and stable retention of distinct
  applicability chunks.
