# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 16 — Ingestion Runtime Remediation`.

The goal is to support real-world local source trees where PDFs arrive inside
nested product/category folders, without requiring manual flattening or
renaming of the original files.

## In Scope

- Discover source PDFs recursively under the configured raw input directory.
- Derive collision-safe document ids from the relative source path rather than
  from `Path.stem` alone.
- Prevent output artifact collisions when two PDFs share the same filename in
  different source folders.
- Preserve stable source-path traceability in processed metadata and chunk
  artifacts.
- Add targeted tests for recursive discovery and path-derived id behavior.

## Out of Scope

- XLSX or non-PDF ingestion.
- Replacing the current Docling/PDFium conversion backends.
- Retrieval-ranking, embedding-model, or Qdrant-schema redesign.
- Large-scale taxonomy enrichment beyond what is required to preserve the
  relative source path and stable ids.

## Alignment Expectations

At minimum:

- operators can copy nested source folders into `data/raw` without flattening;
- original filenames and folder hierarchy remain untouched in the source tree;
- generated artifact names and ids remain deterministic and collision-safe.

## Acceptance Criteria

- The ingestion CLI can ingest PDFs located under nested subdirectories of the
  input directory.
- The implementation no longer relies on `source_pdf_path.stem` alone as the
  unique document id.
- Two files with the same basename in different folders do not overwrite each
  other's markdown, processed metadata, or chunk artifacts.
- Tests cover recursive discovery and duplicate-basename scenarios.
