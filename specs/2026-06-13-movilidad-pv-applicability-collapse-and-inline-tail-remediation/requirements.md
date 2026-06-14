# Requirements

## Title

Collapse narrow `PV` applicability duplication and remove residual inline
commercial tails.

## Context

After the first `PV` structure/dedup remediation, the transversal mobility
portfolio pair still showed two narrow residual problems:

- `pv portafolio movilidad v2` overproduced standalone `PLANES QUE APLICA`
  chunks due to chunk overlap in applicability-heavy sections;
- a small number of applicability-body lines still preserved inline commercial
  slogan tails when the markdown block started with a heading.

## Scope

This slice should:

- disable chunk overlap for pure `PV` applicability chunks;
- normalize heading-prefixed `PV` applicability bodies;
- preserve canonical applicability headings while removing residual inline
  commercial tails.

This slice should not:

- redesign generic overlap rules for the whole corpus;
- add retrieval reranking logic;
- index the `PV` cohort yet.

## Acceptance Criteria

### 1. Applicability overlap control

- Pure `PV` applicability chunks do not duplicate prior applicability entries
  only because of overlap rollover.

### 2. Inline tail cleanup

- Inline commercial slogan tails no longer survive in the reconstructed
  `pv portafolio movilidad v2` chunk artifacts.

### 3. Regression coverage

- Focused ingestion tests verify:
  - no-overlap behavior for `PV` applicability chunks;
  - canonicalization of equivalent applicability headings;
  - cleanup of heading-prefixed applicability bodies.
