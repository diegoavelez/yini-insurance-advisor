# Requirements

## Title

Prioritize the SOAT coverage summary section over lateral policy chunks.

## Context

After aligning SOAT coverage intent to `document_type=policy`, runtime
validation improved materially, but the top retrieved evidence still tended to
surface lateral `policy` chunks such as transport or claims details before the
summary section `SECCIÓN I ¿Qué cubre este seguro?`.

The goal of this slice is not to redesign retrieval. It is to make the existing
deterministic reranking recognize when a curated expansion term exactly matches
the retrieved section heading and prioritize that evidence accordingly.

## Scope

This slice should:

1. strengthen reranking when a curated appended term exactly matches
   `section` or a `section_path` label;
2. keep existing label/body matching behavior intact for other slices;
3. add a focused regression test for SOAT coverage prioritization;
4. record the slice in the roadmap.

This slice should not:

- change query filters or retrieval contracts;
- introduce new ingestion behavior;
- implement generic semantic rescoring.

## Required Behavior

### 1. Exact section matches outrank lateral chunks

Acceptance criteria:

- for SOAT coverage intent, a chunk whose `section` exactly matches
  `SECCIÓN I ¿Qué cubre este seguro?` can outrank a higher-base-score lateral
  chunk when the curated rule explicitly targets that heading.

### 2. Backward compatibility

Acceptance criteria:

- existing retrieval tests continue to pass;
- the reranking change remains deterministic and local.
