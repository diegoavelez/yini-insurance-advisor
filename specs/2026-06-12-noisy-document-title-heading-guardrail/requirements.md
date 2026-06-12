# Requirements

## Title

Guard retrieval-facing document titles against noisy media-style headings.

## Context

`Phase 18 — Corpus Metadata and Retrieval Traceability` currently promotes the
first non-empty Markdown heading into `document_name`. A live ARL FAQ retrieval
showed a failure mode where a media/embed heading such as
`Grabación: https://...` becomes the retrieval-facing document label, even
though the deterministic filename stem is more truthful and more useful.

The next corrective slice should block obviously noisy heading candidates
without redesigning the broader document metadata contract.

## Scope

This slice should:

1. Add a narrow heading guardrail for `document_name` promotion.
2. Fall back to the deterministic source filename stem when the heading is
   rejected.
3. Add focused coverage for the noisy-heading case.

This slice should not:

- introduce title-casing or humanization of filename stems;
- scan the full document for a better semantic title;
- change `document_version` extraction behavior;
- redesign chunking or retrieval contracts.

## Required Behavior

### 1. Noisy heading rejection

The metadata extractor should reject heading candidates that are obviously
media/embed labels rather than document titles.

Acceptance criteria:

- headings with URL payloads are not promoted to `document_name`;
- media-style prefixes such as `Grabación:` are not promoted to
  `document_name`;
- the behavior remains deterministic and local to metadata extraction.

### 2. Deterministic fallback

Rejected headings should fall back to the current deterministic baseline.

Acceptance criteria:

- the extractor falls back to `source_pdf_path.stem`;
- unaffected safe headings still become `document_name`.

### 3. Regression coverage

The repository should cover both the safe and rejected heading paths.

Acceptance criteria:

- existing safe-heading coverage remains valid;
- a focused test verifies rejection of a noisy ARL-style FAQ heading.
