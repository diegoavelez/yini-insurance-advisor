# Changelog

## 2026-05-25

- Add the first `Phase 14` deployment slice with a root Docker runtime
  skeleton, explicit dependency installation from `pyproject.toml`, explicit
  Gradio bind/port runtime wiring, and the current app entrypoint without
  drifting into container smoke validation or hosted deployment work.

## 2026-05-22

- Add the corrective `Phase 13` demo-hardening slice that sanitizes explicit
  public trace summaries, preserves safe concise trace labels, redacts unsafe
  internal trace items, and falls back to the derived review-oriented trace
  when explicit trace data is not safe to show.
- Add the final `Phase 13` demo-hardening slice with a narrow `Answer Quality`
  surface, explicit degraded messaging for lower-confidence and limited-evidence
  drafts, and local validation that closes the remaining demo UI hardening work.

## 2026-05-21

- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  readiness surface, explicit degraded messaging for runtime/dependency
  readiness failures, and local validation without drifting into
  answer-quality degradation work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  error-state surface, explicit distinction between input-validation and
  runtime-processing failures, and local validation without drifting into
  degraded-service messaging work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  loading-state surface, explicit in-flight and ready feedback through the
  current Gradio UI handler, and local validation without drifting into
  error-state redesign or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow operator-facing
  debug-metadata surface, compact request/runtime/retrieval metadata tied to
  the current UI seams, and local validation without drifting into
  loading/error-state or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  support-context surface, concise request-follow-up guidance tied to the
  current request-correlation seams, and local validation without drifting
  into broader debug-metadata or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  trace-summary surface, concise review-oriented trace rendering across
  success/refusal UI paths, and local validation without drifting into broader
  debug-context or degraded-service messaging work.
- Add the first `Phase 13` demo-hardening slice with a grouped Gradio `Blocks`
  layout, clearer review-oriented output organization for answer/citations/
  confidence/limitations/status, and local validation without drifting into
  trace-summary or degraded-service messaging work.
- Add the corrective `Phase 12` MCP slice that closes the remaining
  compatibility-boundary gap by making request-field and MCP-visible
  tool-metadata compatibility expectations explicit, aligning the implemented
  MCP seam with the final phase requirements.
- Add the final `Phase 12` MCP slice with explicit tool-compatibility
  boundaries for the current MCP-visible surface, operational forward/backward
  compatibility expectations aligned to the interface version policy, and local
  validation that closes the remaining MCP integration work.
- Add the next `Phase 12` MCP slice with an explicit interface version policy,
  date-based version naming, operational bump rules for additive and breaking
  MCP-surface changes, and local validation without drifting into detailed
  compatibility-boundary work.
- Add the next `Phase 12` MCP slice with a narrow local client seam, end-to-end
  initialize/list/call roundtrip over the current registered MCP tool surface,
  and local validation without drifting into interface versioning work.
- Add the next `Phase 12` MCP slice with initial server-side tool
  registration and exposure for `document_retrieval` and `clause_extraction`,
  explicit MCP-visible tool metadata, and local validation without drifting
  into MCP client integration.
- Add the first `Phase 12` MCP slice with a minimal server seam, explicit
  typed transport request/response contracts, initialize/ping-only handling,
  and local validation without drifting into tool execution wiring.

## 2026-05-20

- Add the corrective `Phase 11` optimization slice that remediates
  query-classification measurable-improvement semantics by making the current
  optimization-subset evaluation surface explicit, reporting when improvement
  is not actually validated, and removing overstated optimization claims from
  the roadmap.
- Add the final corrective `Phase 11` optimization slice with hosted-like
  query-classification latency-budget validation over the product-facing
  classification path, explicit distinction from the local comparison seam, and
  local validation that truthfully closes the remaining `Phase 11` gap.
- Add the final `Phase 11` optimization slice with typed
  query-classification latency-budget validation, explicit within-budget /
  over-budget reporting over the current optimized predictor and latency
  comparison seam, and local validation that closes the remaining `Phase 11`
  work.
- Add the next `Phase 11` optimization slice with a typed
  query-classification quality-improvement validation seam, explicit improved /
  flat / regressed reporting over the current optimized predictor and baseline,
  and local validation without drifting into latency-budget validation.
- Add the next `Phase 11` optimization slice with a real optimized
  query-classification callable, subset-backed predictor wiring, compatibility
  with the existing quality/latency/cost comparison seams, and local
  validation without yet claiming measurable improvement.
- Add the final `Phase 11` optimization slice with a measurable
  query-classification cost-comparison seam, typed baseline-versus-optimized
  external-call and estimated-cost reporting over the current optimization
  subset, and local validation that closes the remaining `Phase 11` work.
- Add the next `Phase 11` optimization slice with a measurable
  query-classification latency-comparison seam, typed baseline-versus-optimized
  latency reporting over the current optimization subset, and local validation
  without drifting into cost comparison work.
- Add the next `Phase 11` optimization slice with a measurable
  query-classification quality-comparison seam, typed overall and per-category
  reporting, deterministic baseline-versus-optimized evaluation over the
  current optimization subset, and local validation without drifting into
  latency or cost comparison work.
- Add the next `Phase 11` optimization slice with a narrow query-classification
  optimization dataset subset, typed optimization-example contracts, explicit
  linkage to the 30-question evaluation and golden-behavior assets, and local
  validation without drifting into before/after comparison work.
- Add the next `Phase 11` optimization slice with a minimal DSPy
  query-classification module skeleton, explicit typed optimization I/O
  contracts, lazy DSPy runtime loading, and local validation without drifting
  into optimization dataset or before/after comparison work.
- Add the first `Phase 11` optimization slice by selecting `query
  classification` as the initial DSPy target, defining explicit baseline
  quality, latency, and zero-external-call cost surfaces, and documenting the
  decision without drifting into module implementation.
- Add the next `Phase 10` evaluation slice with a hosted-like latency smoke
  over the local evaluation runner, a deterministic latency assertion surface,
  and local validation without drifting into citation regression smoke work.
- Add the next `Phase 10` evaluation slice with hosted-like startup and
  health/readiness smoke coverage over the current app/runtime seams, keeping
  the checks deterministic and scoped away from latency and citation
  regressions.

## 2026-05-19

- Add the next `Phase 10` evaluation slice with a deterministic local
  evaluation runner over the curated assets, typed run-level and per-question
  outputs, stable `question_id` linkage, and local validation without drifting
  into hosted regression smoke work.
- Add the next `Phase 10` evaluation slice with typed local evaluation
  run-result contracts, deterministic per-question result linkage, and schema
  validation for run-level and per-question outputs without drifting into
  runner execution.
- Add the next `Phase 10` evaluation slice with a typed citation-expectation
  dataset for the curated 30-question set, deterministic question linkage,
  explicit distinction between grounded, no-citation, and guardrail citation
  cases, and local alignment validation without drifting into runner work.
- Add the next `Phase 10` evaluation slice with a typed retrieval-expectation
  dataset for the curated 30-question set, deterministic question linkage,
  explicit distinction between grounded, no-retrieval, and guardrail retrieval
  cases, and local alignment validation without drifting into citation
  expectations or runner work.
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
