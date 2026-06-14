# Roadmap

## Philosophy

The roadmap is intentionally split into very small implementation phases.

Each phase should:

- produce a working artifact;
- reduce ambiguity;
- be independently testable;
- include operational acceptance criteria for startup, configuration, and
  failure behavior;
- avoid large refactors.

Do NOT skip phases.
Do NOT build multiple major systems simultaneously.

The project should evolve incrementally.

---

# Phase 0 — Repository Foundation

## Goal

Create a stable engineering foundation before writing AI logic.

## Deliverables

- repository structure;
- AGENTS.md;
- governance docs;
- pyproject.toml;
- Ruff configuration;
- Pytest configuration;
- `.env.example`;
- logging setup;
- Makefile;
- Docker skeleton;
- README skeleton.
- basic environment mapping;
- initial health and startup strategy.

## Success Criteria

- repository runs locally;
- linting works;
- tests execute;
- Docker builds successfully;
- environment expectations are documented;
- container startup behavior is defined.

---

# Phase 1 — Configuration and Contracts

## Goal

Create typed configuration and shared contracts.

## Deliverables

- Pydantic settings;
- environment validation;
- deployment mode flags;
- startup validation seam;
- shared schemas;
- retrieval contracts;
- tool contracts;
- response contracts;
- workflow state contract.

## Success Criteria

- app loads config safely;
- invalid environment values fail loudly;
- hosted and local startup expectations are explicit;
- contracts are reusable across modules.

Implementation note:

- This phase is intentionally delivered through three narrow slices:
  - `settings-env-validation`
  - `shared-contracts-foundation`
  - `deployment-mode-flags`
- Provider credential activation follows this sequence unless a later spec
  explicitly changes it:
  - Qdrant credentials activate in `Phase 4`;
  - Groq credentials activate in `Phase 5`;
  - Phoenix endpoint activates in `Phase 6` when hosted tracing is enabled.

---

# Phase 2 — PDF Processing Pipeline

## Goal

Convert PDFs into clean Markdown.

## Deliverables

- Docling integration;
- PDF ingestion pipeline;
- ingestion execution model;
- Markdown export;
- cleaning pipeline;
- metadata extraction.

## Success Criteria

- PDFs convert reliably;
- Markdown preserves useful structure;
- processed documents are stored consistently;
- container/runtime dependencies for Docling are validated;
- raw and processed document storage is reproducible.

Implementation note:

- This phase is intentionally delivered through two narrow slices:
  - `docling-ingestion-skeleton`
  - `markdown-cleaning-and-metadata-extraction`

Initial narrow slices:

- `docling-ingestion-skeleton` covers Docling setup, admin CLI ingestion flow,
  reproducible storage layout, failure reporting, and typed processed-document
  contracts before later cleaning and chunking slices.
- `markdown-cleaning-and-metadata-extraction` extends the ingestion pipeline
  with conservative Markdown cleaning, deterministic cleaned artifacts, minimal
  metadata extraction, and explicit post-conversion failure behavior.

---

# Phase 3 — Semantic Chunking

## Goal

Create retrieval-ready chunks.

## Deliverables

- chunking module;
- configurable chunk size/overlap;
- metadata propagation;
- deterministic chunk identifiers;
- chunk schema versioning;
- chunk persistence.

## Success Criteria

- chunks preserve semantic meaning;
- clauses are not arbitrarily split;
- metadata remains traceable;
- re-chunking behavior is predictable across deployments.

Implementation note:

- This phase is intentionally delivered through multiple narrow slices:
  - `deterministic-chunk-contracts-and-persistence`
  - `semantic-boundary-aware-chunk-refinement`

Initial narrow slices:

- `deterministic-chunk-contracts-and-persistence` should cover:
  - the first chunk contract for cleaned Markdown outputs;
  - configurable chunk size and overlap settings;
  - deterministic chunk identifiers;
  - metadata propagation from processed documents into chunks;
  - chunk persistence to local reproducible artifacts before Qdrant indexing.
- `semantic-boundary-aware-chunk-refinement` should cover:
  - heading-aware and clause-safe chunk boundary refinement;
  - stricter prevention of arbitrary clause splitting;
  - improved section metadata propagation into chunk records;
  - stable chunk schema version advancement when boundary logic changes;
  - rerun behavior that preserves determinism while improving chunk quality.

---

# Phase 4 — Embeddings and Vector Store

## Goal

Index chunks into Qdrant Cloud.

## Deliverables

- embedding pipeline;
- Qdrant integration;
- collection setup;
- indexing workflow;
- idempotent indexing behavior;
- retry/backoff behavior;
- retrieval smoke tests.

## Success Criteria

- chunks are searchable;
- metadata filters work;
- retrieval returns meaningful results;
- collection bootstrap is repeatable;
- indexing can be rerun safely.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `embedding-generation-and-local-artifacts` should cover:
  - deterministic embedding inputs derived from persisted chunk bundles;
  - provider/model-aware embedding configuration usage from `core.config`;
  - typed local embedding artifact persistence before Qdrant writes;
  - explicit vector payload shape for later indexing;
  - failure handling and rerun determinism for offline embedding generation.
- `qdrant-collection-bootstrap-and-idempotent-indexing` should cover:
  - Qdrant client wiring and collection bootstrap;
  - idempotent upsert behavior from local embedding artifacts;
  - metadata filter payload mapping;
  - retry/backoff behavior;
  - indexing smoke checks against the configured collection.

Current implementation status:

- completed:
  - `embedding-generation-and-local-artifacts`
  - `qdrant-collection-bootstrap-and-idempotent-indexing`

- remaining in `Phase 4`:
  - none

---

# Phase 5 — Basic RAG MVP

## Goal

Create the first grounded QA system.

## Deliverables

- retrieval pipeline;
- grounded answer generation;
- citations;
- simple Gradio query interface;
- deployable hosted app package;
- startup and request smoke tests.

## Success Criteria

- advisor can ask questions;
- system returns grounded answers;
- citations appear consistently;
- hosted app starts reliably;
- user-visible failure states exist.

Clarification:

- This phase is the first usable grounded QA slice, not the full
  portfolio-complete MVP defined later in this roadmap.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `retrieval-pipeline-and-ranked-results` should cover:
  - query embedding generation through the configured embedding path;
  - Qdrant search against the indexed collection;
  - mapping search hits into typed `RetrievedChunk` results;
  - deterministic metadata and citation traceability in retrieval outputs;
  - retrieval smoke checks and failure behavior before answer generation.
