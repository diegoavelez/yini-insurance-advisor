# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 2 — PDF Processing Pipeline`.

The goal is to build the first deterministic post-conversion processing step
after `docling-ingestion-skeleton`:

- clean Docling Markdown into a stable retrieval-ready intermediate form;
- extract minimal document metadata without speculative heuristics;
- persist cleaned artifacts alongside the existing ingestion outputs;
- preserve traceability from source PDF to cleaned Markdown and metadata.

This slice does **not** start semantic chunking yet.

## In Scope

- Define the first Markdown cleaning contract for Docling output.
- Define the cleaned artifact layout and naming rules.
- Define the minimal metadata extraction contract for this stage.
- Define how cleaned outputs relate to existing ingestion metadata.
- Define explicit failure behavior for partial or invalid extraction outcomes.

## Out of Scope

- Semantic chunking.
- Embeddings generation.
- Qdrant indexing.
- Retrieval logic.
- UI ingestion triggers.
- Advanced policy-semantic parsing.
- Version inference heuristics beyond obvious extracted text fields.

## Execution Model

This slice should remain an admin-only offline CLI workflow.

The processing step should extend the existing ingestion pipeline rather than
introducing an app route or interactive UI path.

### CLI Contract

The existing ingestion command remains the canonical entrypoint for this stage:

```bash
python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "*.pdf" \
  --overwrite false \
  --fail-fast false
```

This slice should define how the command now performs two deterministic stages:

1. PDF to raw Markdown conversion through Docling.
2. Raw Markdown to cleaned processed artifact generation.

The CLI should still exit non-zero when:

- Docling is unavailable;
- the input directory is missing;
- no matching PDF files are found;
- a conversion or cleaning step fails while `--fail-fast=true`.

## Artifact Layout

The storage contract from the previous slice remains in force:

- `data/raw/` for source PDFs
- `data/markdown/` for raw Docling Markdown output
- `data/processed/` for cleaned Markdown and processed metadata artifacts

### Naming and Path Rules

- `source_pdf_id` remains derived from the PDF filename stem.
- Raw Markdown output remains `data/markdown/<source_pdf_id>.md`.
- Processed metadata remains `data/processed/<source_pdf_id>.json`.
- This slice adds cleaned Markdown output at
  `data/processed/<source_pdf_id>.cleaned.md`.
- Manifest output remains append-only JSONL at the configured manifest path.

This slice must keep all paths deterministic from the source PDF id and CLI
inputs.

## Markdown Cleaning Contract

The first cleaning pass should be intentionally conservative.

Allowed transformations:

- normalize line endings;
- trim trailing whitespace;
- collapse excessive blank lines;
- remove obviously empty boilerplate lines created by conversion;
- preserve section ordering and meaningful headings;
- preserve clause text without paraphrasing or semantic rewriting.

Disallowed transformations:

- summarization;
- semantic rewriting;
- clause merging based on interpretation;
- policy-specific heuristic classification;
- hallucinated headings or metadata.

The cleaning logic should favor preserving retrieval evidence over producing
beautiful prose.

## Metadata Extraction Contract

This slice should extract only minimal metadata that is directly available from
deterministic sources such as:

- `source_pdf_id`
- source filename
- cleaned artifact paths
- raw Markdown presence
- cleaned Markdown presence

Optional extracted text metadata may include:

- `document_name`
- `document_version`

but only when obtained through explicit, low-risk rules defined in code.

If reliable extraction is not available, the fields should remain:

- `document_name = source_pdf_id`
- `document_version = null`

This slice should not invent domain-specific version parsing heuristics.

## Processed-Document Contract Changes

The processed-document contract should now preserve:

- source PDF identity
- source PDF path
- raw Markdown output path
- cleaned Markdown output path
- processed metadata path
- document name
- document version
- ingestion status
- error message
- ingested timestamp

If the current contract needs to expand, it should do so through explicit typed
fields rather than ad hoc dictionaries.

## Failure Behavior

If raw Markdown conversion succeeds but cleaning fails:

- the manifest must still record a failed attempt;
- the failure must include an explicit error message;
- partial cleaned artifacts should not be treated as successful outputs.

If metadata extraction is incomplete but cleaning succeeds:

- the run may still succeed;
- missing optional metadata must be represented explicitly as fallback values or
  `null`;
- the implementation must not fail solely because richer metadata is absent.

## Reproducibility Rules

This slice must preserve reproducibility:

- same input PDFs and flags produce the same artifact paths;
- cleaning behavior must be deterministic;
- metadata fallbacks must be deterministic;
- processed outputs must remain traceable to raw Markdown and source PDFs.

## Acceptance Criteria

- The existing ingestion CLI remains the only execution path for this stage.
- Cleaned Markdown output is defined and stored deterministically.
- The cleaning contract is conservative and evidence-preserving.
- Minimal metadata extraction behavior is explicit.
- Missing optional metadata is handled without speculative heuristics.
- Failure behavior is explicit for raw conversion failures and cleaning failures.
- The slice clearly stops before semantic chunking.
