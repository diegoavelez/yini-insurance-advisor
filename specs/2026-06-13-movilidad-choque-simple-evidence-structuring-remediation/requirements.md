# Requirements

## Title

Improve `choque simple` evidence structure for the shared mobility circular.

## Context

The previous `movilidad-choque-simple-supported-scope-and-retrieval` slice
successfully routes queries to the correct transversal corpus. Runtime
retrieval now lands in `circular choque simple.pdf`, but the evidence still
arrives with weak structural labels such as repeated `CIRCULAR EXTERNA`,
date-only fragments, and signature/footer boilerplate.

The next narrow slice should improve structure at ingestion time so retrieval
and grounded answers can cite more meaningful sections without changing the
retrieval contract.

## Scope

This slice should:

- remove narrow circular-specific boilerplate from chunk inputs;
- promote semantic labels such as `ASUNTO CHOQUE SIMPLE`,
  `ARTÍCULO 16 — DAÑOS MATERIALES`,
  `INFORME POLICIAL Y RECAUDO PROBATORIO`, and
  `INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE`;
- keep ordinary non-circular ingestion behavior unchanged.

This slice should not:

- redesign the whole chunking pipeline;
- introduce LLM summarization;
- create a broad legal-document parser;
- change retrieval, citation, or answer contracts.

## Acceptance Criteria

### 1. Boilerplate suppression

- Circular-specific footer/header boilerplate no longer becomes standalone
  evidence blocks.

### 2. Semantic section promotion

- Key `choque simple` circular blocks use stronger section labels than the
  repeated generic `CIRCULAR EXTERNA` heading.

### 3. Backward compatibility

- Focused ingestion tests pass.
- Existing comparison, deductible, and coverage normalization behavior remains
  unchanged.
