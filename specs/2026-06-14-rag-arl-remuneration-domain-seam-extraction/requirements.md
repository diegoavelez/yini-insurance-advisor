# Requirements

## Slice

`rag-arl-remuneration-domain-seam-extraction`

## Goal

Extract the ARL remuneration-policy retrieval and evidence-selection domain out
of `rag/ingestion.py` into a dedicated `rag` seam without changing current
runtime behavior.

## Context

`rag/ingestion.py` has grown beyond 6k lines and now contains a stable,
self-contained ARL remuneration-policy cluster covering:

- intent detection for broad/table/overview remuneration queries;
- chunk-family recognition for the remuneration policy document;
- deterministic ranking and duplicate resolution for ARL remuneration chunks;
- broad-answer citation compaction for direct remuneration support chunks.

That logic has already been corrected and validated live, so the next narrow
step is code-surface reduction rather than another retrieval behavior change.

## Requirements

1. The ARL remuneration-policy constants and helper functions must move to a
   dedicated module under `rag/`.
2. `rag/ingestion.py` must import and use that module instead of keeping the
   domain logic inline.
3. Retrieval behavior must remain unchanged for:
   - broad remuneration queries;
   - explicit table/percentage remuneration queries;
   - broad-answer citation compaction for remuneration overview prompts.
4. Existing tests and live CLI validation for the current ARL remuneration flow
   must continue to pass.

## Non-Goals

- changing query semantics or ranking policy;
- changing contracts, UI, or response wording;
- extracting other `rag/ingestion.py` domains in this slice.
