# Requirements

## Title

Preserve governing section context inside chunk text for structurally fragmented PDFs.

## Context

Real inspection of `movilidad__autos__diferenciales-planes-autos` shows that the chunker often assigns a correct `section` and `section_path`, but the chunk text itself starts mid-section because overlap and block assembly resume after the heading.

This is especially harmful for PDFs diagrammed in boxes and loose labels, where many semantically meaningful terms live in headings rather than in the repeated body text.

The next narrow slice should ensure chunk text retains the governing section context when it would otherwise be missing.

## Scope

This slice should:

1. Detect when a chunk text is missing its governing section-path headings.
2. Prefix deterministic heading context into the chunk text.
3. Keep chunk metadata contracts unchanged.
4. Add focused regression coverage.

This slice should not:

- redesign the chunk contract;
- add probabilistic summarization;
- depend on product-specific document ids;
- redesign embedding or retrieval contracts.

## Required Behavior

### 1. Section-context preservation

Chunk text should include the governing section context derived from `section_path` when that context is not already present.

Acceptance criteria:

- chunk text keeps the original extracted content intact;
- missing governing headings are prefixed deterministically;
- existing headings are not duplicated when already present.

### 2. Dense structured documents

The behavior should help documents with tables, boxed content, and repeated short fragments.

Acceptance criteria:

- follow-on chunks from the same section can still contain the governing heading context;
- section metadata remains aligned with the prefixed headings.

### 3. Backward compatibility

Acceptance criteria:

- current chunking tests still pass unless intentionally updated;
- chunk ids and metadata fields remain stable for identical block ordering.
