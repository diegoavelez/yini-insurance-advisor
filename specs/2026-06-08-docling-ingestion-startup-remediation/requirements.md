# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 16 — Ingestion Runtime Remediation`.

The goal is to diagnose and remediate the current local Docling startup block
that prevents the repo from converting sample PDFs into markdown artifacts in a
reasonable development loop.

This slice must stay focused on ingestion-runtime remediation.

## In Scope

- Record concrete evidence of where the current Docling startup path blocks.
- Determine whether the practical fix is:
  - runtime/config adjustment,
  - dependency-path remediation,
  - warm-up/documented constraint,
  - or an explicit approved local fallback path.
- Implement the minimum safe remediation needed to restore local
  PDF-to-markdown ingestion for sample files, or document the approved fallback
  path if a direct runtime fix is not feasible in-scope.
- Add or update targeted validation for the chosen remediation path.

## Out of Scope

- Broad redesign of the RAG pipeline.
- Embedding or retrieval changes unrelated to PDF-to-markdown ingestion.
- Hosted deployment changes.
- Large-scale ingestion architecture replacement beyond the minimum safe local
  remediation needed here.

## Alignment Expectations

At minimum:

- the remediation must be evidence-driven and tied to the observed startup
  block;
- the repo must end this slice with a practical local path to produce markdown
  artifacts from sample PDFs;
- the change should stay narrow and avoid speculative rewrites.

## Acceptance Criteria

- The current Docling startup block is documented with concrete evidence.
- A practical local remediation or approved fallback path is implemented.
- Sample PDF ingestion can proceed to markdown artifact generation through the
  chosen path.
- The slice remains narrowly scoped to ingestion runtime remediation.
