# Requirements

## Title

Persist canonical product metadata from source-relative paths when overlays are absent.

## Context

The AUTOS comparison corpus surfaced in retrieval only after a runtime fallback inferred `product=auto` from `source_pdf_relative_path`. That fixed recall, but the persisted processed-document and chunk artifacts still carry `product=null`, leaving an avoidable inconsistency between storage and runtime behavior.

The next narrow slice should persist inferred canonical product metadata during ingestion whenever operator overlays do not already provide it.

## Scope

This slice should:

1. Infer canonical `product` from `source_pdf_relative_path` during ingestion.
2. Preserve overlay precedence over inferred values.
3. Propagate the resolved product into processed-document and chunk artifacts.

This slice should not:

- rewrite historical artifacts in bulk;
- infer new document types from filenames;
- change retrieval contracts.

## Required Behavior

### 1. Persisted product inference

Acceptance criteria:

- ingestion persists `product=auto` for documents under paths like `MOVILIDAD/AUTOS/...` when overlay metadata is absent;
- chunk bundles and chunk records inherit the same resolved product.

### 2. Overlay precedence

Acceptance criteria:

- operator-curated overlay values still win over inferred path values.

### 3. Backward compatibility

Acceptance criteria:

- existing overlay-driven metadata tests still pass;
- focused ingestion tests pass;
- roadmap records the slice.
