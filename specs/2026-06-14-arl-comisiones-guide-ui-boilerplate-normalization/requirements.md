# Requirements

## Title

Remove UI-surface boilerplate from the `ARL` commissions guide chunk.

## Context

The `ARL` corpus is already live and retrievable, and the RUI FAQ precision
slice is closed. The next narrow quality gap is now localized to one guide:

- `ARL/instructivos consulta de comisiones arl sura v2.pdf`

Its single guide chunk still preserves OCR/UI leftovers such as:

- `C a p a c i d a d : A R L`
- `[ C a p a c i d a d - A R L ]`
- standalone `sura`
- standalone `sura sura`

These lines are not procedural evidence. They weaken retrieval readability and
pollute answer citations even though the document family and operational path
already work.

## Scope

This slice should:

1. add narrow document-specific cleanup for the ARL commissions guide;
2. remove only clearly non-procedural UI leftovers from the cleaned markdown;
3. preserve the actual step-by-step guidance and existing document metadata;
4. validate the refreshed guide through rebuilt artifacts and live retrieval.

This slice should not:

- redesign ARL retrieval ranking globally;
- split the guide into a multi-step workflow model;
- alter unrelated ARL guides or policies;
- broaden into a generic OCR cleanup framework.

## Required Behavior

### 1. Boilerplate suppression

Acceptance criteria:

- the cleaned markdown no longer contains the `Capacidad ARL` UI labels;
- standalone `sura` and `sura sura` OCR leftovers are removed;
- the procedural bullet list remains intact.

### 2. Chunk readability recovery

Acceptance criteria:

- rebuilding the guide chunk bundle yields one cleaner guide chunk;
- the chunk still references the same guide document family and procedure.

### 3. Live retrieval validation

Acceptance criteria:

- a representative ARL commissions guide retrieval query still returns this
  guide first;
- the returned chunk surface is cleaner and no longer starts with UI
  boilerplate before the procedural steps.
