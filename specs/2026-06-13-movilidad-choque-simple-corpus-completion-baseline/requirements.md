# Requirements

## Title

Complete the baseline onboarding workflow for the remaining `choque simple`
transversal corpus.

## Context

The current mobility retrieval seam for `choque simple` is already functional,
but it relies primarily on `circular choque simple.pdf`. The remaining
`choque simple` PDFs in `MOVILIDAD/TRANSVERSALES` should be ingested as one
coherent operational cohort so validation can cover the full advisor workflow:
legal basis, evidence capture, attention flow, and recobro flow.

## Scope

This slice should:

- make the local batch workflow explicitly support running a narrow raw-PDF
  cohort by glob without editing commands manually each time;
- document the `choque simple` cohort commands for ingestion, embeddings, and
  indexing;
- keep the current metadata overlays and term-equivalence seams unchanged.

This slice should not:

- reclassify unrelated transversal documents;
- widen the cohort to all remaining `MOVILIDAD/TRANSVERSALES` PDFs;
- introduce new retrieval heuristics;
- run broad quality remediations for `pv` or utilitarian-plan documents.

## Acceptance Criteria

### 1. Narrow cohort support

- The documented batch workflow can target only the `choque simple` PDFs in
  `MOVILIDAD/TRANSVERSALES` using committed repo commands or variables.

### 2. Traceable operator procedure

- The playbook documents the cohort commands for:
  - ingestion;
  - embeddings generation;
  - Qdrant indexing.

### 3. Backward compatibility

- The generic batch workflow still supports full-tree ingestion.
- The change remains a thin operator-flow improvement, not a runtime contract
  redesign.
