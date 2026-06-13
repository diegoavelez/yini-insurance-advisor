# Requirements

## Title

Improve corpus retrievability for fragmented comparison documents through denser section-aware chunk aggregation.

## Context

The AUTOS comparative document is extracted from a PDF laid out in tables and loose boxed text. The current chunker preserves headings and section metadata, but still emits many short consecutive blocks under the same governing section.

Real retrieval validation shows that even after section-context prefixing and deterministic reranking, the comparative document remains absent from the candidate pool for comparison queries. This indicates the embedded chunk text is still too fragmented to compete with FAQ-style prose.

The next narrow slice should improve chunk density for such structured sections without redesigning the retrieval contract.

## Scope

This slice should:

1. Aggregate more than two consecutive short blocks under the same section path.
2. Preserve deterministic ordering and existing chunk metadata contracts.
3. Keep heading-aware behavior intact.
4. Remain general enough for similar structured PDFs, not hardcoded to AUTOS ids.

This slice should not:

- redesign the chunk contract;
- add LLM summarization;
- introduce product-specific chunking rules;
- redesign embedding or retrieval interfaces.

## Required Behavior

### 1. Dense section aggregation

The chunker should greedily aggregate consecutive short non-heading blocks that share the same section path when the combined size still fits the configured chunk size.

Acceptance criteria:

- aggregation can include more than one adjacent merge;
- headings still anchor their following content;
- aggregation remains deterministic.

### 2. Structured comparison documents

The behavior should help table-like and boxed documents where many semantic cues are split into short lines.

Acceptance criteria:

- related comparison cues like coverage labels, differentiators, and plan names can end up in the same grouped block;
- grouped block section metadata remains aligned with the governing section path.

### 3. Backward compatibility

Acceptance criteria:

- existing chunk ids remain deterministic for identical inputs under the new logic;
- focused chunking regression tests pass;
- unchanged documents do not require contract changes.
