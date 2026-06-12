# Requirements

## Title

Formalize an external local batch runtime flow for ingestion and embeddings.

## Context

The current repository-local `.venv` remains a poor fit for heavy local batch
operations on this machine. Recent validation showed that:

- the repo-local `.venv` stalls on heavyweight imports such as `torch`;
- a clean virtualenv outside the synced workspace restores practical
  performance for `Docling` warm-up, `ingest-pdfs`, and `generate-embeddings`;
- the current repository lacks a narrow operator-facing surface that makes this
  validated external-runtime workflow easy to repeat.

The next slice should formalize that workflow without redesigning the app
runtime, container flow, or deployment contract.

## Scope

This slice should:

1. Add a minimal operator-facing batch-runtime surface to the repository.
2. Keep the runtime path configurable rather than hardcoding a single
   machine-specific location.
3. Preserve the existing app runtime flow for `make app` and `.venv`.
4. Reuse the current ingestion CLI rather than introducing a parallel wrapper
   program.

This slice should not:

- move the application runtime away from `.venv`;
- require the batch runtime to live inside the repository;
- redesign the ingestion contracts;
- redesign Qdrant or Groq configuration;
- commit generated corpus artifacts.

## Required Behavior

### 1. Configurable external batch runtime

The repository should expose a clearly named configurable path for the external
batch virtualenv, suitable for local operator use.

Acceptance criteria:

- the default app/runtime variables remain unchanged for existing `make setup`,
  `make test`, and `make app` flows;
- batch-oriented targets use a separate configurable runtime path;
- the operator can override the batch runtime path without editing source code.

### 2. Minimal batch operator commands

The repository should expose minimal repeatable commands for:

- warming up Docling assets;
- ingesting PDFs;
- generating embeddings;
- indexing embeddings.

Acceptance criteria:

- the commands are discoverable in a single repo-native place;
- each command maps directly to existing `python -m rag.ingestion ...`
  subcommands;
- the commands support overriding the input/output locations needed for safe
  local testing.

### 3. Operator documentation

The repository should document when to use the external batch runtime and why.

Acceptance criteria:

- the docs explain that the external runtime is for local batch operations,
  not for the app or deployment runtime;
- the docs explain that heavy artifacts should remain local and uncommitted;
- the docs show one practical example using temporary output directories.

## Non-Goals

- introducing Docker as the default local ingestion path;
- adding automatic external-venv creation logic beyond a simple setup target;
- changing the public deployment path;
- introducing new environment validation for local-only helper paths.
