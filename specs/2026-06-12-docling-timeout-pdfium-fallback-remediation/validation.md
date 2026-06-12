# Validation

## Status

- Planned on `2026-06-12`.

## Required Checks

- `backend="docling"` falls back to PDFium on per-document timeout.
- Non-timeout Docling failures still raise.

## Required Scenarios

- A simulated `subprocess.TimeoutExpired` in Docling returns PDFium markdown.
- A simulated non-timeout `RuntimeError` from Docling still fails explicitly.

## Merge Readiness

This slice is ready when a single slow Docling conversion no longer blocks the
local ingestion batch and the fallback policy remains narrow and testable.
