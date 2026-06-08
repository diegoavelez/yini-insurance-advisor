# Requirements

## Feature Summary

This feature defines the second narrow implementation slice of
`Phase 16 — Ingestion Runtime Remediation`.

The goal is to make Docling the explicit primary local ingestion backend,
allow it enough time to initialize and download required assets, and preserve a
controlled fallback path for local recovery when the user opts into it.

This slice must stay focused on local ingestion policy and runtime behavior.

## In Scope

- Make local ingestion default to a Docling-first backend policy.
- Increase and/or make configurable the Docling startup timeout for local runs.
- Add an explicit local warm-up path that allows Docling to download required
  assets before bulk ingestion.
- Preserve a selectable fallback mode for PDFium-based conversion when needed.
- Add or update targeted tests for backend selection and warm-up behavior.

## Out of Scope

- Broader ingestion architecture replacement.
- Embedding, retrieval, or Qdrant changes.
- Hosted deployment changes.
- Large-scale documentation rewrite beyond the local-ingestion policy notes
  required by this slice.

## Alignment Expectations

At minimum:

- Docling remains the preferred local conversion path;
- local operators can intentionally allow Docling startup and asset download;
- fallback behavior is explicit rather than silently overriding the preferred
  policy when the user requests Docling-only behavior.

## Acceptance Criteria

- The local ingestion CLI defaults to a Docling-first policy.
- The Docling startup timeout is configurable and practical for local runs.
- There is an explicit warm-up path for Docling asset download.
- Targeted tests cover backend selection and warm-up behavior.
