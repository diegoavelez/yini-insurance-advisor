# Requirements

## Title

Establish `.docx` exclusion as an explicit MVP policy.

## Context

The remaining `.docx` files in the PAC corpus are Word forms intended to be
filled manually outside the RAG flow. The MVP should not ingest them, cite
them, or return them in grounded answers.

Some current-source documentation still frames those `.docx` files as
"deferred" support. That wording implies future runtime handling inside the
current MVP boundary, which is no longer the intended product posture.

## Scope

This slice should:

1. make the MVP policy explicit that ingestion is PDF-only;
2. state that `.docx` forms are out of scope for ingestion and answer
   generation;
3. update current-source docs so `.docx` files are described as excluded, not
   deferred support.

This slice should not:

- add `.docx` parsing or conversion support;
- rewrite historical spec bundles that accurately describe earlier decisions;
- change retrieval, chunking, or answer runtime behavior.

## Required Behavior

### 1. MVP ingestion posture

Acceptance criteria:

- current-source docs state that ingestion is PDF-only;
- current-source docs state that `.docx` files are not onboarded into the RAG
  corpus.

### 2. Answer-surface posture

Acceptance criteria:

- current-source docs state that `.docx` forms are not returned as answer
  evidence or response artifacts.

### 3. Roadmap sync

Acceptance criteria:

- roadmap status lines no longer describe `.docx` files as deferred support;
- the current roadmap posture describes them as excluded from the MVP.
