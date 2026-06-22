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

## Dated Slice Index

This list is a traceability index of dated slice slugs, not the preferred
operational view for category onboarding. Future category work should prefer
root-cause-sized bundles rather than query-sized micro-slices.

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
- `bicicletas-patinetas-coverage-policy-family-recovery`
- `viajes-coverage-section-priority-recovery`
- `utilitarios-pesados-policy-family-recovery`
- `choque-simple-intent-evidence-routing-recovery`
- `mvp-current-category-acceptance-matrix`
- `mvp-current-category-acceptance-smoke-automation`
- `rag-cli-command-adapter-and-request-lifecycle-seam-extraction`
- `roadmap-operational-rollup-status-sync`
- `docx-mvp-exclusion-policy`
- `phase-15-evaluation-report-baseline`
- `phase-15-dead-code-and-surface-cleanup`
- `phase-15-final-test-release-baseline`
- `eps-pac-asegurabilidad-policy-family-recovery`
- `soat-tariff-table-label-recovery`
- `eps-pac-60-mas-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-60-mas-policy-family-coverage-alignment`
- `eps-pac-formularios-y-gestion-basica-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-global-web-guides-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-long-instructivos-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-policy-family-coverage-alignment`
- `eps-pac-clausulado-tradicional-isolated-onboarding`
- `eps-pac-canales-transaccionales-isolated-onboarding`

Current implementation status:

Operational category rollup:

- metadata and retrieval foundations: completed
- AUTOS comparison hardening: completed
- BICICLETAS Y PATINETAS onboarding + retrieval hardening: completed
- MOTOS onboarding + comparison alignment: completed
- `choque simple` transversal onboarding + retrieval hardening: completed
- `movilidad-pv` onboarding + retrieval hardening: completed
- `UTILITARIO Y PESADOS` onboarding + guide-family alignment: completed
  (dedicated category)
- `movilidad-financiacion` onboarding + extraction/guide-family hardening:
  completed
- `movilidad-transversales` baseline onboarding: completed
- `MUEVETE LIBRE` onboarding + coverage hardening: completed
- `SOAT` onboarding + coverage alignment: completed
- `VIAJES` onboarding + baseline retrieval: completed
- `movilidad-suscripcion` onboarding + retrieval hardening: completed
- `EPS/PAC` follow-on cohort onboarding: completed (all PAC PDF cohorts onboarded; `.docx` Word forms are excluded from the MVP ingestion and answer surface)

Implementation note:

- This rollup is now synchronized with the later operational category posture
  already documented in the roadmap, so it should no longer be used to infer
  stale open work for `MUEVETE LIBRE` or `movilidad-suscripcion`.
- `.docx` Word forms are not a deferred MVP corpus feature; they are
  intentionally excluded from ingestion and from answer evidence/response
  outputs.
- the `Phase 15` evaluation-report deliverable now has a durable baseline
  artifact in `docs/evaluation-report.md`, summarizing the current
  deterministic evaluation surfaces and the committed MVP acceptance smoke
  coverage.
- the `Phase 15` dead-code cleanup deliverable is now satisfied by removing the
  empty `mcp/` placeholder package surface and retaining `core/mcp_*` as the
  only documented MCP implementation boundary.
- the `Phase 15` final-tests deliverable is now satisfied by the explicit
  deterministic MVP release gate `make test-release`, documented in
  `README.md` and `docs/evaluation-report.md` as the authoritative pre-release
  verification baseline for the current MVP surface.

Completed slice index:

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
- `phase-15-evaluation-report-baseline`
- `phase-15-dead-code-and-surface-cleanup`
- `phase-15-final-test-release-baseline`
- `eps-pac-60-mas-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-60-mas-policy-family-coverage-alignment`
- `eps-pac-formularios-y-gestion-basica-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-global-web-guides-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-long-instructivos-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-policy-family-coverage-alignment`
- `eps-pac-clausulado-tradicional-isolated-onboarding`
- `eps-pac-canales-transaccionales-isolated-onboarding`

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

## Dated Slice Index

This list is a traceability index of dated slice slugs, not the preferred
operational view for category onboarding. Future category work should prefer
root-cause-sized bundles rather than query-sized micro-slices.

- `docling-ingestion-startup-remediation`
- `docling-primary-local-ingestion-policy`
- `recursive-ingestion-and-path-derived-document-ids`
- `qdrant-point-id-normalization`
- `qdrant-retrieval-client-compatibility`
- `docling-timeout-pdfium-fallback-remediation`
- `roadmap-operational-rollup-status-sync`

Current implementation status:

Operational category rollup:

- metadata and retrieval foundations: completed
- AUTOS comparison hardening: completed
- BICICLETAS Y PATINETAS onboarding + retrieval hardening: completed
- MOTOS onboarding + comparison alignment: completed
- `choque simple` transversal onboarding + retrieval hardening: completed
- `movilidad-pv` onboarding + retrieval hardening: completed
- `UTILITARIO Y PESADOS` onboarding + guide-family alignment: completed
  (dedicated category)
