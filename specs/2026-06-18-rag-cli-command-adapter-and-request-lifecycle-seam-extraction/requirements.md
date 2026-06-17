# Requirements

## Title

Extract CLI command adapters and request lifecycle orchestration from
`rag/ingestion.py`.

## Context

The current MVP already has a working Gradio surface and the accepted category
set is now protected by deterministic acceptance smokes. The remaining issue is
backend coupling in the CLI entrypoint:

- `rag/ingestion.py` still duplicates `RetrievalQuery` construction across
  retrieval and grounded-answer commands;
- top-level request lifecycle logging and command dispatch still live in the
  same module as lower-level ingestion, retrieval, and answer orchestration;
- warmup, retrieval, and answer commands still depend on direct entrypoint glue
  instead of a narrow adapter seam.

This is not a user-visible feature gap, but it is a stability gap for the MVP
backend while more corpus categories and corrective slices continue.

## Scope

This slice should:

1. extract a dedicated seam for shared CLI request lifecycle orchestration;
2. extract simple command adapters for Docling warmup, embedding warmup,
   retrieval, and grounded answering;
3. centralize `RetrievalQuery` construction from CLI args in one place;
4. keep parser definitions and lower-level runtime/retrieval helpers in
   `rag/ingestion.py`.

This slice should not:

- change command names, flags, or CLI output format;
- redesign ingestion, retrieval, or grounded-answer logic;
- change the Gradio UI contract;
- introduce new runtime dependencies.

## Required Behavior

### 1. Shared retrieval-query builder

Acceptance criteria:

- one shared helper builds `RetrievalQuery` from CLI args;
- retrieval and grounded-answer commands both use that helper;
- default `top_k` behavior remains unchanged.

### 2. Thin command adapters

Acceptance criteria:

- Docling warmup remains behaviorally identical through a thin adapter seam;
- embedding warmup remains behaviorally identical through a thin adapter seam;
- retrieval and grounded-answer command runners become thin wrappers over the
  shared query builder plus injected business functions.

### 3. Request lifecycle seam

Acceptance criteria:

- CLI request startup logging, request-id generation, command dispatch,
  success logging, and failure logging are extracted behind one dedicated seam;
- request-aware command invocation remains supported;
- `rag/ingestion.py` keeps the parser definitions and exposes the same
  top-level `main(...)` entrypoint.

### 4. Regression coverage

Acceptance criteria:

- focused tests validate shared query construction;
- focused tests validate request-id fallback behavior;
- focused tests validate success and non-zero failure lifecycle logging through
  the extracted seam.

### 5. Roadmap sync

Acceptance criteria:

- the roadmap records this refactor candidate as closed;
- the roadmap states that parser definitions and lower-level helpers remain in
  `rag/ingestion.py` intentionally after this extraction.
