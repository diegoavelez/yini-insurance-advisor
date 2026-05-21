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

- measurable improvement exists;
- optimization process is documented;
- hosted latency remains within budget.

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