- `movilidad-financiacion` onboarding + extraction/guide-family hardening:
  completed
- `movilidad-transversales` baseline onboarding: completed
- `VIAJES` onboarding + policy-variant disambiguation: completed
- `MUEVETE LIBRE` onboarding + coverage hardening: completed
- `SOAT` onboarding + coverage alignment: completed
- `movilidad-suscripcion` onboarding + retrieval hardening: completed
- `EPS/PAC` follow-on cohort onboarding: completed (all PAC PDF cohorts onboarded; `.docx` Word forms are excluded from the MVP ingestion and answer surface)

Completed slice index:

- `docling-ingestion-startup-remediation`
- `docling-primary-local-ingestion-policy`
- `recursive-ingestion-and-path-derived-document-ids`
- `qdrant-point-id-normalization`
- `qdrant-retrieval-client-compatibility`
- `docling-timeout-pdfium-fallback-remediation`
- `eps-pac-60-mas-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-60-mas-policy-family-coverage-alignment`
- `eps-pac-formularios-y-gestion-basica-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-global-web-guides-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-long-instructivos-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-policy-family-coverage-alignment`
- `eps-pac-clausulado-tradicional-isolated-onboarding`
- `eps-pac-canales-transaccionales-isolated-onboarding`

- remaining in `Phase 16`:

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

- remaining in `Phase 17`:

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

## Dated Slice Index

This list is a traceability index of dated slice slugs, not the preferred
operational view for category onboarding. Future category work should prefer
root-cause-sized bundles rather than query-sized micro-slices.

- `document-metadata-contract-baseline`
- `source-relative-path-through-retrieval-payloads`
- `unsupported-metadata-filter-guardrail`
- `operator-curated-document-metadata-overlays`
- `document-metadata-filter-enablement`
- `operator-curated-term-equivalence-normalization`
- `rag-lexical-normalization-seam-extraction`
- `rag-arl-remuneration-domain-seam-extraction`
- `rag-document-canonicalization-seam-extraction`
- `rag-qdrant-client-and-payload-seam-extraction`
- `rag-qdrant-indexing-runtime-seam-extraction`
- `rag-grounded-answer-assembly-and-guardrails-seam-extraction`
- `rag-answer-evidence-selection-domain-seam-extraction`
- `rag-local-hybrid-recall-and-query-normalization-seam-extraction`
- `rag-pdf-conversion-and-markdown-cleaning-seam-extraction`
- `ingestion-chunk-emission-and-artifact-skip-correctness-remediation`
- `rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction`
- `rag-manifest-recording-and-artifact-iteration-seam-extraction`
- `rag-batch-command-loop-and-failure-handling-seam-extraction`
- `rag-runtime-provider-and-warmup-seam-extraction`
- `rag-cli-command-adapter-and-request-lifecycle-seam-extraction`
- `qdrant-metadata-filter-index-alignment`
- `noisy-document-title-heading-guardrail`
- `autos-plan-comparison-retrieval-alignment`
- `autos-plan-comparison-reranking-or-evidence-bias`
- `section-context-prefixed-chunk-remediation`
- `autos-comparison-corpus-retrievability-remediation`
- `autos-comparison-table-normalization-remediation`
- `autos-comparison-hybrid-recall-remediation`
- `autos-comparison-primary-guide-ranking-recovery`
- `autos-basico-pt-evidence-family-alignment`
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
- `movilidad-utilitarios-pesados-corpus-baseline-ingestion-and-retrieval`
- `movilidad-utilitarios-pesados-guide-family-ranking-alignment`
- `movilidad-utilitarios-pesados-category-reclassification-remediation`
- `movilidad-financiacion-corpus-baseline-ingestion-and-retrieval`
- `movilidad-financiacion-extraction-readiness-remediation`
- `movilidad-financiacion-guide-family-ranking-alignment`
- `movilidad-financiacion-heading-stub-priority-recovery`
- `movilidad-transversales-corpus-baseline-ingestion-and-retrieval`
- `movilidad-viajes-corpus-baseline-ingestion-and-retrieval`
- `movilidad-viajes-international-policy-disambiguation-alignment`
- `movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval`
- `movilidad-suscripcion-section-structure-remediation`
- `movilidad-suscripcion-subsection-lineage-normalization`
- `movilidad-suscripcion-breadth-diversification`
- `movilidad-suscripcion-heading-stub-evidence-prioritization`
- `movilidad-suscripcion-collective-billing-intent-alignment`
- `movilidad-suscripcion-collective-billing-leading-chunk-prioritization`
- `movilidad-suscripcion-facturacion-por-asegurado-scope-and-retrieval-alignment`
- `movilidad-suscripcion-modalidad-de-facturacion-renovacion-intent-alignment`
- `movilidad-suscripcion-financing-evidence-precision`
- `movilidad-suscripcion-financiacion-individual-retrieval-recovery`
- `muevete-libre-corpus-baseline-ingestion-and-retrieval`
- `muevete-libre-coverage-breadth-evidence-balancing`
- `muevete-libre-intrasection-coverage-chunk-prioritization`
- `muevete-libre-coverage-retrieval-alignment`
- `muevete-libre-heading-hierarchy-normalization`
- `soat-corpus-baseline-ingestion-and-retrieval`
- `soat-coverage-document-type-alignment`
- `soat-coverage-evidence-prioritization-alignment`