- `grounded-answer-generation-and-citations` should cover:
  - prompt construction from retrieved evidence;
  - Groq-backed grounded answer generation;
  - citation formatting and response contracts;
  - basic failure handling for empty or insufficient retrieval results;
  - initial end-to-end grounded QA flow before UI work expands further.
- `gradio-query-ui-and-hosted-smoke` should cover:
  - the first user-facing Gradio query interface over the grounded QA path;
  - startup validation for the hosted app path;
  - request smoke checks for the public MVP demo;
  - minimal user-visible failure states for retrieval and answer-generation errors;
  - deployable hosted packaging for the first usable MVP interaction surface.

Current implementation status:

- completed:
  - `retrieval-pipeline-and-ranked-results`
  - `grounded-answer-generation-and-citations`
  - `gradio-query-ui-and-hosted-smoke`

---

# Phase 6 — Baseline Observability

## Goal

Make system behavior diagnosable before tools and multi-agent orchestration
increase complexity.

## Deliverables

- request and correlation identifiers;
- startup diagnostics;
- retrieval traces;
- latency tracking;
- structured error events;
- basic hosted health/readiness checks.

## Success Criteria

- traces and diagnostics are visible during local and hosted runs;
- startup failures are actionable;
- performance bottlenecks can be localized.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `startup-diagnostics-and-request-correlation` should cover:
  - request identifiers;
  - startup diagnostics for active configuration and runtime mode;
  - structured logging hooks around retrieval and grounded-answer execution;
  - explicit error-event shape for the current CLI and app entrypoints.
- `retrieval-traces-and-hosted-health-checks` should cover:
  - retrieval and answer-generation latency tracking;
  - hosted health/readiness checks;
  - narrow Phoenix activation where configured;
  - smoke visibility for the MVP runtime path.

Current implementation status:

- completed:
  - `startup-diagnostics-and-request-correlation`
  - `retrieval-traces-and-hosted-health-checks`

---

# Phase 7 — Core Tooling

## Goal

Implement reusable tools.

## Deliverables

- document_retrieval_tool;
- clause_extraction_tool;
- policy_comparison_tool;
- citation_verifier_tool;
- response_draft_tool;
- tool error contracts;
- tool latency expectations.

## Success Criteria

- tools are independently callable;
- contracts are typed;
- outputs are structured;
- tool failures are observable.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `document-retrieval-tool-and-error-contracts` should cover:
  - one independently callable retrieval tool wrapper over the current
    retrieval pipeline;
  - explicit tool-level success and failure behavior;
  - narrow latency expectations for retrieval execution;
  - typed error surface for tool callers.
- `clause-extraction-tool-from-retrieved-evidence` should cover:
  - clause extraction over retrieved chunks only;
  - typed clause categorization and failure behavior;
  - no policy comparison or answer drafting yet.
- `policy-comparison-tool-from-typed-evidence` should cover:
  - policy comparison over typed evidence and extracted clauses;
  - structured comparison points and insufficient-information behavior;
  - observable failure handling for the comparison path only.
- `citation-verifier-tool` should cover:
  - citation verification over drafted outputs and cited evidence;
  - explicit verification success/failure contracts;
  - observable failure handling for the verification path only.
- `response-draft-tool` should cover:
  - a reusable drafting seam over the grounded QA backend;
  - typed response-draft behavior for later workflow reuse;
  - no LangGraph orchestration yet.

Current implementation status:

- completed:
  - `document-retrieval-tool-and-error-contracts`
  - `clause-extraction-tool-from-retrieved-evidence`
  - `policy-comparison-tool-from-typed-evidence`
  - `citation-verifier-tool`
  - `response-draft-tool`
- remaining in `Phase 7`:
  - none

---

# Phase 8 — LangGraph Workflow

## Goal

Replace basic RAG with controlled multi-agent orchestration.

## Deliverables

- LangGraph setup;
- shared workflow state;
- Planner Agent;
- Retriever Agent;
- Policy Analyst Agent;
- Citation Verifier;
- Response Formatter Agent;
- state transition tracing.

## Success Criteria

- workflow executes end-to-end;
- state transitions are observable;
- fallbacks work.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `langgraph-state-and-linear-workflow-skeleton` should cover:
  - LangGraph project wiring;
  - one shared workflow state over existing typed tool contracts;
  - a single linear workflow path using the existing reusable tools;
  - observable state transition tracing without planner branching yet.
- `planner-and-tool-routing-agent` should cover:
  - a narrow planner step that selects among the existing tool paths;
  - explicit routing decisions and typed fallback behavior;
  - no multi-branch recovery or advanced planning yet.
- `policy-analyst-and-verifier-workflow-pass` should cover:
  - integration of comparison, verification, and drafting inside the graph;
  - one end-to-end analyst/verifier/drafter pass over the existing tools;
  - no UI redesign or external tool exposure yet.
- `workflow-insufficient-evidence-fallbacks` should cover:
  - typed fallback edges for weak or insufficient evidence only;
  - observable fallback transitions for conservative non-error outcomes;
  - no retry behavior yet.
- `workflow-tool-failure-retry-policies` should cover:
  - retry boundaries for selected tool/runtime failures only;
  - observable retry and terminal-failure transitions;
  - no broader recovery tree beyond the existing workflow path.

Current implementation status:

- completed:
  - `langgraph-state-and-linear-workflow-skeleton`
  - `planner-and-tool-routing-agent`
  - `policy-analyst-and-verifier-workflow-pass`
  - `workflow-insufficient-evidence-fallbacks`
  - `workflow-tool-failure-retry-policies`
- remaining in `Phase 8`:
  - none

---

# Phase 9 — Guardrails

## Goal

Add safety and scope protections.

## Deliverables

- prompt injection detection;
- scope validation;
- refusal behavior;
- confidence scoring;
- mandatory citation enforcement;
- abuse-case test scenarios;
- refusal telemetry.

## Success Criteria

- unsupported queries are rejected safely;
- unsafe behavior is measurable against abuse cases;
- confidence signals appear consistently.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `unsupported-query-scope-guardrails` should cover:
  - explicit scope validation for out-of-scope or unsupported user queries;
  - conservative refusal behavior at the workflow and UI boundary;
  - no prompt-injection handling or abuse-case suite yet.
- `citation-and-confidence-guardrails` should cover:
  - this concern should be split further into narrower slices before implementation.
