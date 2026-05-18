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
- constitution docs;
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