Current implementation status:

Operational category rollup:

- metadata and retrieval foundations: completed
- AUTOS comparison hardening: completed
- BICICLETAS Y PATINETAS onboarding + retrieval hardening: completed
- MOTOS onboarding + comparison alignment: completed
- `choque simple` transversal onboarding + retrieval hardening: completed
- `movilidad-pv` onboarding + retrieval hardening: completed
- `UTILITARIO Y PESADOS` onboarding + guide-family alignment: completed
  (dedicated category)
- `movilidad-financiacion` onboarding + extraction/guide-family hardening:
  completed
- `movilidad-transversales` baseline onboarding: completed
- `movilidad-viajes` onboarding + policy disambiguation alignment: completed
- `movilidad-suscripcion` onboarding + retrieval hardening: completed
- `MUEVETE LIBRE` onboarding + coverage hardening: completed
- `SOAT` onboarding + coverage alignment: completed
- `EPS/PAC` follow-on cohort onboarding: completed (all PAC PDF cohorts onboarded; `.docx` Word forms are excluded from the MVP ingestion and answer surface)

Completed slice index:

- `document-metadata-contract-baseline`
- `source-relative-path-through-retrieval-payloads`
- `unsupported-metadata-filter-guardrail`
- `operator-curated-document-metadata-overlays`
- `document-metadata-filter-enablement`
- `operator-curated-term-equivalence-normalization`
- `rag-lexical-normalization-seam-extraction`
- `rag-arl-remuneration-domain-seam-extraction`
- `rag-document-canonicalization-seam-extraction`
- `qdrant-metadata-filter-index-alignment`
- `noisy-document-title-heading-guardrail`
- `autos-plan-comparison-retrieval-alignment`
- `autos-plan-comparison-reranking-or-evidence-bias`
- `section-context-prefixed-chunk-remediation`
- `autos-comparison-corpus-retrievability-remediation`
- `autos-comparison-table-normalization-remediation`
- `autos-comparison-hybrid-recall-remediation`
- `eps-pac-asegurabilidad-policy-family-recovery`
- `eps-pac-asegurabilidad-section-priority-recovery`
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
- `movilidad-utilitarios-pesados-corpus-baseline-ingestion-and-retrieval`
- `movilidad-utilitarios-pesados-guide-family-ranking-alignment`
- `movilidad-utilitarios-pesados-category-reclassification-remediation`
- `movilidad-financiacion-corpus-baseline-ingestion-and-retrieval`
- `movilidad-financiacion-extraction-readiness-remediation`
- `movilidad-financiacion-guide-family-ranking-alignment`
- `movilidad-transversales-corpus-baseline-ingestion-and-retrieval`
- `movilidad-viajes-corpus-baseline-ingestion-and-retrieval`
- `movilidad-viajes-international-policy-disambiguation-alignment`
- `movilidad-suscripcion-corpus-baseline-ingestion-and-retrieval`
- `movilidad-suscripcion-section-structure-remediation`
- `movilidad-suscripcion-subsection-lineage-normalization`
- `movilidad-suscripcion-breadth-diversification`
- `movilidad-suscripcion-heading-stub-evidence-prioritization`
- `movilidad-suscripcion-collective-billing-intent-alignment`
- `movilidad-suscripcion-collective-billing-leading-chunk-prioritization`
- `movilidad-suscripcion-facturacion-por-asegurado-scope-and-retrieval-alignment`
- `movilidad-suscripcion-modalidad-de-facturacion-renovacion-intent-alignment`
- `movilidad-suscripcion-financing-evidence-precision`
- `movilidad-suscripcion-financiacion-individual-retrieval-recovery`
- `muevete-libre-corpus-baseline-ingestion-and-retrieval`
- `muevete-libre-coverage-retrieval-alignment`
- `muevete-libre-coverage-breadth-evidence-balancing`
- `muevete-libre-intrasection-coverage-chunk-prioritization`
- `muevete-libre-heading-hierarchy-normalization`
- `soat-corpus-baseline-ingestion-and-retrieval`
- `soat-coverage-document-type-alignment`
- `soat-coverage-evidence-prioritization-alignment`
- `eps-pac-60-mas-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-60-mas-policy-family-coverage-alignment`
- `eps-pac-formularios-y-gestion-basica-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-global-web-guides-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-long-instructivos-corpus-baseline-ingestion-and-retrieval`
- `eps-pac-policy-family-coverage-alignment`
- `eps-pac-clausulado-tradicional-isolated-onboarding`
- `eps-pac-canales-transaccionales-isolated-onboarding`

- remaining in `Phase 18`:

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
- The shared lexical term-equivalence helpers now live behind a dedicated
  `rag/term_equivalences.py` seam, reducing further coupling growth inside
  `rag/ingestion.py` while additional categories continue onboarding.
