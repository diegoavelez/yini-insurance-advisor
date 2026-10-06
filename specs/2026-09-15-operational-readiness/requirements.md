# Requirements — operational-readiness

## Work Unit

- identifier: `YINI-OPERATIONAL-READINESS-001`
- SDD depth: Level 1 operational-readiness preparation
- status: documentary candidate only; no provider, release, or production
  readiness is established

## Context

`docs/mvp-go-live.md` remains the published MVP operational baseline. It names
`make test-release`, hosted smoke, rollback, and the corpus-update posture.
This follow-on does not duplicate that baseline or add product scope. It records
the bounded evidence needed before a separately authorized operational check can
be considered.

The static inventory reviewed `Makefile`, `pyproject.toml`, `requirements.txt`,
`core/config.py`, `rag/runtime_providers.py`, `rag/pdf_conversion.py`,
`rag/qdrant_store.py`, `rag/ingestion.py`, and the test files named by
`make test-release`. That inspection is not execution and does not establish
provider health, a cached model, a populated corpus, or network isolation.

## Objective

Define an evidence-limited readiness preparation that identifies the local gate,
its declared dependencies and boundaries, and the only proposed external
protocol. Preserve a clear distinction between historical transport evidence,
local documentary evidence, and current external health.

## In Scope

- inventory the four `pytest` groups invoked by `make test-release` and their
  declared local executable path;
- identify declared runtime dependencies from `pyproject.toml` and the
  provider-facing seams reviewed statically;
- record each local gate group as `NOT_RUN` for this work unit, including the
  limit that network/provider/corpus isolation was not demonstrated by the
  earlier static inspection;
- define a separately authorized, fail-closed proposal for Qdrant contract
  metadata, Hugging Face load/readiness, and one benign application query;
- retain `docs/mvp-go-live.md` as a link, not a duplicated go-live procedure.

## Out of Scope

- running `pytest`, `make`, application code, validators that import the app,
  any provider or network request, or any corpus access;
- changing runtime code, dependencies, tests, CI, credentials, configuration,
  the hosted application, or the current corpus;
- Git staging, commit, push, remote readback, publication, acceptance, or
  independent review;
- asserting that the local gate is globally network-isolated or that a test
  does make a network call. Neither conclusion follows from this inspection.

## Acceptance Criteria

1. The candidate names the existing local gate, its four command groups, and
   its declared executable/dependency boundary without reporting an execution.
2. Every unexecuted local group is explicitly `NOT_RUN`; the absence of a
   demonstrated isolation proof is recorded as an evidence gap, not as a
   product failure.
3. The external proposal fixes an exact cap, public or synthetic data class,
   timeout, zero retries, budget treatment, and stop conditions for each stage.
4. The candidate distinguishes historical `PUBLISH-3` transport from current
   Git ownership and from provider health.
5. The candidate makes no readiness, cost, deployment, provider, or production
   claim beyond the documentary evidence it records.

## Authorized Level 1 Extension — Test Isolation (2026-10-06)

`YINI-READINESS-ISOLATION-IMPL-2` separately authorizes test-local implementation
and local validation. The documentary history above retains its original scope.
Tests must ignore the default real `.env` and inherited Settings fields before
collection and during execution, while explicit test environment overrides and
the cached-settings assertions keep their meaning. Production configuration
must remain unchanged. A subprocess regression uses only an invented `.env`
and invented inherited credentials in a temporary directory, observes intended
RED then GREEN, and checks collection and runtime defaults through `get_settings`.
The four exact `Makefile` test-release groups may run once only after their
imports, fixtures and provider/filesystem boundaries are inspected as safe.
No actual secrets, private corpus, model initialization, network, installation,
Git mutation, independent review or acceptance is included.

## Authorized Level 1 Extension — Corpus Separation (2026-10-06)

`YINI-READINESS-ISOLATION-IMPL-3` renews the local objective in a fresh task.
Collection and execution of local tests must not load real evaluation datasets
or processed chunks. Preserve all dataset/corpus assertions in an explicit
`--run-corpus-evaluation` route, with deferred reads and a registered
`corpus_evaluation` marker. A marker alone is insufficient if decorators read
the dataset during collection. This route remains `NOT_RUN` in this bundle.
Invented inline cases independently exercise normalization and expected filters.
A temporary-process regression blocks corpus/dotenv reads before collection
and proves local collection and execution succeed. Production configuration
and previous Settings isolation remain unchanged. Separating additional real
dataset tests through conftest/Makefile is allowed; their files and assertions
remain intact, and omissions must be explicit rather than counted as PASS.
