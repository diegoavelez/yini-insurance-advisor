# Changelog

## 2026-05-18

- Implement the `docling-ingestion-skeleton` Phase 2 slice with an admin-only
  CLI entrypoint, deterministic output paths, append-only manifest logging, and
  typed processed-document contracts.
- Add Docling as a project dependency and rebuild the repo’s local `.venv` on
  Python `3.11` to align the actual environment with the documented tech stack.
- Update `README.md` to reflect completed `Phase 0`, completed `Phase 1`, and
  the first implemented `Phase 2` ingestion slice.
- Tighten spec alignment with explicit CLI usage docs and added tests for
  append-only manifest reruns and invalid ingestion status values.
- Add the `markdown-cleaning-and-metadata-extraction` Phase 2 slice with
  conservative Markdown cleaning, deterministic cleaned artifacts, minimal
  metadata extraction, and failure handling for post-conversion processing.
- Add the first `Phase 3` slice for deterministic chunk contracts and local
  chunk persistence, including explicit chunk configuration, stable chunk ids,
  propagated traceability metadata, and persisted per-document chunk bundles.
- Add the `semantic-boundary-aware-chunk-refinement` Phase 3 slice with
  heading-aware and clause-safe chunk boundaries, explicit `v2` chunk schema
  versioning, richer `section_path` metadata, and failure-path validation for
  refined chunk generation.
- Add the first `Phase 4` slice for local embedding generation, including
  typed embedding artifacts, config-driven `sentence-transformers` usage,
  canonical local persistence under `data/processed/embeddings`, and explicit
  failed-manifest behavior for malformed chunk artifacts.
- Add the second `Phase 4` slice for Qdrant indexing, including collection
  bootstrap and compatibility checks, deterministic point mapping from local
  embedding artifacts, idempotent upserts, retry/backoff behavior, and explicit
  indexing manifest coverage for permanent failures and multi-artifact
  continuation.
- Add the first `Phase 5` slice for retrieval, including query embedding reuse,
  Qdrant search, typed `RetrievedChunk` mapping, preserved traceability
  metadata from indexed payloads, explicit empty-result behavior, and retrieval
  failure coverage for malformed payloads.
- Add the second `Phase 5` slice for grounded answer generation, including
  deterministic prompt construction from retrieved evidence, Groq-backed draft
  answers, citation mapping with stable `chunk_id` traceability, and explicit
  low-confidence handling for empty or weak retrieval evidence.
- Add the remaining `Phase 5` MVP UI slice with a thin Gradio app over the
  grounded QA backend, explicit user-visible insufficiency and runtime error
  states, startup/request smoke coverage, and local usage documentation.
- Add the first `Phase 6` observability slice with startup diagnostics,
  request correlation ids, structured retrieval and grounded-answer execution
  events, correlated CLI/UI failure logging, and validation that execution
  events do not leak secrets.
- Add the remaining `Phase 6` observability slice with health/readiness checks,
  optional Phoenix activation, explicit Phoenix failure policy, startup smoke
  visibility for hosted app readiness, and correlated latency traces for the
  grounded QA path.

## 2026-05-17

- `chore: phase 0 foundation scaffold`
- `docs: add settings env validation spec`
- `docs: align roadmap with deployment posture`
- `feat: implement settings env validation`
- `docs: add changelog maintenance skill`
- `merge: settings-env-validation into main`
- Add the `shared-contracts-foundation` Phase 1 spec slice for retrieval, response, tool, and workflow-state contracts.
- Add typed shared contract models for documents, tools, responses, and agent state aligned with the PRD vocabulary.
- Expand contract validation coverage for typed filters, clause categories, comparisons, citations, wrapper results, and workflow state construction.
- Add deployment mode flags to the typed settings contract to close the last identified Phase 1 gap.
- Add the `deployment-mode-flags` spec slice and document allowed `APP_ENV` behavior for public MVP demo vs internal production.
- Add the `docling-ingestion-skeleton` Phase 2 kickoff spec with a CLI-first ingestion contract, deterministic storage rules, rerun policy, and processed-document contract expectations.
- Tighten roadmap and existing specs with credential activation timing, contract stability expectations, and a clearer MVP boundary.