- `answer-citation-presence-guardrails` should cover:
  - mandatory citation presence checks for answerable responses only;
  - conservative fallback or refusal behavior when an answerable response lacks citations;
  - no confidence-policy expansion yet.
- `response-confidence-consistency-guardrails` should cover:
  - confidence consistency checks across typed response outputs;
  - conservative downgrade behavior for mismatched confidence signals;
  - no injection detection or telemetry expansion yet.
- `prompt-injection-and-abuse-case-telemetry` should cover:
  - this concern should be split further into narrower slices before implementation.
- `prompt-injection-signals-and-refusal` should cover:
  - narrow prompt-injection detection signals;
  - conservative refusal behavior when those signals trigger;
  - no abuse-case suite expansion yet.
- `abuse-case-validation-and-refusal-telemetry` should cover:
  - this concern should be split further into narrower slices before implementation.
- `guardrail-abuse-case-scenarios` should cover:
  - abuse-case validation scenarios for the implemented guardrails only;
  - regression-oriented tests for unsafe or boundary-seeking prompts;
  - no telemetry aggregation changes yet.
- `refusal-telemetry-and-guardrail-summary` should cover:
  - refusal telemetry for guardrail-triggered outcomes;
  - a narrow summary surface for guardrail/refusal events;
  - no new injection-detection heuristics.

Current implementation status:

- completed:
  - `unsupported-query-scope-guardrails`
  - `answer-citation-presence-guardrails`
  - `response-confidence-consistency-guardrails`
  - `prompt-injection-signals-and-refusal`
  - `guardrail-abuse-case-scenarios`
  - `refusal-telemetry-and-guardrail-summary`
- remaining in `Phase 9`:
  - none

---

# Phase 10 — Evaluation Dataset

## Goal

Create a repeatable evaluation baseline.

## Deliverables

- 30 curated evaluation questions;
- evaluation schemas;
- golden dataset;
- evaluation runner;
- hosted-like regression scenarios.

## Success Criteria

- evaluation can run automatically;
- results are reproducible;
- retrieval quality can be measured;
- startup, latency, and citation regressions are detectable.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `evaluation-schema-and-question-set` should cover:
  - typed evaluation schemas;
  - a first curated question set;
  - no runner execution yet.
- `question-set-expansion-and-category-balance` should cover:
  - expansion from the initial question set toward the 30-question target;
  - category balance across normal QA and guardrail scenarios;
  - no golden reference outputs yet.
- `question-set-target-30-completion` should cover:
  - completion of the curated set to the 30-question roadmap target;
  - final gap-filling across underrepresented scenarios;
  - no golden reference outputs yet.
- `golden-behavior-and-guardrail-outcomes` should cover:
  - golden expected behavior labels for the curated question set;
  - expected refusal or guarded-answer outcomes where applicable;
  - no retrieval/citation evidence expectations yet.
- `retrieval-expectation-annotations` should cover:
  - retrieval expectations where applicable;
  - explicit evidence-oriented retrieval annotations over the existing golden set;
  - no citation-specific expectation work yet.
- `citation-expectation-annotations` should cover:
  - citation expectations where applicable;
  - explicit citation-oriented annotations over the existing retrieval-aware golden set;
  - no hosted-like regression execution yet.
- `evaluation-runner-contract-and-result-schema` should cover:
  - typed local evaluation result contracts;
  - deterministic result-shape definitions over the curated evaluation assets;
  - no runner execution yet.
- `local-evaluation-runner-execution` should cover:
  - a repeatable local evaluation runner;
  - deterministic execution over the curated evaluation assets;
  - no hosted-like regression scenarios yet.
- `hosted-startup-and-health-smokes` should cover:
  - hosted-like startup and health smoke scenarios;
  - smoke-oriented execution over the existing local runner surface where relevant;
  - no latency or citation regression checks yet.
- `hosted-latency-smokes` should cover:
  - hosted-like latency regression smoke scenarios;
  - smoke-oriented execution over the existing local runner surface;
  - no citation regression checks yet.
- `hosted-citation-regression-smokes` should cover:
  - hosted-like citation regression smoke scenarios;
  - smoke-oriented execution over the existing local runner surface;
  - no DSPy optimization yet.
- `behavioral-evaluation-runner-remediation` should cover:
  - removal of tautological behavior evaluation in the local runner;
  - explicit linkage of run results to the active expectation datasets;
  - correction of any duplicated golden-output ownership between question and golden datasets.

Current implementation status:

- completed:
  - `evaluation-schema-and-question-set`
  - `question-set-expansion-and-category-balance`
  - `question-set-target-30-completion`
  - `golden-behavior-and-guardrail-outcomes`
  - `retrieval-expectation-annotations`
  - `citation-expectation-annotations`
  - `evaluation-runner-contract-and-result-schema`
  - `local-evaluation-runner-execution`
  - `hosted-startup-and-health-smokes`
  - `hosted-latency-smokes`
  - `hosted-citation-regression-smokes`
  - `behavioral-evaluation-runner-remediation`
- remaining in `Phase 10`:
  - none

---

# Phase 11 — DSPy Optimization

## Goal

Optimize one targeted component programmatically.

## Recommended Targets

- query rewriting;
- answer drafting;
- retrieval routing;
- query classification.

## Deliverables

- DSPy module;
- optimization dataset subset;
- before/after comparison;
- latency and cost comparison.

## Success Criteria

- the optimization outcome is truthfully reported on the documented evaluation
  surface;
- optimization process is documented;
- hosted-like latency remains within budget on the product-facing
  classification path.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `optimization-target-selection-and-baseline` should cover:
  - selection of one optimization target from the recommended set;
  - explicit baseline metric definition for that target;
  - no DSPy module implementation yet.
- `dspy-query-classification-module-skeleton` should cover:
  - one minimal DSPy module for query classification;
  - explicit input/output contract for local optimization work;
  - no optimization dataset subset yet.
- `query-classification-optimization-dataset-subset` should cover:
  - a narrow dataset subset for query classification optimization;
  - stable linkage to the existing evaluation assets where relevant;
  - no before/after comparison yet.
- `query-classification-quality-comparison` should cover:
  - measurable baseline versus optimized quality comparison for query
    classification;
  - explicit per-category and overall evaluation reporting;
  - no latency or cost comparison yet.
