# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 2 — PDF Processing Pipeline`.

The goal is to specify the ingestion skeleton only:

- Docling setup expectations
- admin CLI ingestion entrypoint
- reproducible storage layout
- explicit failure reporting
- typed processed-document contracts

## In Scope

- Define the CLI-first ingestion execution model.
- Define the storage layout for raw PDFs, markdown outputs, and processed
  documents.
- Define the processed-document contract surface needed by later cleaning and
  chunking work.
- Define Docling dependency and runtime assumptions for local and container use.
- Define explicit ingestion success and failure reporting behavior.

## Out of Scope

- Full markdown cleaning and normalization heuristics.
- Semantic chunking.
- Embeddings generation.
- UI ingestion triggers.
- Qdrant integration.

## Execution Model

The first ingestion path should be an admin-only offline CLI job.

Rationale:

- reproducible runs;
- easier local and container validation;
- no coupling to unfinished UI/runtime paths.

### CLI Contract

The first slice should reserve one canonical ingestion command:

```bash
python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "*.pdf" \
  --overwrite false \
  --fail-fast false
```

Required arguments:

- `--input-dir`
- `--markdown-dir`
- `--processed-dir`
- `--manifest-path`

Optional arguments:

- `--glob` default `*.pdf`
- `--overwrite` default `false`
- `--fail-fast` default `false`

The command should exit non-zero when:

- Docling is unavailable;
- the input directory is missing;
- no matching PDF files are found;
- one or more conversions fail while `--fail-fast=true`.

## Storage Layout

The slice should treat these locations as the baseline storage contract:

- `data/raw/` for source PDFs
- `data/markdown/` for Docling markdown output
- `data/processed/` for cleaned or normalized document artifacts and metadata

Each processed document contract should preserve the relationship between the
original PDF and derived outputs.

### Naming and Path Rules

- Each source document is identified by `source_pdf_id`, derived from the PDF
  filename stem.
- This first slice assumes source filenames are unique within `data/raw/`.
- Markdown output path should be `data/markdown/<source_pdf_id>.md`.
- Processed metadata path should be `data/processed/<source_pdf_id>.json`.
- Manifest output should be append-only JSONL at the configured manifest path,
  with one record per ingestion attempt.

If a future slice introduces explicit version metadata, it may extend
`source_pdf_id` or processed metadata fields, but this slice should not invent
version parsing heuristics.

### Re-run Policy

- Default behavior with `--overwrite=false`:
  - if markdown and processed outputs already exist for a source PDF, mark the
    attempt as `skipped` and keep existing artifacts unchanged;
  - still write a manifest record for the skipped attempt.
- With `--overwrite=true`:
  - regenerate markdown and processed metadata for matching files;
  - write a fresh manifest record for the new attempt.

This slice should not delete prior manifest records.

## Processed-Document Contract Surface

The first contract set should cover:

- source PDF identity
- source path
- markdown output path
- processed output path
- document name / version metadata when available
- ingestion status
- explicit error reporting fields

The minimum status vocabulary should be:

- `succeeded`
- `failed`
- `skipped`

Each manifest or processed-document record should include:

- `source_pdf_id`
- `source_pdf_path`
- `markdown_output_path`
- `processed_output_path`
- `document_name`
- `document_version`
- `ingestion_status`
- `error_message`
- `ingested_at`

### Reproducibility Rules

This slice must treat ingestion as a reproducible offline job:

- the same input file set and flags should produce the same output paths;
- status reporting should not depend on UI state;
- artifact locations should be deterministic from the CLI inputs;
- Docling availability should be validated through a non-network local check or
  fail loudly before conversion begins.

## Acceptance Criteria

- The ingestion flow is specified as a CLI contract, not an app route.
- Raw, markdown, and processed storage expectations are explicit.
- Docling dependency assumptions are explicit enough for local and container
  setup.
- The processed-document contract surface is specified for later implementation.
- Failure reporting is part of the contract, not an afterthought.
- Re-run behavior and output naming rules are explicit.
