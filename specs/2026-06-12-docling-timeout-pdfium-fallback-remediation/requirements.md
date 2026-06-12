# Requirements

## Title

Allow per-document PDFium fallback when Docling exceeds the local conversion
timeout.

## Context

The local AUTOS ingestion run showed that `diferenciales planes autos.pdf`
hangs under Docling long enough to block the entire batch, even though the
rest of the AUTOS corpus converts successfully. The repository already uses
PDFium as a fallback for `backend="auto"`, but the current `backend="docling"`
operator path still aborts the document on timeout instead of falling back.

The next corrective slice should keep Docling as the first choice while
preventing one slow PDF from blocking the whole local ingestion loop.

## Scope

This slice should:

1. Fallback to PDFium when Docling times out for one document.
2. Keep that fallback limited to timeout cases.
3. Add focused regression coverage for both timeout fallback and non-timeout
   failures.

This slice should not:

- demote Docling from the default local backend;
- broaden fallback to every Docling parsing/runtime error;
- redesign operator CLI flags;
- change chunking, embeddings, or indexing behavior.

## Required Behavior

### 1. Timeout fallback

When the selected backend is `docling` and a per-document Docling conversion
exceeds the configured timeout, ingestion should use PDFium for that document
if PDFium is available.

Acceptance criteria:

- timeout-triggered Docling failures no longer block the document when PDFium
  is available;
- the function returns non-empty markdown from PDFium in that case.

### 2. Narrow failure policy

The fallback should remain limited to timeout behavior.

Acceptance criteria:

- non-timeout Docling failures still raise an explicit runtime error;
- the change does not silently swallow unrelated conversion defects.

### 3. Regression coverage

The repository should cover both the positive and negative paths.

Acceptance criteria:

- tests verify PDFium fallback for `backend="docling"` on timeout;
- tests verify non-timeout Docling errors still fail.