- `query-classification-latency-comparison` should cover:
  - latency comparison for the optimized query-classification path;
  - explicit comparison against the documented deterministic baseline;
  - no cost comparison yet.
- `query-classification-cost-comparison` should cover:
  - cost comparison for the optimized query-classification path;
  - explicit comparison against the documented zero-external-call baseline;
  - no broader productionization yet.
- `query-classification-optimized-predictor-wiring` should cover:
  - one real optimized query-classification callable built from the DSPy
    module and current optimization subset;
  - explicit wiring into the existing quality, latency, and cost comparison
    seams;
  - no claim of measurable improvement yet.
- `query-classification-quality-improvement-validation` should cover:
  - documented before/after quality results from the real optimized predictor;
  - explicit confirmation of whether quality measurably improves over the
    deterministic baseline;
  - no latency-budget validation yet.
- `query-classification-latency-budget-validation` should cover:
  - explicit confirmation of whether the optimized query-classification path
    remains within the documented latency budget;
  - documented linkage to the existing latency-comparison seam;
  - no broader productionization yet.
- `query-classification-measurable-improvement-remediation` should cover:
  - replacement of the current optimization-infrastructure-only closure with a
    real optimized predictor path that can demonstrate measurable improvement,
    or an explicit downgrade of the success claim if such improvement is not
    defensible yet;
  - alignment of the comparison surface with the documented `Phase 11`
    baseline;
  - no hosted-latency validation yet.
- `hosted-query-classification-latency-budget-validation` should cover:
  - validation that the product-facing optimized classification path remains
    within the documented latency budget;
  - explicit distinction between local seam timing and hosted-like request-path
    timing;
  - no broader productionization yet.

Selected first target and baseline:

- selected target:
  - `query classification`
- rationale:
  - it already has narrow deterministic seams in `query_scope` and
    `prompt_guardrails`;
  - it is directly measurable with the existing 30-question evaluation assets;
  - it has lower latency and cost risk than answer drafting or retrieval
    routing for the first DSPy slice.
- baseline quality surface:
  - exact-match rate against `ExpectedBehavior` over the 30-question evaluation
    set;
  - per-category exact-match rate across grounded QA, unsupported, prompt
    injection, citation guardrail, and confidence guardrail scenarios.
- current narrow comparison surface for `Phase 11` implementation:
  - the 10-example query-classification optimization subset;
  - this subset is the current defensible surface for baseline-versus-optimized
    comparison and improvement reporting;
  - it is narrower than the 30-question evaluation set and should be treated as
    such in validation claims.
- baseline latency surface:
  - wall-clock duration of `run_local_evaluation()`;
  - derived per-question average duration from the local evaluation run.
- baseline cost surface:
  - current baseline is zero external model calls for the deterministic local
    classification seam;
  - future DSPy comparisons must report any incremental model-call or token-cost
    surface against that baseline.

Current implementation status:

- completed:
  - `optimization-target-selection-and-baseline`
  - `dspy-query-classification-module-skeleton`
  - `query-classification-optimization-dataset-subset`
  - `query-classification-quality-comparison`
  - `query-classification-latency-comparison`
  - `query-classification-cost-comparison`
  - `query-classification-optimized-predictor-wiring`
  - `query-classification-quality-improvement-validation`
  - `query-classification-latency-budget-validation`
  - `query-classification-measurable-improvement-remediation`
  - `hosted-query-classification-latency-budget-validation`
- remaining in `Phase 11`:
  - none

---

# Phase 12 — MCP Integration

## Goal

Expose tools through MCP.

## Deliverables

- MCP server;
- MCP client;
- tool exposure;
- MCP tests;
- interface versioning plan.

## Success Criteria

- tools are callable through MCP;
- contracts remain stable;
- MCP boundaries are operationally explicit.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `mcp-transport-and-server-contract-skeleton` should cover:
  - one minimal MCP server boundary for the current tool surface;
  - explicit request/response contract shape for the server seam;
  - no tool execution wiring yet.
- `mcp-tool-registration-and-exposure` should cover:
  - registration of the initial callable tools through the MCP server;
  - explicit mapping from current local tool seams into MCP-visible tools;
  - no client integration yet.
- `mcp-client-seam-and-local-roundtrip` should cover:
  - one narrow local MCP client seam;
  - end-to-end roundtrip validation against the registered tool surface;
  - no interface versioning plan yet.
- `mcp-interface-version-policy` should cover:
  - an explicit versioning policy for the exposed MCP interface;
  - naming and bump rules for future MCP-surface changes;
  - no compatibility-boundary matrix yet.
- `mcp-tool-compatibility-boundaries` should cover:
  - explicit compatibility boundaries for future tool evolution;
  - forward/backward-compatibility expectations for the current MCP-visible
    surface;
  - no broader deployment work yet.
- `mcp-request-field-and-tool-metadata-compatibility-remediation` should cover:
  - explicit compatibility expectations for MCP request fields and MCP-visible
    tool metadata on the current surface;
  - alignment of the implemented compatibility seam with the final `Phase 12`
    boundary requirements;
  - no broader error-contract hardening or deployment work yet.

Current implementation status:

- completed:
  - `mcp-transport-and-server-contract-skeleton`
  - `mcp-tool-registration-and-exposure`
  - `mcp-client-seam-and-local-roundtrip`
  - `mcp-interface-version-policy`
  - `mcp-tool-compatibility-boundaries`
  - `mcp-request-field-and-tool-metadata-compatibility-remediation`
- remaining in `Phase 12`:
  - none

---

# Phase 13 — Demo UI Hardening

## Goal

Improve public demo usability.

## Deliverables

- better Gradio layout;
- source display;
- confidence display;
- trace summary display;
- loading states;
- error states;
- degraded-service messaging.

## Success Criteria

- demo is understandable;
- outputs are easy to review;
- failures are visible;
- support/debug context is exposed safely.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `demo-layout-and-output-grouping` should cover:
  - improved Gradio layout for the current MVP surface;
  - clearer grouping of answer, citations, confidence, and limitations;
  - no trace-summary or degraded-service messaging yet.
- `demo-trace-summary-display` should cover:
  - a narrow user-visible trace summary surface;
  - reuse of current workflow and observability seams where available;
  - no support/debug context exposure yet.
- `demo-support-context-display` should cover:
  - safe exposure of user-visible support context tied to current observability seams;
  - concise support details that help follow up on a request without exposing
    operator-only internals;
  - no broader debug-metadata exposure yet.
