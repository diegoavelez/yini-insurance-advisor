# Yini

Yini is an internal assistant designed to help senior insurance advisors
retrieve, analyze, compare, and summarize information from official Sura
insurance policy and procedure documents.

This repository now contains the completed `Phase 0` foundation, the full
`Phase 1` configuration and shared-contract slices, and the first narrow
implementation slice of `Phase 2` for Docling-based PDF ingestion.

## Source Documents

- `PRD.md` is the product requirements source of truth.
- `constitution.md` is the constitution entry point.
- `specs/` contains the split constitution documents and future implementation
  specs.

## Current Status

- `Phase 0` foundation is complete.
- `Phase 1` is complete through settings validation, deployment mode flags, and
  shared typed contracts.
- The first narrow `Phase 2` slice is implemented:
  - admin-only Docling ingestion CLI
  - deterministic raw/markdown/processed storage conventions
  - typed processed-document contracts
  - manifest-based ingestion reporting
- The app UI remains a placeholder entry point while ingestion and retrieval are
  built incrementally.

## Local Setup

Use a local virtual environment for all development.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
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

## Repository Layout

```text
app/        Placeholder application entry point
agents/     Future LangGraph agents
contracts/  Shared typed contracts and ingestion metadata
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

The next implementation work continues `Phase 2` from `specs/roadmap.md`:
clean Markdown normalization, metadata extraction, and the remaining PDF
processing pipeline slices after the `docling-ingestion-skeleton` foundation.