- Additional `rag/ingestion.py` decoupling is still intentionally deferred
  until the current category-onboarding wave settles. The first documented
  post-onboarding refactor candidates now closed are:
  - `rag-arl-remuneration-domain-seam-extraction`, which moved the stabilized
    ARL remuneration-policy ranking and citation-compaction helpers behind a
    dedicated `rag` seam.
  - `rag-document-canonicalization-seam-extraction`, which moved document-name
    extraction, safe heading promotion, collision-safe `source_pdf_id`
    derivation, artifact-path construction, and overlay-first
    product/document-type resolution behind a dedicated `rag` seam.
  - `rag-markdown-chunk-normalization-seam-extraction`, which moved
    document-specific markdown cleanup, semantic block grouping, section-path
    prefixing, and overlap-disable heuristics behind a dedicated `rag` seam
    while keeping `rag.ingestion.py` as the orchestration layer.
  - `rag-qdrant-client-and-payload-seam-extraction`, which moved Qdrant
    point/payload mapping, retrieval-filter translation, source-document prune
    filters, and collection/payload-index bootstrap behind a dedicated `rag`
    seam while preserving the current indexing and retrieval contract.
  - `rag-qdrant-indexing-runtime-seam-extraction`, which moved the remaining
    Qdrant indexing retry/backoff, source-document prune execution, and
    post-index smoke validation helpers behind the same dedicated `rag` seam
    while preserving indexing manifest outcomes and idempotent reindexing
    behavior.
  - `rag-grounded-answer-assembly-and-guardrails-seam-extraction`, which moved
    grounded-answer prompt construction, citation/documentary-basis derivation,
    grounding verification, and conservative refusal/limited-response builders
    behind a dedicated `rag` seam while keeping answer orchestration in
    `rag.ingestion.py`.
  - `rag-answer-evidence-selection-domain-seam-extraction`, which moved the
    domain-specific candidate-pool sizing, reranking, evidence diversification,
    answer-evidence narrowing, and citation-evidence narrowing helpers behind a
    dedicated `rag` seam while preserving current retrieval and answer
    orchestration behavior.
  - `rag-local-hybrid-recall-and-query-normalization-seam-extraction`, which
    moved retrieval-query normalization with term equivalences, domain-specific
    hybrid recall term construction, local chunk filtering/scoring, and exact
    applicability deduplication behind a dedicated `rag` seam while keeping
    retrieval orchestration in `rag.ingestion.py`.
  - `rag-pdf-conversion-and-markdown-cleaning-seam-extraction`, which moved
    PDF-conversion backend checks, offline Hugging Face resolution,
    Docling/PDFium conversion routing, markdown-usability checks, and
    conservative markdown cleanup behind a dedicated `rag` seam while keeping
    ingestion orchestration in `rag.ingestion.py`.
  - `rag-ingestion-artifact-assembly-and-skip-policy-seam-extraction`, which
    moved chunk-record assembly, chunk/embedding bundle construction,
    persisted artifact-compatibility checks, and per-document artifact reuse
    policy behind a dedicated `rag` seam while keeping top-level ingestion
    and embedding command orchestration in `rag.ingestion.py`.
  - `rag-manifest-recording-and-artifact-iteration-seam-extraction`, which
    moved ingestion/embedding/indexing manifest-record builders, JSONL
    appenders, and deterministic source/chunk/embedding artifact iteration
    behind a dedicated `rag` seam while keeping batch command orchestration
    in `rag.ingestion.py`.
  - `rag-batch-command-loop-and-failure-handling-seam-extraction`, which
    moved the repeated ingestion/embedding/indexing batch loops, fail-fast
    branching, per-artifact exception recovery, and manifest-append
    orchestration behind a dedicated `rag` seam while keeping top-level CLI
    dispatch in `rag.ingestion.py`.
  - `rag-runtime-provider-and-warmup-seam-extraction`, which moved runtime
    backend availability checks, embedding/Qdrant/Groq provider bridges, Groq
    client and SentenceTransformer loading, offline asset-warmup helpers,
    embedding-vector and grounded-completion generation, and the closely
    related warmup command support surfaces behind a dedicated `rag` seam
    while keeping retrieval/answer orchestration and top-level CLI dispatch in
    `rag.ingestion.py`.
  - `rag-cli-command-adapter-and-request-lifecycle-seam-extraction`, which
    moved request-id-aware seam invocation, simple warmup/retrieval/answer
    command adapters, shared `RetrievalQuery` construction from CLI args, and
    top-level CLI request lifecycle logging/dispatch behind
    `rag/cli_runtime.py` while intentionally keeping parser definitions and
    lower-level runtime/retrieval helpers in `rag.ingestion.py`.
- No further post-onboarding CLI refactor candidate is promoted ahead of
  direct MVP blockers yet; parser definitions and lower-level helpers remain in
  `rag.ingestion.py` intentionally after this extraction.
- The manual `mvp-current-category-acceptance-matrix` execution focus is now
  closed: the currently onboarded corpus has live category-acceptance
  evidence, and `mvp-current-category-acceptance-smoke-automation` adds a
  committed smoke dataset plus deterministic local runner on top of that
  manual acceptance pass.