- `demo-debug-metadata-exposure` should cover:
  - safe exposure of operator-facing debug metadata for the current demo path;
  - clear separation from the user-visible support context already shown in the UI;
  - no degraded-service messaging yet.
- `demo-loading-state-feedback` should cover:
  - explicit loading-state behavior for the public demo path;
  - user-visible in-flight feedback during request execution;
  - no user-visible error-state redesign yet.
- `demo-error-state-clarity` should cover:
  - clearer user-visible error states for current failures;
  - alignment with the existing request failure surface;
  - no degraded-service messaging yet.
- `demo-readiness-degraded-messaging` should cover:
  - explicit degraded-service messaging for known runtime-readiness and
    dependency-availability problems;
  - alignment with the current readiness semantics already exposed by the app;
  - no answer-quality degradation messaging yet.
- `demo-answer-quality-degraded-messaging` should cover:
  - explicit degraded-service messaging for partial-answer or reduced-quality
    response conditions that still return a draft;
  - alignment with current guardrails and review-oriented output semantics;
  - no broader deployment work yet.

Current implementation status:

- completed:
  - `demo-layout-and-output-grouping`
  - `demo-trace-summary-display`
  - `demo-trace-summary-sanitization-remediation`
  - `demo-support-context-display`
  - `demo-debug-metadata-exposure`
  - `demo-loading-state-feedback`
  - `demo-error-state-clarity`
  - `demo-readiness-degraded-messaging`
  - `demo-answer-quality-degraded-messaging`
- remaining in `Phase 13`:
  - none

---

# Phase 14 — Docker and Deployment Hardening

## Goal

Harden the MVP deployment path for a safe public demo while preserving a clean
bridge to future internal production deployment.

## Deliverables

- production-ready Dockerfile;
- Hugging Face Spaces deployment;
- environment setup;
- deployment documentation;
- hosted smoke tests;
- deployment rollback notes;
- explicit demo-mode operating constraints.

## Success Criteria

- app deploys successfully;
- public demo is accessible;
- startup is stable;
- public demo guardrails are documented;
- deployment steps are reproducible.

Implementation note:

- This phase should also be delivered through narrow slices.

Initial narrow slices:

- `dockerfile-runtime-skeleton` should cover:
  - one production-oriented Dockerfile for the current app/runtime path;
  - explicit dependency installation and app entrypoint wiring;
  - no hosted platform deployment work yet.
- `container-local-smoke-and-startup-validation` should cover:
  - local container build validation for the current app path;
  - explicit confirmation that the Docker runtime skeleton can be built locally;
  - no startup or readiness smoke execution yet.
- `container-local-startup-validation` should cover:
  - local container startup validation for the current app path;
  - explicit confirmation that the built image can launch the current app entrypoint;
  - no readiness probing or hosted deployment work yet.
- `container-local-readiness-validation` should cover:
  - explicit readiness validation after successful local container startup;
  - smoke checks for the current readiness surface only;
  - no hosted deployment platform work yet.
- `hugging-face-spaces-config-and-launch-surface` should cover:
  - minimal Hugging Face Spaces configuration surface for the current demo;
  - explicit environment/runtime expectations for that hosted target;
  - no launch artifact wiring yet.
- `hugging-face-spaces-launch-artifacts` should cover:
  - the minimal repository-side Docker launch artifact expected by the configured Spaces target;
  - explicit alignment between the chosen Spaces runtime config and the selected Docker build file;
  - no start-command normalization yet.
- `hugging-face-spaces-start-command-alignment` should cover:
  - removal or explicit resolution of stale start-command artifacts that still imply a second Spaces launch path;
  - no Dockerfile or broader deployment-doc work yet.
- `hugging-face-spaces-entrypoint-normalization` should cover:
  - final alignment between the selected Spaces Docker launch artifact and the current app entrypoint;
  - any minimal start script or command normalization required by the Spaces target after stale artifact cleanup;
  - no rollback or operations notes yet.
- `deployment-docs-for-spaces` should cover:
  - deployment instructions for the chosen Hugging Face Spaces target;
  - the minimal operator steps needed to publish the current repo state there;
  - no operating-constraints or rollback notes yet.
- `demo-runtime-and-dependency-constraints-notes` should cover:
  - explicit demo-mode runtime and dependency constraints for the hosted demo;
  - narrow documentation of required environment variables and hosted runtime assumptions;
  - no guardrail/scope notes or rollback playbook yet.
- `demo-guardrail-and-refusal-constraints-notes` should cover:
  - explicit demo-mode guardrail and refusal notes for the hosted demo;
  - narrow documentation of user-visible guardrail behavior tied to the current advisor surface;
  - no supported-scope notes or rollback playbook yet.
- `demo-supported-scope-constraints-notes` should cover:
  - explicit supported-scope notes for the hosted demo;
  - narrow documentation of user-visible scope limitations tied to the current advisor surface;
  - no rollback playbook yet.
- `deployment-rollback-notes` should cover:
  - rollback notes for the hosted deployment path;
  - the minimum operator guidance for reverting the current hosted demo state;
  - no hosted smoke expectations or broader productionization work yet.
- `hosted-smoke-expectations-and-operator-notes` should cover:
  - final hosted smoke expectations for the deployed demo;
  - narrow operator notes for checking the hosted surface after deployment;
  - no broader productionization work yet.
- `hosted-spaces-deployment-validation-and-evidence` should cover:
  - one real Hugging Face Spaces deployment validation for the current demo;
  - durable recording of the deployed Space URL, deployed commit SHA, and actual hosted smoke results;
  - no broader productionization work yet.
- `spaces-entrypoint-normalization-traceability-remediation` should cover:
  - either a dated spec/validation artifact for the roadmap-claimed entrypoint normalization slice;
  - or explicit removal/correction of that completion claim if traceability cannot be shown;
  - no hosted deployment execution work yet.
- `readme-phase-status-sync` should cover:
  - synchronization of the top-level README phase-status summary with the actual implemented roadmap state;
  - no deployment behavior changes or broader documentation rewrite.

Current implementation status:

