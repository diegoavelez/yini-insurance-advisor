# Validation

## Status

- Planned on `2026-06-09`.
- Completed on `2026-06-09`.

## Required Checks

- Review `README.md`, `rag/ingestion.py`, and the typed contracts that carry
  document metadata.
- Confirm the roadmap and this dated spec remain documentation-only in this
  slice.

## Required Scenarios

- The current metadata contract is explicit and reviewable.
- The current limitations are documented without implying unimplemented
  enrichment behavior.
- The slice remains narrowly scoped to baseline contract definition.

## Merge Readiness

This spec is ready when the repository has a clear, dated baseline for
document metadata and corpus identity assumptions, enabling the next
implementation slice to be narrow and evidence-based.

## Evidence

- Reviewed the current metadata-bearing contracts in `contracts/documents.py`
  and `contracts/embeddings.py`.
- Reviewed the current ingestion metadata seams in `rag/ingestion.py`.
- Updated the top-level metadata baseline notes in `README.md`.
- Confirmed the diff remains documentation-only for this slice.

## Recorded Outcome

- The repository now has an explicit baseline for `source_pdf_id`,
  `source_pdf_relative_path`, retrieval-facing `document_name`, and optional
  `document_version`.
- The previous `README.md` statement that `document_name` mirrors
  `source_pdf_id` and `document_version` is always unset was corrected to match
  current implemented behavior.
- No ingestion, retrieval, embedding, or indexing behavior changed in this
  slice.