- The accepted category set is therefore no longer protected only by roadmap
  notes and manual reruns; it now also has a typed regression artifact in
  `data/eval/mvp-acceptance-smokes.json` and a deterministic runner in
  `core/evaluation_runner.py`.
- Remaining post-onboarding coupling slices can now resume without losing the
  current MVP acceptance posture, unless a new corpus wave or fresh live
  regression creates another direct MVP blocker.
- The first live P1 snapshot on 2026-06-15 established:
  - `ARL` = `pass`
  - `MOVILIDAD/MUEVETE LIBRE` = `pass`
  - `MOVILIDAD/SOAT` = `fragile-pass`
  - `MOVILIDAD/AUTOS` = `fail`
  - `EPS/PAC` = `fail`
- The narrow blocker `eps-pac-asegurabilidad-policy-family-recovery` is now
  closed at the document-family level:
  - `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` no longer routes to
    `clausulado pac 60 mas sura v1.pdf`;
  - live retrieval and grounded answering now stay inside
    `politicas asegurabilidad pac 60 mas.pdf`;
  - the PAC row therefore moved from `fail` to `fragile-pass`.
- The narrow blocker `eps-pac-asegurabilidad-section-priority-recovery` is now
  closed:
  - the explicit query `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?`
    now matches a committed PAC asegurabilidad expansion rule;
  - live retrieval now ranks the direct `EDADES Y REQUISITOS...` and
    `GRUPOS ASEGURABLES` sections ahead of operational sections such as
    `CONGELACIONES` and `REACTIVACIÓN`;
  - live grounded answering now cites the direct asegurabilidad sections
    prominently, so the `EPS/PAC` P1 row can move from `fragile-pass` to
    `pass`.
- Live MVP acceptance checks now also confirm the current `MOVILIDAD/MOTOS`
  row as `pass` without further corrective work:
  - `¿Qué diferencia hay entre los planes de motos?` ranks
    `comparativo motos.pdf` first;
  - `¿Qué cubre el plan de motos?` stays inside
    `clausulado-plan motos.pdf` with direct `PLAN MOTOS SURA` citations.
- The narrow blocker `autos-comparison-primary-guide-ranking-recovery` is now
  closed:
  - the broad query `¿Qué diferencia hay entre los planes de autos?` now
    matches a committed AUTOS comparison expansion rule;
  - live retrieval now ranks `diferenciales planes autos.pdf` first instead of
    electric/hybrid marketing evidence;
  - with `autos-basico-pt-evidence-family-alignment` already closed, the
    `MOVILIDAD/AUTOS` P1 row can move from `fail` to `pass`.
- The narrow blocker `autos-basico-pt-evidence-family-alignment` is now
  closed at the document-family level:
  - `¿Qué cubre el plan autos básico PT?` now injects the canonical
    `Plan Autos Básico Pérdidas Totales` guide-family filter;
  - a narrow coverage-oriented expansion rule now pulls the
    `Coberturas principales` table to the top of the candidate set;
  - live retrieval and grounded answering now stay inside
    `generalidades plan autos basico pt v2.pdf` while surfacing the explicit
    `Daños a terceros`, `Pérdida total daños`, and `Pérdida total hurto`
    coverage rows;
  - the remaining AUTOS MVP gap is therefore the broad comparison-ranking
    path, not the explicit `Básico PT` family routing path.
- The narrow blocker `soat-tariff-table-label-recovery` is now closed:
  - the SOAT tariff markdown is normalized into labeled tariff statements
    before chunk generation;
  - rebuilt SOAT tariff chunks now preserve vehicle-category labels such as
    `Motos`, `Autos familiares`, and `Vehículos de carga o mixto`;
  - live tariff retrieval and grounded answering now stay inside
    `tarifas soat 2026.pdf` while surfacing labeled tariff evidence.
- Remaining post-onboarding coupling slices are now intentionally deferred
  until the MVP acceptance pass for the current category set is complete,
  unless one of those slices becomes necessary to unblock a failing retrieval,
  grounded-answer, or deployment acceptance scenario directly.
- That MVP acceptance pass should cover the currently onboarded category set:
  - `ARL`
  - `MOVILIDAD/AUTOS`
  - `MOVILIDAD/BICICLETAS Y PATINETAS`
  - `MOVILIDAD/MOTOS`
  - `MOVILIDAD/TRANSVERSALES` including `choque simple`
  - `MOVILIDAD/PV`
  - `MOVILIDAD/UTILITARIO Y PESADOS`
  - `MOVILIDAD/FINANCIACION`
  - `MOVILIDAD/VIAJES`
  - `MOVILIDAD/SUSCRIPCION`
  - `MOVILIDAD/MUEVETE LIBRE`
  - `MOVILIDAD/SOAT`
