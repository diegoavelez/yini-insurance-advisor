# Requirements

## Title

Baseline-ingest the `PV` transversal mobility cohort and audit extraction
quality before retrieval alignment work.

## Context

After completing the `choque simple` cohort, the next highest-value transversal
group is the commercial `PV` pair:

- `pv portafolio movilidad v2.pdf`
- `pv planes movilidad v1.pdf`

These documents likely improve broad mobility-domain coverage for the MVP, but
they also carry high extraction risk because they are slide-like commercial
PDFs. The next narrow slice should ingest only this cohort, inspect the
resulting markdown/chunks, and decide whether the current Docling-first path is
good enough or if a dedicated remediation slice is required.

## Scope

This slice should:

- ingest only the `PV` transversal pair;
- verify that processed, cleaned-markdown, and chunk artifacts are generated;
- inspect the cleaned markdown and chunk outputs for extraction quality;
- capture the next recommended remediation slice if the extraction is not yet
  acceptable.

This slice should not:

- ingest the rest of `MOVILIDAD/TRANSVERSALES`;
- add new retrieval heuristics yet;
- broaden into `utilitarios`, `suscripción`, or `financiación` documents.

## Acceptance Criteria

### 1. Narrow cohort ingestion

- The `PV` pair is ingested as its own cohort using the committed operator
  flow.

### 2. Extraction audit

- Cleaned markdown and chunk artifacts are inspected for:
  - noisy title promotion;
  - repeated slide/cover headings;
  - broken reading order;
  - weak semantic sections.

### 3. Clear next action

- The slice ends with a concrete recommendation:
  - either the cohort is ready for embeddings/indexing, or
  - the next remediation slice is identified narrowly.
