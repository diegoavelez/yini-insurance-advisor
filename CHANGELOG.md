# Changelog

## 2026-05-19

- Add the next `Phase 10` evaluation slice with a typed golden behavior
  dataset for the 30-question curated set, deterministic question-to-outcome
  linkage, explicit refusal and guardrail expectations, and local alignment
  validation without drifting into retrieval/citation evidence annotations or
  runner work.
- Add the next `Phase 10` evaluation slice by completing the curated local
  question set to the 30-question roadmap target, preserving stable ids,
  balanced category coverage, and deterministic schema validation without
  drifting into golden outputs or runner work.
- Add the next `Phase 10` evaluation slice by expanding the local curated
  question set from the initial seed to a broader balanced dataset with stable
  ids, explicit expected-behavior metadata, and schema validation coverage
  across normal QA and current guardrail categories.
- Add the first `Phase 10` evaluation slice with typed evaluation-question
  schemas, a versioned local curated question set covering normal QA and
  guardrail-oriented prompts, and deterministic dataset validation coverage.
- Add the final `Phase 9` guardrail slice with a narrow local summary surface
  for guardrail/refusal events, typed event records, distinguishable guardrail
  classes, and preserved request-correlation context without drifting into
  broader analytics work.
- Add the next `Phase 9` guardrail slice with deterministic abuse-case
  regression scenarios over implemented guardrails, explicit assertions of the
  expected refusal or downgrade outcomes, and benign supported control coverage
  without drifting into telemetry-summary work.
- Add the next `Phase 9` guardrail slice with deterministic prompt-injection
  signal detection, conservative typed refusal behavior at the workflow and UI
  boundary, and correlated guardrail observability without drifting into
  abuse-case-suite work.
- Add the next `Phase 9` guardrail slice with explicit confidence-consistency
  enforcement, conservative typed downgrade behavior for overstated confidence,
  and correlated guardrail observability without drifting into prompt-injection
  or abuse-case work.
- Add the next `Phase 9` guardrail slice with mandatory citation presence for
  answerable responses, conservative typed downgrade behavior when citations
  are missing, and correlated guardrail observability without drifting into
  broader confidence-policy work.
- Add the first `Phase 9` guardrail slice with deterministic unsupported-query
  scope classification, conservative typed refusal outcomes at the workflow and
  UI boundary, and correlated refusal observability without drifting into
  prompt-injection or citation-confidence policy work.
- Close the remaining `Phase 8` validation gap with an end-to-end
  unsupported-route workflow test, confirming conservative non-error behavior
  for out-of-scope queries and fully closing the documented planner slice
  verification.
- Add the next `Phase 8` workflow slice with explicit insufficient-evidence
  fallback edges after comparison and citation verification, conservative
  typed fallback outcomes, fallback traceability in shared state, and
  observability for fallback selection events.
- Add the next `Phase 7` tooling slice with an independently callable
  `citation_verifier_tool`, conservative verification over drafted output and
  cited evidence only, explicit weak/unsupported non-error outcomes, and typed
  success/failure observability coverage.
- Add the final `Phase 7` tooling slice with an independently callable
  `response_draft_tool`, typed advisor-facing draft output from upstream
  evidence only, explicit insufficient-information handling, and preserved
  observability for reusable drafting.
- Add the first `Phase 8` workflow slice with LangGraph wiring, shared workflow
  state, one linear end-to-end tool path, typed workflow success/failure
  output, and observable state transition tracing.
- Add the next `Phase 8` workflow slice with a typed planner step, explicit
  route selection over existing workflow paths, conservative unsupported-route
  handling, and observable planner decision events.
- Add the next `Phase 8` workflow slice with explicit analyst, verifier, and
  drafter stages, clearer stage outputs in shared workflow state, and tighter
  graph-stage boundaries over the existing tool seams.

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
- Add the first `Phase 7` tooling slice with an independently callable
  `document_retrieval_tool`, typed tool failure contracts, empty-result
  success handling, preserved request correlation, and explicit tool failure
  observability coverage.
- Add the next `Phase 7` tooling slice with an independently callable
  `clause_extraction_tool`, conservative typed clause categorization over
  retrieved evidence only, traceable supporting chunk ids, and explicit
  success/failure observability coverage.
- Add the next `Phase 7` tooling slice with an independently callable
  `policy_comparison_tool`, conservative structured comparison points over
  typed evidence only, explicit insufficient-information handling, and typed
  success/failure observability coverage.

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
