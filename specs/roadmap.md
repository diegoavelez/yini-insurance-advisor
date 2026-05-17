# Roadmap

## Philosophy

The roadmap is intentionally split into very small implementation phases.

Each phase should:

- produce a working artifact;
- reduce ambiguity;
- be independently testable;
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

## Success Criteria

- repository runs locally;
- linting works;
- tests execute;
- Docker builds successfully.

---

# Phase 1 — Configuration and Contracts

## Goal

Create typed configuration and shared contracts.

## Deliverables

- Pydantic settings;
- environment validation;
- shared schemas;
- retrieval contracts;
- tool contracts;
- response contracts;
- workflow state contract.

## Success Criteria

- app loads config safely;
- invalid environment values fail loudly;
- contracts are reusable across modules.

---

# Phase 2 — PDF Processing Pipeline

## Goal

Convert PDFs into clean Markdown.

## Deliverables

- Docling integration;
- PDF ingestion pipeline;
- Markdown export;
- cleaning pipeline;
- metadata extraction.

## Success Criteria

- PDFs convert reliably;
- Markdown preserves useful structure;
- processed documents are stored consistently.

---

# Phase 3 — Semantic Chunking

## Goal

Create retrieval-ready chunks.

## Deliverables

- chunking module;
- configurable chunk size/overlap;
- metadata propagation;
- chunk persistence.

## Success Criteria

- chunks preserve semantic meaning;
- clauses are not arbitrarily split;
- metadata remains traceable.

---

# Phase 4 — Embeddings and Vector Store

## Goal

Index chunks into Qdrant Cloud.

## Deliverables

- embedding pipeline;
- Qdrant integration;
- collection setup;
- indexing workflow;
- retrieval smoke tests.

## Success Criteria

- chunks are searchable;
- metadata filters work;
- retrieval returns meaningful results.

---

# Phase 5 — Basic RAG MVP

## Goal

Create the first grounded QA system.

## Deliverables

- retrieval pipeline;
- grounded answer generation;
- citations;
- simple Gradio query interface.

## Success Criteria

- advisor can ask questions;
- system returns grounded answers;
- citations appear consistently.

---

# Phase 6 — Core Tooling

## Goal

Implement reusable tools.

## Deliverables

- document_retrieval_tool;
- clause_extraction_tool;
- policy_comparison_tool;
- citation_verifier_tool;
- response_draft_tool.

## Success Criteria

- tools are independently callable;
- contracts are typed;
- outputs are structured.

---

# Phase 7 — LangGraph Workflow

## Goal

Replace basic RAG with controlled multi-agent orchestration.

## Deliverables

- LangGraph setup;
- shared workflow state;
- Planner Agent;
- Retriever Agent;
- Policy Analyst Agent;
- Citation Verifier;
- Response Formatter Agent.

## Success Criteria

- workflow executes end-to-end;
- state transitions are observable;
- fallbacks work.

---

# Phase 8 — Guardrails

## Goal

Add safety and scope protections.

## Deliverables

- prompt injection detection;
- scope validation;
- refusal behavior;
- confidence scoring;
- mandatory citation enforcement.

## Success Criteria

- unsupported queries are rejected safely;
- hallucinated answers decrease;
- confidence signals appear consistently.

---

# Phase 9 — Observability

## Goal

Instrument the system with Phoenix.

## Deliverables

- Phoenix setup;
- trace instrumentation;
- retrieval traces;
- tool traces;
- latency tracking;
- token usage tracking;
- cost estimation.

## Success Criteria

- traces are visible;
- workflow debugging improves;
- performance bottlenecks are measurable.

---

# Phase 10 — Evaluation Dataset

## Goal

Create a repeatable evaluation baseline.

## Deliverables

- 30 curated evaluation questions;
- evaluation schemas;
- golden dataset;
- evaluation runner.

## Success Criteria

- evaluation can run automatically;
- results are reproducible;
- retrieval quality can be measured.

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
- before/after comparison.

## Success Criteria

- measurable improvement exists;
- optimization process is documented.

---

# Phase 12 — MCP Integration

## Goal

Expose tools through MCP.

## Deliverables

- MCP server;
- MCP client;
- tool exposure;
- MCP tests.

## Success Criteria

- tools are callable through MCP;
- contracts remain stable.

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
- error states.

## Success Criteria

- demo is understandable;
- outputs are easy to review;
- failures are visible.

---

# Phase 14 — Docker and Deployment

## Goal

Deploy the MVP publicly.

## Deliverables

- production-ready Dockerfile;
- Hugging Face Spaces deployment;
- environment setup;
- deployment documentation.

## Success Criteria

- app deploys successfully;
- public demo is accessible;
- startup is stable.

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
- final tests.

## Success Criteria

- repository is understandable;
- demo is stable;

---

# Phase Ordering Rules

## Mandatory Ordering

Do NOT:

- build DSPy before evaluation exists;
- build agents before tools exist;
- build tools before retrieval exists;
- optimize prompts before baseline evaluation exists;
- add deployment complexity before local execution works.

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
# MVP Completion Definition

The MVP is complete when:

- the advisor can ask questions;
- grounded answers are returned;
- citations work;
- LangGraph orchestration works;
- Phoenix traces work;
- MCP is demonstrable;
- DSPy optimization exists;
- the app is publicly deployed;
- evaluation metrics exist;
- Docker deployment is stable.