- 2026-06-15: `MOVILIDAD/BICICLETAS Y PATINETAS` now passes its acceptance row
  after `bicicletas-patinetas-coverage-policy-family-recovery`; explicit
  coverage queries now stay inside `clausulado-bicis y patinetas.pdf`, and the
  deductible smoke query again ranks `pv bicis y patinetas v2.pdf` first after
  removing the over-broad `seguro` trigger from the coverage-only routing rule.
- 2026-06-20: hosted manual Space QA reopened the bicicletas/patinetas
  deductible query; the public UI path lacked local chunk-artifact support and
  drifted outside `pv bicis y patinetas v2.pdf`, so
  `hosted-manual-bicis-deductible-and-choque-procedure-retrieval-recovery`
  now adds a deterministic hosted-safe guide-family routing rule for the
  deductible intent before the row can be treated as stable again.
- 2026-06-15: `MOVILIDAD/VIAJES` now passes its acceptance row after
  `viajes-coverage-section-priority-recovery`; national and international
  coverage smokes stay inside their intended clausulado families and now
  prioritize `SECCIÓN I QUÉ CUBRE ESTE SEGURO` evidence instead of exclusions
  and operational sections.
- 2026-06-15: `MOVILIDAD/UTILITARIO Y PESADOS` now passes its acceptance row
  after `utilitarios-pesados-policy-family-recovery`; the guide smoke stays in
  `ayudaventas utilitarios y pesados v2.pdf`, and the policy smoke now cites
  `SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS` from
  `clausulado-plan utilitarios y pesados.pdf` instead of the transversal
  suscripción policy document.
- 2026-06-15: `MOVILIDAD/TRANSVERSALES / choque simple` now passes its
  acceptance row after `choque-simple-intent-evidence-routing-recovery`; photo
  intent now ranks `como tomar fotos choque simple v2.pdf` first, while
  procedure intent is anchored on `proceso atencion choque simple v2.pdf` with
  `circular choque simple.pdf` support instead of over-prioritizing the photo
  guide.
- 2026-06-20: hosted manual Space QA reopened the choque simple procedure
  query; the public UI path drifted back to the photo guide family, so
  `hosted-manual-bicis-deductible-and-choque-procedure-retrieval-recovery`
  now adds deterministic hosted-safe procedure-family routing to
  `EN EVENTOS DE CHOQUES` before the row can be treated as stable again.
- 2026-06-20: hosted manual Space QA also exposed a wide-table readability gap
  in the SOAT tariff response; `spaces-wide-table-scroll-and-readability` now
  scopes horizontal-scroll table styling to the public answer/documentary
  Markdown surfaces so numeric tariff cells remain readable without shrinking
  the font.
- 2026-06-15: `MOVILIDAD/PV` now passes its acceptance row; live retrieval for
  `¿Qué beneficios incluye la propuesta de valor de movilidad?` stayed fully
  inside the `PROPUESTA DE VALOR MOVILIDAD` evidence family, and the grounded
  answer cited both `pv planes movilidad v1.pdf` and
  `pv portafolio movilidad v2.pdf` with diverse benefit sections instead of
  repeated applicability-only chunks.
- 2026-06-15: `MOVILIDAD/FINANCIACION` now reaches `fragile-pass`; live
  retrieval and grounded answering stay inside
  `instructivo financiacion de polizas v1.pdf`, but the top retrieval result is
  still a heading-only chunk and some extracted text remains noisy enough to
  justify a follow-up extraction-quality slice instead of a clean `pass`.
- 2026-06-15: `MOVILIDAD/FINANCIACION` now passes its acceptance row after
  `movilidad-financiacion-heading-stub-priority-recovery`; live retrieval for
  `¿Cómo funciona la financiación de pólizas individuales?` now ranks the
  contentful `Paso a paso` chunk above the `Procedimientos:` stub, and the
  grounded answer stays inside `instructivo financiacion de polizas v1.pdf`
  with `confidence=high`.
- 2026-06-15: `MOVILIDAD/SUSCRIPCION` now passes its acceptance row; the
  billing-by-insured retrieval smoke ranks section `14.6.2` first from
  `politicas de suscripcion de movilidad.pdf`, and the broader suscripción
  answer stays fully inside that policy family with `confidence=high`.
- `EPS/PAC` PDF cohorts
- A category should not be treated as MVP-ready merely because ingestion
  completed; it should satisfy the operational acceptance gates already
  documented in `docs/category-onboarding-playbook.md`, including embeddings,
  Qdrant indexing, at least one real retrieval query, and at least one real
  grounded-answer query with intended evidence.
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
- `MOVILIDAD/TRANSVERSALES` now uses the same overlay-backed baseline seam for
  true shared mobility documents, while `UTILITARIO Y PESADOS` has been
  reclassified into its own dedicated category/product instead of remaining in
  the transversal branch.
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
- `UTILITARIO Y PESADOS` was initially onboarded as part of
  `MOVILIDAD/TRANSVERSALES`, but raw-path audit showed the corpus belongs to
  its own category folder and now persists under the dedicated canonical
  product `utilitarios y pesados`.
- Its guide-family leakage is still closed through the existing curated
  `document_name` filter seam, so explicit `utilitarios y pesados`
  benefit/assistance queries stay within
  `Seguro de Autos Utilitarios y Pesados` while the policy path remains
  unchanged.
