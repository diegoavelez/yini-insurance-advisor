# Requirements

## Title

Persist canonical document type metadata from source-relative paths when overlays are absent.

## Context

After persisting `product` from `source_pdf_relative_path`, the AUTOS comparative artifacts still expose `document_type=null`. The retrieval path now works, but storage-level metadata remains partially incomplete for path-encoded documents such as `clausulado`, `preguntas frecuentes`, `ayudaventas`, and `formato`.

The next narrow slice should persist inferred canonical `document_type` metadata during ingestion whenever operator overlays do not already provide it.

## Scope

This slice should:

1. Infer canonical `document_type` from source-relative path and filename tokens.
2. Preserve overlay precedence over inferred values.
3. Propagate the resolved document type into processed-document and chunk artifacts.

This slice should not:

- rewrite historical artifacts in bulk;
- infer unrelated metadata fields beyond `document_type`;
- change retrieval contracts.

## Required Behavior

### 1. Persisted document type inference

Acceptance criteria:

- ingestion persists `document_type=guide` for path/filename patterns like `ayudaventas` or `instructivo` when overlay metadata is absent;
- ingestion persists `document_type=faq` for patterns like `preguntas frecuentes`;
- ingestion persists `document_type=policy` for patterns like `clausulado`;
- chunk bundles and chunk records inherit the same resolved document type.

### 2. Overlay precedence

Acceptance criteria:

- operator-curated overlay values still win over inferred path values.

### 3. Backward compatibility

Acceptance criteria:

- existing overlay-driven metadata tests still pass;
- focused ingestion tests pass;
- roadmap records the slice.