- completed:
  - `dockerfile-runtime-skeleton`
  - `container-local-build-validation`
  - `container-local-startup-validation`
  - `container-local-readiness-validation`
  - `hugging-face-spaces-runtime-config`
  - `hugging-face-spaces-dockerfile-alignment`
  - `hugging-face-spaces-start-artifact-cleanup`
  - `hugging-face-spaces-entrypoint-normalization`
  - `deployment-docs-for-spaces`
  - `demo-runtime-and-dependency-constraints-notes`
  - `demo-guardrail-and-refusal-constraints-notes`
  - `demo-supported-scope-constraints-notes`
  - `deployment-rollback-notes`
  - `hosted-smoke-expectations-and-operator-notes`
  - `hosted-spaces-deployment-validation-and-evidence`
  - `spaces-entrypoint-normalization-traceability-remediation`
  - `readme-phase-status-sync`
- remaining in `Phase 14`:
  - none

---

# Phase 15 — Final Evaluation and Cleanup

## Goal

Stabilize the project for final delivery.

## Deliverables

- README completion;
- architecture diagrams;
- evaluation report;
- deployment guide;
- cleanup of dead code;
- final tests;
- roadmap and operational documentation review.

## Success Criteria

- repository is understandable;
- demo is stable;
- deployment and evaluation artifacts are consistent.

## Narrow Slices

- `spanish-demo-ui-localization`
- `spanish-retrieval-and-embedding-alignment`
- `spanish-guardrail-and-scope-alignment`
- `spanish-evaluation-fixtures-and-smoke-coverage`
- `spanish-ui-state-derivation-hardening`
- `phase-15-final-readme-and-roadmap-sync`
- `readme-phase-18-19-status-and-milestones-sync`
- `architecture-and-repo-surface-status-sync`
- `local-embedding-runtime-remediation`
- `spanish-query-scope-autos-alignment-remediation`
- `arl-supported-scope-alignment-remediation`
- `bicicletas-patinetas-supported-scope-alignment-remediation`
- `bicicletas-patinetas-pv-diagrammatic-block-normalization-remediation`
- `bicicletas-patinetas-pv-requirements-and-deductible-linear-normalization`
- `bicicletas-patinetas-deductible-evidence-bias-remediation`
- `bicicletas-patinetas-deductible-candidate-recall-remediation`

Current implementation status:

completed:

- `spanish-demo-ui-localization`
- `spanish-retrieval-and-embedding-alignment`
- `spanish-guardrail-and-scope-alignment`
- `spanish-evaluation-fixtures-and-smoke-coverage`
- `spanish-ui-state-derivation-hardening`
- `phase-15-final-readme-and-roadmap-sync`
- `readme-phase-18-19-status-and-milestones-sync`
- `architecture-and-repo-surface-status-sync`
- `local-embedding-runtime-remediation`
- `spanish-query-scope-autos-alignment-remediation`
- `arl-supported-scope-alignment-remediation`
- `bicicletas-patinetas-supported-scope-alignment-remediation`
- `bicicletas-patinetas-pv-diagrammatic-block-normalization-remediation`
- `bicicletas-patinetas-pv-requirements-and-deductible-linear-normalization`
- `bicicletas-patinetas-deductible-evidence-bias-remediation`
- `bicicletas-patinetas-deductible-candidate-recall-remediation`

---

# Phase 16 — Ingestion Runtime Remediation

## Goal

Restore a practical, verifiable local ingestion path for PDF-to-markdown
conversion when the current Docling-based runtime does not start in a
reasonable development loop.

## Deliverables

- documented root-cause evidence for the Docling startup block;
- a narrow remediation decision for local ingestion;
- restored ability to run PDF-to-markdown ingestion locally, or an explicit
  approved fallback path;
- updated operational documentation for the chosen ingestion posture.

## Success Criteria

- the repo has a practical local path to convert sample PDFs into markdown
  artifacts;
- the remediation is evidenced, not speculative;
- the chosen ingestion path is documented and testable.

## Narrow Slices

- `docling-ingestion-startup-remediation`
- `docling-primary-local-ingestion-policy`
- `recursive-ingestion-and-path-derived-document-ids`
- `qdrant-point-id-normalization`
- `qdrant-retrieval-client-compatibility`
- `docling-timeout-pdfium-fallback-remediation`

Current implementation status:

completed:

- `docling-ingestion-startup-remediation`
- `docling-primary-local-ingestion-policy`
- `recursive-ingestion-and-path-derived-document-ids`
- `qdrant-point-id-normalization`
- `qdrant-retrieval-client-compatibility`
- `docling-timeout-pdfium-fallback-remediation`

remaining in `Phase 16`:

- none

---

# Phase 17 — Runtime Compatibility Hardening

## Goal

Stabilize the final external runtime dependencies that still determine whether
the validated local RAG pipeline can answer real user queries end-to-end.

## Deliverables

- explicit runtime compatibility evidence for the configured LLM provider/model;
- synchronized local configuration examples for the supported runtime;
- a documented end-to-end answer-path validation that includes real retrieval
  and real model completion.

## Success Criteria

- the configured Groq model identifier is correct and documented;
- local runtime configuration examples do not drift from the validated setup;
- `answer-query` succeeds end-to-end against the indexed sample corpus.

## Narrow Slices

- `groq-model-runtime-compatibility`
- `groq-default-config-and-readme-contract-alignment`
- `hosted-latency-smoke-budget-remediation`
- `readme-phase-16-and-17-status-sync`
- `external-batch-runtime-operator-flow`

Current implementation status:

completed:

- `groq-model-runtime-compatibility`
- `groq-default-config-and-readme-contract-alignment`
- `hosted-latency-smoke-budget-remediation`
- `readme-phase-16-and-17-status-sync`
- `external-batch-runtime-operator-flow`

remaining in `Phase 17`:

- none

---

# Phase 18 — Corpus Metadata and Retrieval Traceability

## Goal

Strengthen the document-metadata layer that sits between local ingestion and
advisor-facing retrieval so the corpus is easier to operate, filter, inspect,
and cite as the real Spanish document set grows.

## Deliverables

- clearer document-level metadata contracts beyond path-derived ids;
- explicit traceability from raw source structure to retrieval-facing document
  identifiers and labels;
- a foundation for later filter quality and citation readability improvements.

## Success Criteria

- corpus metadata responsibilities are explicit and reviewable;
- the repository no longer relies on `source_pdf_id` alone as the practical
  document identity surface for future retrieval-facing improvements;
- the first metadata-enrichment seam remains narrow and locally testable.

## Narrow Slices