- The next operational movilidad cohort after the `UTILITARIO Y PESADOS`
  reclassification is now `financiación`, starting with the single-document guide
  `instructivo financiacion de polizas v1.pdf` before broadening into
  `suscripción`.
- That financing baseline cohort has now completed ingestion, embeddings, and
  Qdrant indexing, but the current extraction surface collapsed to a one-token
  artifact (`sura`) and one meaningless chunk, so the next narrow slice is
  extraction readiness rather than retrieval-family alignment.
- That extraction-readiness slice is now closed: when initial Docling output is
  mostly image placeholders with too little text, ingestion retries Docling
  with full-page OCR, which recovered the financing guide into meaningful
  sections and retrieval-visible chunks.
- The remaining financing gap is now a narrow guide-family ranking issue:
  explicit financing queries can surface the financing guide, but `PV`
  financing mentions still outrank it unless the existing curated
  `document_name` filter seam is used.
- That financing guide-family ranking slice is now closed: explicit
  financing-guide queries are constrained to
  `Manual Procedimiento Financiacion de polizas individuales`, and live
  top-k retrieval no longer leaks `PV` financing mentions ahead of the guide.
- The remaining financing quality gap then narrowed to intra-family evidence
  ordering: the financing guide family was correct, but the heading-only
  `Procedimientos:` stub could still outrank richer procedural chunks such as
  `Paso a paso`.
- That financing heading-stub priority slice is now closed: explicit financing
  guide prompts now prefer contentful procedural chunks from
  `Manual Procedimiento Financiacion de polizas individuales`, so live top-k no
  longer starts with the heading-only stub.
- The next operational transversal cohort after financing remains
  `suscripción`, using `politicas de suscripcion de movilidad.pdf` before
  broadening into other shared mobility process materials.
- That suscripción baseline cohort is now operationally onboarded through
  ingestion, embeddings, and Qdrant indexing, using the existing PDFium
  fallback path after a lower operational Docling timeout for the 64-page
  source document.
- Live suscripción retrieval now stays inside the correct policy family, so
  there is no first-pass cross-document leakage issue.
- The remaining suscripción gap is intra-document structure quality: fallback
  chunks still surface as generic `Page N` sections with page boilerplate and
  weak residual fragments, so the next narrow slice is semantic
  section-structure remediation rather than document-family alignment.
- That suscripción section-structure slice is now closed: the cleaned markdown
  head starts from semantic policy sections, chunk metadata now reflects
  numbered policy headings instead of `Page N`, and live retrieval no longer
  returns page-label fragments.
- That suscripción heading-stub slice is now closed: broad policy retrieval
  can expand its candidate pool and prefer contentful policy evidence ahead of
  bare heading-only stubs from the same family.
- That suscripción breadth-diversification slice is now closed: broad policy
  retrieval no longer lets repeated `14.1` collective-policy chunks dominate
  the first results before other distinct policy sections appear.
- That suscripción subsection-lineage slice is now closed: the collective
  billing subtree under `14.6` now preserves normalized child lineage such as
  `14.6.1` and `14.6.2` in cleaned markdown, chunk metadata, and live
  retrieval results.
- That suscripción collective-billing intent slice is now closed: explicit
  billing prompts now rank `14.6.*` collective billing sections ahead of
  `13.11. Financiación de Pólizas Individuales`.
- That suscripción leading-chunk slice is now closed: explicit collective
  billing retrieval can recover the exact `14.6.2` subsection from local
  lexical recall and prefer the cleaner billing lead ahead of later fragmentary
  continuations from the same subsection.
- That suscripción `facturación por asegurado` slice is now closed: the
  deterministic supported-scope seam admits that query pattern, live retrieval
  now prioritizes the `14.6.2` chunk that contains the modality conditions,
  and live grounded answers no longer refuse the request for unsupported scope.
- That suscripción renewal billing-mode slice is now closed: renewal-specific
  collective billing queries foreground `14.6.2` collective-policy evidence
  ahead of individual payment-change rules, and live answers now lead with the
  correct collective-policy documentary basis.
- That suscripción `13.11` financing-individual slice is now closed: the
  normalization path no longer hijacks supported suscripción financing queries
  into the unrelated financing manual, live retrieval now restores direct
  `13.11. Financiación de Pólizas Individuales` evidence, and grounded answers
  lead with that subsection as their primary documentary basis.
- That suscripción financing-evidence precision slice is now closed: live
  financing-individual retrieval keeps `13.11` first, promotes the direct
  financing follow-on section `13.1.2` ahead of lateral collective-policy
  material such as `14.1`, and grounded answers now expose a financing-focused
  documentary basis and citation set when direct support is already sufficient.
- That transversal leading-preamble normalization slice is now closed: the two
  `choque simple` process guides no longer emit a leading chunk with
  `section = None`, `proceso atencion choque simple v2` now drops the noisy
  `Normatividad vigente` preamble in favor of a stable `EN EVENTOS DE CHOQUES`
  root heading, and `proceso recobro choque simple v2` now promotes a stable
  root heading so its opening advisory text no longer escapes semantic section
  lineage.
