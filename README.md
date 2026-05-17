# Yini

Yini is an internal assistant designed to help senior insurance advisors
retrieve, analyze, compare, and summarize information from official Sura
insurance policy and procedure documents.

This repository currently contains the Phase 0 foundation described in
`PRD.md`: constitution docs, project structure, local tooling, configuration
bootstrap, logging bootstrap, tests, and deployment skeletons.

## Source Documents

- `PRD.md` is the product requirements source of truth.
- `constitution.md` is the constitution entry point.
- `specs/` contains the split constitution documents and future implementation
  specs.

## Current Status

- Phase 0 repository foundation is scaffolded.
- Product logic is not implemented yet.
- The app entry point is a placeholder that validates configuration and logging.

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
contracts/  Shared typed contracts
core/       Settings and logging bootstrap
data/       Raw, markdown, processed, and eval data
deploy/     Container and startup files
docs/       Supporting durable documentation
mcp/        Future MCP server/client modules
ops/        Guardrails and observability modules
rag/        Future ingestion and retrieval pipeline
specs/      Constitution and implementation specs
tests/      Smoke tests and future test coverage
```

## Next Milestones

The next implementation milestone is Phase 1 from `specs/roadmap.md`:
typed configuration and shared contracts.
