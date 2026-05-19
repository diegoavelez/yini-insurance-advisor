# Yini

Yini is an internal assistant designed to help senior insurance advisors
retrieve, analyze, compare, and summarize information from official Sura
insurance policy and procedure documents.

This repository now contains the completed `Phase 0` foundation, the full
`Phase 1` configuration and shared-contract slices, the implemented `Phase 2`
and `Phase 3` ingestion/chunking pipeline, the full `Phase 4` embedding and
indexing pipeline, and the core `Phase 5` grounded QA backend.

## Source Documents

- `PRD.md` is the product requirements source of truth.
- `constitution.md` is the constitution entry point.
- `specs/` contains the split constitution documents and future implementation
  specs.

## Current Status

- `Phase 0` and `Phase 1` are complete.
- `Phase 2` is complete through:
  - Docling-based offline ingestion
  - deterministic raw/markdown/processed storage conventions
  - conservative Markdown cleaning and minimal metadata extraction
- `Phase 3` is complete through:
  - deterministic chunk persistence
  - semantic boundary-aware chunk refinement
- `Phase 4` is complete through:
  - local embedding generation artifacts
  - Qdrant collection bootstrap and idempotent indexing
- `Phase 5` is complete through:
  - ranked retrieval
  - Gradio MVP query UI
  - grounded answer generation with citations
- The next major work starts `Phase 6` observability.

## Local Setup

Use a local virtual environment for all development.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

If `python3.11` is not on your shell path, use any Python 3.11+ executable
instead. The project does not support Python 3.10.

## Common Commands

```bash
make setup
make lint
make test
make app
```

## Gradio MVP UI

The current app entrypoint is a thin Gradio layer over the grounded QA backend.

Canonical command:

```bash
python -m app.ui
```

The UI exposes:

- advisor question input
- suggested grounded answer
- citations
- confidence
- limitations
- status / advisor-review messaging

User-visible failure behavior:

- blank input returns an explicit prompt to enter a question
- insufficient evidence remains a typed low-confidence response
- retrieval or generation failures surface as explicit UI errors

## Ingestion CLI

The first implemented `Phase 2` slice is an admin-only offline ingestion job.

Canonical command:

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

Required flags:

- `--input-dir`
- `--markdown-dir`
- `--processed-dir`
- `--manifest-path`

Optional flags:

- `--glob` defaults to `*.pdf`
- `--overwrite` defaults to `false`
- `--fail-fast` defaults to `false`

The command exits non-zero when:

- Docling is not importable in the local runtime
- the input directory does not exist
- no matching PDF files are found
- a conversion fails while `--fail-fast=true`

Current metadata behavior for this slice:

- `document_name` currently mirrors `source_pdf_id`
- `document_version` is intentionally left unset
- this slice records metadata fields and deterministic artifact paths, but does
  not yet implement richer metadata extraction or Markdown cleaning

## Repository Layout

```text
app/        Gradio MVP application entry point
agents/     Future LangGraph agents
contracts/  Shared typed contracts across ingestion, retrieval, and answers
core/       Settings and logging bootstrap
data/       Raw, markdown, processed, and eval data
deploy/     Container and startup files
docs/       Supporting durable documentation
mcp/        Future MCP server/client modules
ops/        Guardrails and observability modules
rag/        Ingestion and future retrieval pipeline
specs/      Constitution and implementation specs
tests/      Smoke tests and future test coverage
```

## Next Milestones

The next implementation work moves into `Phase 6` observability from
`/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/specs/roadmap.md`.