- `document-metadata-contract-baseline`
- `source-relative-path-through-retrieval-payloads`
- `unsupported-metadata-filter-guardrail`
- `operator-curated-document-metadata-overlays`
- `document-metadata-filter-enablement`
- `operator-curated-term-equivalence-normalization`
- `qdrant-metadata-filter-index-alignment`
- `noisy-document-title-heading-guardrail`
- `autos-plan-comparison-retrieval-alignment`
- `autos-plan-comparison-reranking-or-evidence-bias`
- `section-context-prefixed-chunk-remediation`
- `autos-comparison-corpus-retrievability-remediation`
- `autos-comparison-table-normalization-remediation`
- `autos-comparison-hybrid-recall-remediation`
- `source-path-product-filter-fallback-remediation`
- `source-path-product-metadata-backfill`
- `source-path-document-type-metadata-backfill`
- `bicicletas-patinetas-corpus-baseline-ingestion-and-retrieval`
- `motos-corpus-baseline-ingestion-and-retrieval`
- `motos-plan-comparison-retrieval-alignment`
- `movilidad-choque-simple-corpus-completion-baseline`
- `movilidad-choque-simple-evidence-structuring-remediation`
- `movilidad-choque-simple-photo-guide-title-and-structure-remediation`
- `movilidad-choque-simple-supported-scope-and-retrieval`
- `movilidad-pv-portafolio-baseline-ingestion-and-extraction-audit`
- `movilidad-pv-structure-and-chunk-dedup-remediation`
- `movilidad-pv-applicability-collapse-and-inline-tail-remediation`
- `movilidad-pv-retrieval-readiness-audit`
- `movilidad-pv-duplicate-applicability-dedup-remediation`
- `embedding-runtime-readiness-validation`
- `movilidad-pv-embedding-and-indexing-execution`
- `movilidad-pv-query-intent-and-ranking-alignment`
- `movilidad-pv-document-family-ranking-alignment`
- `qdrant-document-name-filter-index-alignment`
- `movilidad-pv-benefit-breadth-and-duplicate-section-diversification`
- `movilidad-transversales-corpus-baseline-ingestion-and-retrieval`
- `muevete-libre-corpus-baseline-ingestion-and-retrieval`
- `muevete-libre-coverage-breadth-evidence-balancing`
- `muevete-libre-intrasection-coverage-chunk-prioritization`
- `muevete-libre-coverage-retrieval-alignment`
- `soat-corpus-baseline-ingestion-and-retrieval`
- `soat-coverage-document-type-alignment`
- `soat-coverage-evidence-prioritization-alignment`

Current implementation status:

completed:

- `document-metadata-contract-baseline`
- `source-relative-path-through-retrieval-payloads`
- `unsupported-metadata-filter-guardrail`
- `operator-curated-document-metadata-overlays`
- `document-metadata-filter-enablement`
- `operator-curated-term-equivalence-normalization`
- `qdrant-metadata-filter-index-alignment`
- `noisy-document-title-heading-guardrail`
- `autos-plan-comparison-retrieval-alignment`
- `autos-plan-comparison-reranking-or-evidence-bias`
- `section-context-prefixed-chunk-remediation`
- `autos-comparison-corpus-retrievability-remediation`
- `autos-comparison-table-normalization-remediation`
- `autos-comparison-hybrid-recall-remediation`
- `source-path-product-filter-fallback-remediation`
- `source-path-product-metadata-backfill`
- `source-path-document-type-metadata-backfill`
- `bicicletas-patinetas-corpus-baseline-ingestion-and-retrieval`
- `motos-corpus-baseline-ingestion-and-retrieval`
- `motos-plan-comparison-retrieval-alignment`
- `movilidad-choque-simple-corpus-completion-baseline`
- `movilidad-choque-simple-evidence-structuring-remediation`
- `movilidad-choque-simple-photo-guide-title-and-structure-remediation`
- `movilidad-choque-simple-supported-scope-and-retrieval`
- `movilidad-pv-portafolio-baseline-ingestion-and-extraction-audit`
- `movilidad-pv-structure-and-chunk-dedup-remediation`
- `movilidad-pv-applicability-collapse-and-inline-tail-remediation`
- `movilidad-pv-retrieval-readiness-audit`
- `movilidad-pv-duplicate-applicability-dedup-remediation`
- `embedding-runtime-readiness-validation`
- `movilidad-pv-embedding-and-indexing-execution`
- `movilidad-pv-query-intent-and-ranking-alignment`
- `movilidad-pv-document-family-ranking-alignment`
- `qdrant-document-name-filter-index-alignment`
- `movilidad-pv-benefit-breadth-and-duplicate-section-diversification`
- `movilidad-transversales-corpus-baseline-ingestion-and-retrieval`
- `muevete-libre-corpus-baseline-ingestion-and-retrieval`
- `soat-corpus-baseline-ingestion-and-retrieval`
- `soat-coverage-document-type-alignment`
- `soat-coverage-evidence-prioritization-alignment`

remaining in `Phase 18`:

- none

Implementation note:

- This phase now includes the smallest truthful retrieval-facing metadata
  filter surface for currently curated `document_type` and `product` values.
- Retrieval-time metadata filters also depend on Qdrant payload indexes for
  those curated fields, and collection bootstrap is now responsible for
  creating them when the client supports payload-index management.
- Retrieval-facing `document_name` promotion now rejects obviously noisy
  heading candidates such as media/embed labels with URLs and falls back to the
  deterministic source filename stem instead.
- Retrieval normalization can also carry narrow operator-curated comparison
  bundles when repeated AUTOS comparison queries need stronger lexical
  alignment with comparative documents.
- When those comparison bundles match, retrieval can use a larger candidate
  pool plus deterministic lexical reranking before returning the final top-k.
- Chunk text can now be prefixed with its governing `section_path` headings
  when overlap or fragmented layout would otherwise drop that context from the
  embedded text surface.
- Structured documents with many short adjacent fragments under one section can
  now be greedily aggregated into denser grouped blocks before chunk assembly.
- SOAT coverage-vs-tariff intent can now default retrieval toward the correct
  `document_type` surface, while preserving explicit caller-provided filters.
- When curated coverage terms exactly match a chunk `section` or one item in
  its `section_path`, deterministic reranking now gives that evidence a
  stronger boost than generic label/body matches.
- `MUEVETE LIBRE` now shares the baseline onboarding seam used by the other
  mobility products, including canonical product normalization,
  overlay-backed persisted metadata, and supported-scope admission.
- `MOVILIDAD/TRANSVERSALES` now uses the same overlay-backed baseline seam,
  but persists under shared `product=movilidad` rather than creating a new
  product taxonomy branch.