- `MUEVETE LIBRE` coverage-intent retrieval can now bias toward policy
  `Cobertura` sections instead of adjacent generic sections when operators ask
  what the product covers.
- Coverage-intent reranking can also prefer breadth across distinct explicit
  coverage sections before repeating multiple chunks from the same section.
- When multiple chunks represent the same explicit coverage section, retrieval
  can now prefer the more descriptive chunk over reminder-style operational
  follow-up text.
- The current four-document `ARL` cohort is now operationally live: existing
  embeddings have been indexed into Qdrant Cloud, representative `guide`,
  `faq`, and `policy` retrieval queries succeed under `product=arl`, and a
  representative `ARL/RUI` grounded answer completes successfully through
  Groq.
- That `arl-rui-faq-heading-and-citation-precision` slice is now closed: the
  RUI FAQ rewrites into numbered semantic question headings, the noisy
  Vimeo/portal/table interruption no longer survives as retrieval sections, the
  live normativity query now retrieves the exact question section first, and
  the live grounded answer now cites only that direct normativity chunk in its
  documentary basis and citation list.
- That `arl-comisiones-guide-ui-boilerplate-normalization` slice is now
  closed: the commissions guide no longer preserves `Capacidad ARL` or
  standalone `sura` UI leftovers in its only chunk, and live retrieval now
  returns the same guide first with a cleaner procedural surface.
- That `arl-comisiones-guide-family-answer-evidence-alignment` slice is now
  closed: explicit commissions-guide answers keep high confidence while
  narrowing their documentary basis and citations to only
  `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`
  when that guide already contains the full answer.
- That `arl-cuenta-bancaria-guide-family-answer-evidence-alignment` slice is
  now closed: explicit account-update guide answers keep high confidence while
  narrowing their documentary basis and citations to only
  `Actualización de cuenta bancaria para pago de comisiones ARL SURA` when that
  guide already contains the full answer.
- That `arl-remuneracion-policy-heading-dedup` slice is now closed: the
  remuneration-policy chunk surface no longer repeats known section headings
  such as `## Canales para la afiliación a ARL SURA`, `## Clientes nuevos
  (venta) para el Canal Externo`, or `## Por cambio de intermediario`, and the
  refreshed Qdrant retrieval surface stays operational with cleaner policy
  text.
- That `arl-remuneracion-policy-parent-child-heading-compaction` slice is now
  closed: heading-only overlap chunks are no longer emitted for the ARL
  remuneration policy, so the previous standalone `Clientes nuevos` scaffold no
  longer appears in the rebuilt bundle or in live retrieval for that section.
- That `arl-remuneracion-policy-intent-retrieval-alignment` slice is now
  closed: broad ARL remuneration-policy retrieval now surfaces explicit
  remuneration sections before introductory channel sections, both in focused
  tests and in live Qdrant retrieval for
  `¿Cuál es el esquema de remuneración del canal externo ARL?`.
- That `arl-remuneracion-policy-overview-vs-table-priority` slice is now
  closed: broad ARL remuneration queries now lead with the explanatory
  `Clientes nuevos (venta) para el Canal Externo` chunk, while explicit
  percentage/sector queries still lead with `Pago de comisiones por
  Atracción`.
- That `arl-remuneracion-policy-broad-answer-citation-compaction` slice is now
  closed: broad ARL remuneration answers keep `confidence=high` while
  compacting documentary basis and citations to the direct overview, appetite,
  table, and change-of-intermediary support chunks, excluding lateral policy
  designación sections in focused tests and live `answer-query` validation.
- The ARL folder is now operationally corrected for the current MVP scope:
  representative `retrieve-chunks` and `answer-query` flows succeed for the
  FAQ, both guides, and the remuneration policy with the intended evidence
  ordering.
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

- remaining in `Phase 19`:

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

# Post-Completion Follow-On Work

All roadmap phases through `Phase 19` are complete. The next approved work, if
it remains inside the current MVP boundary rather than expanding scope, should
start from:

- `mvp-go-live-operational-baseline`

That follow-on slice should consolidate the current deterministic release gate,
hosted smoke checks, rollback posture, and corpus-update/operator baseline into
one explicit MVP go-live surface.

Current status:

- `mvp-go-live-operational-baseline` is now complete through
  `docs/mvp-go-live.md`, which consolidates the release gate, hosted smoke,
  rollback posture, corpus-update workflow, and shipped supported-category set
  for the current MVP.
- `spaces-citation-accordion-and-wide-table-usability` is now complete:
  - the public Gradio UI now keeps `Respuesta sugerida` as the primary visible
    answer surface while moving `Citas clave` into a compact collapsed
    accordion directly below it;
  - hosted answer/evidence tables now expose a stronger horizontal-scroll
    affordance with reserved scrollbar gutter space where supported and a
    sticky first column, preserving readability without shrinking the font;
  - the slice stays UI-only and preserves the current backend response
    contracts.

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
