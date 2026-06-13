# Requirements

## Title

Normalize comparison-table text into semantically richer statements for fragmented AUTOS corpus retrieval.

## Context

The AUTOS comparative document still fails to enter the retrieval candidate pool after section-context prefixing and denser same-section aggregation. Inspection shows the remaining issue is representational: Docling extracts large comparison tables and boxed layouts into noisy row fragments that are hard for embeddings to align with natural comparison questions.

The next narrow slice should rewrite clearly structured comparison-table content into more semantic text while keeping deterministic local behavior and current contracts intact.

## Scope

This slice should:

1. Detect markdown table-like blocks with repeated plan labels.
2. Normalize those blocks into deterministic text statements.
3. Preserve the original information content as much as possible.
4. Feed the normalized text into the existing chunking pipeline.

This slice should not:

- redesign the processed-document contract;
- introduce LLM summarization;
- hardcode one source document id;
- change retrieval or embedding interfaces.

## Required Behavior

### 1. Table-like comparison normalization

When cleaned markdown contains a table-like block with repeated plan labels and comparable cells, the pipeline should emit semantically richer lines.

Acceptance criteria:

- plan names remain explicit in the normalized text;
- row/category labels remain explicit when present;
- normalization is deterministic and local;
- non-table paragraphs remain unchanged.

### 2. Comparison-oriented readability

The normalized text should better resemble the language of comparison queries.

Acceptance criteria:

- output can contain statements such as `<plan>: <attribute/value>`;
- repeated plan columns do not remain only as raw pipe-delimited rows when normalization succeeds;
- normalized text remains attributable to the same section path.

### 3. Backward compatibility

Acceptance criteria:

- ordinary markdown without comparison-table structure is not rewritten;
- focused regression tests pass;
- chunk and retrieval contracts remain unchanged.