- `choque simple` now has a narrow supported-scope and retrieval seam over the
  shared mobility transversal corpus.
- `choque simple` circular evidence can now suppress header/footer boilerplate
  and expose stronger semantic section labels than the repeated
  `CIRCULAR EXTERNA` heading.
- `choque simple` retrieval now also enforces the normalized
  `product=movilidad` + `document_type=guide` scope through hybrid local
  lexical recall, preventing `auto`/`moto` policy chunks from leaking ahead of
  the transversal circular in live queries.
- The operator batch workflow can now target the remaining `choque simple`
  transversal PDFs as one cohort through committed raw/artifact glob controls,
  so ingestion, embeddings, and indexing can be completed before wider
  `TRANSVERSALES` onboarding.
- The `como tomar fotos choque simple` guide can now reject its noisy
  promotional heading as `document_name` and avoid duplicated leading section
  headings inside chunk text after section-path prefixing.
- The `PV` pair (`pv portafolio movilidad v2` + `pv planes movilidad v1`) has
  now completed baseline onboarding plus a first structure/dedup remediation:
  obvious benefit + `PLANES QUE APLICA` pairs can now be merged, and most
  standalone commercial slogan headings are suppressed before chunk
  persistence.
- The second `PV` remediation slice now also disables overlap rollover for pure
  applicability chunks and removes residual inline commercial tails from
  heading-prefixed applicability bodies.
- The duplicate-applicability remediation now removes the remaining exact
  standalone `PLANES QUE APLICA` duplicates from `pv portafolio movilidad v2`,
  reducing the cohort to `78` chunks with `0` duplicate chunk-text groups.
- The remaining blocker before `PV` indexing is runtime rather than corpus
  structure: local embedding generation still depends on successful model
  resolution/cache availability for
  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.
- The runtime-readiness slice now adds an explicit
  `warmup-embedding-assets` command and makes embedding generation fail fast
  with an actionable cache/warm-up message instead of spending time on vague
  network resolution failures.
- The next reasonable slice is therefore
  `movilidad-pv-embedding-and-indexing-execution`.
- The PV execution slice is now complete: the two
  `movilidad__transversales__pv-*` bundles are generated, indexed into Qdrant,
  and retrievable through the live CLI path.
- The next narrow PV correction therefore shifts from runtime to ranking:
  benefit-intent queries over `propuesta de valor movilidad` can now use a
  curated expansion bundle to bias retrieval toward sections such as `Viajes`
  and `Pérdidas totales` instead of weaker generic sections or adjacent
  mobility guides.
- The live validation of that ranking slice exposed one remaining scope gap:
  shared mobility guides can still enter through overlapping anchors, so the
  next correction constrains explicit PV benefit-intent queries to the
  `PROPUESTA DE VALOR MOVILIDAD` document family through the existing curated
  `document_name` filter seam.
- Live validation of that document-family slice then exposed the final runtime
  dependency: Qdrant collection bootstrap also needs to create a keyword
  payload index for `document_name`, otherwise the live collection rejects the
  new filter with `400 Bad Request`.
- With that runtime blocker removed, the remaining PV quality gap is now purely
  intra-family ranking: duplicate `Pérdidas totales` chunks should not consume
  multiple early slots, and broader benefit sections should outrank narrow
  service-detail sections such as isolated `Grúa de amplio alcance`.
- `MUEVETE LIBRE` coverage-intent retrieval can now bias toward policy
  `Cobertura` sections instead of adjacent generic sections when operators ask
  what the product covers.
- Coverage-intent reranking can also prefer breadth across distinct explicit
  coverage sections before repeating multiple chunks from the same section.
- When multiple chunks represent the same explicit coverage section, retrieval
  can now prefer the more descriptive chunk over reminder-style operational
  follow-up text.
- Broader taxonomy inference, automatic classification, and UI filter work
  remain intentionally out of scope.

---

# Phase 19 — Citation Readability and Operator Traceability

## Goal

Improve citation and documentary-basis readability for operators by exposing
truthful source-traceability fields that already exist in retrieval outputs.

## Deliverables

- clearer citation-level source traceability;
- documentary-basis entries that are easier to map back to the corpus tree;
- compatibility-safe response-contract enrichment for operator-facing review.

## Success Criteria

- citations become easier to trace back to the underlying raw document path;
- documentary-basis entries preserve readable source-location context without
  weakening current answer/citation contracts;
- the first readability improvement remains narrow and regression-tested.

## Narrow Slices

- `citation-relative-path-traceability`
- `citation-ui-relative-path-display`
- `documentary-basis-ui-display`
- `citation-and-basis-curated-metadata-display`
- `operator-evidence-summary-display`

Current implementation status:

completed:

- `citation-relative-path-traceability`
- `citation-ui-relative-path-display`
- `documentary-basis-ui-display`
- `citation-and-basis-curated-metadata-display`
- `operator-evidence-summary-display`

remaining in `Phase 19`:

- none

Implementation note:

- This phase should start by reusing existing retrieval metadata rather than
  inventing new taxonomy or display-label rules.
- `citation-ui-relative-path-display`, `documentary-basis-ui-display`,
  `citation-and-basis-curated-metadata-display`, and
  `operator-evidence-summary-display` should stay narrowly focused on the
  current Gradio rendering seams.
- Broader UI redesign, citation prettification heuristics, and operator
  navigation aids remain intentionally out of scope.

---

# Phase Ordering Rules

## Mandatory Ordering

Do NOT:

- build DSPy before evaluation exists;
- build agents before tools exist;
- build tools before retrieval exists;
- optimize prompts before baseline evaluation exists;
- add deployment complexity before local execution works;
- introduce complex orchestration before baseline observability exists.

---

# Implementation Strategy

## Prioritize Vertical Slices

Prefer:

```text
small working pipeline
→ test
→ evaluate
→ extend
Avoid:
building the entire architecture first
```
# Portfolio-Complete MVP Definition

The MVP is complete when:

- the advisor can ask questions;
- grounded answers are returned;
- citations work;
- LangGraph orchestration works;
- observability is usable;
- public demo deployment is stable and documented;
- the internal-production path remains architecturally viable.
- Phoenix traces work;
- MCP is demonstrable;
- DSPy optimization exists;
- the app is publicly deployed;
- evaluation metrics exist;
- Docker deployment is stable.
