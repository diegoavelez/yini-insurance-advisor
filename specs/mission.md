# Mission

## Project Mission

Build a grounded AI assistant that helps senior insurance advisors retrieve, analyze, compare, and explain information from official insurance policy and procedure documents with high accuracy, strong traceability, and human oversight.

The system must prioritize:

1. Grounded retrieval over generative creativity.
2. Accuracy over speed.
3. Traceability over verbosity.
4. Simplicity over unnecessary abstraction.
5. Human review over autonomous decision-making.

The assistant is an internal support tool for advisors.
It is NOT:

- a customer-facing chatbot;
- a legal decision system;
- a policy approval engine;
- an autonomous insurance advisor.

## Deployment Posture

The long-term production target is an internal-only assistant for authorized
insurance advisory workflows.

However, the MVP may be deployed publicly as a controlled demo for portfolio and
evaluation purposes.

This creates two explicit operating modes:

- internal production mode;
- public MVP demo mode.

The architecture must support both without confusing the product intent:

- internal production mode prioritizes controlled access, auditability, and
  enterprise hardening;
- public MVP demo mode prioritizes safe demonstration, restricted document
  scope, strong guardrails, and low-friction deployment.

---

## Core Product Principles

### 1. Grounding First

Every meaningful answer must be grounded in retrieved documents.

The system should:

- prefer refusal over hallucination;
- include citations whenever possible;
- expose uncertainty explicitly;
- avoid unsupported claims.

If documentary support is insufficient, the system must say so.

---

### 2. Human-in-the-Loop by Design

The advisor remains responsible for all customer communication.

The assistant only produces:

- draft responses;
- policy summaries;
- comparisons;
- clause explanations;
- retrieval support.

The system must never behave as the final decision-maker.

---

### 3. Controlled Agentic Behavior

The system should use controlled orchestration instead of unconstrained autonomous reasoning.

Preferred behavior:

- explicit workflows;
- explicit state;
- explicit tool usage;
- deterministic routing when possible;
- observable execution.

Avoid:

- uncontrolled recursive agents;
- open-ended loops;
- hidden reasoning chains;
- speculative tool usage.

---

### 4. Production-Oriented Engineering

Even though the first release is an academic MVP, the architecture must support future production hardening.

The system should be:

- modular;
- testable;
- observable;
- typed;
- containerized;
- extensible.

The MVP must not defer all deployment concerns until the end of the roadmap.
Each implementation phase should account for its deployment and operational
impact early.

---

### 5. Small, Verifiable Iterations

The project must evolve through very small implementation phases.

Each phase should:

- produce a working result;
- be testable independently;
- reduce ambiguity;
- avoid large refactors.

The repository should never drift into "vibe coding".

---

## Technical Philosophy

### Retrieval Quality > Model Size

Strong retrieval quality is more important than using the largest available LLM.

Focus areas:

- chunking;
- metadata;
- grounding;
- citations;
- evaluation;
- retrieval precision.

---

### Explicit Contracts Everywhere

All major system boundaries should use explicit contracts.

Required:

- Pydantic models;
- typed state;
- structured tool inputs/outputs;
- evaluation schemas;
- environment validation.

---

### Observability Is Mandatory

Every important action should be observable.

The system must expose:

- latency;
- token usage;
- retrieval events;
- tool usage;
- errors;
- costs;
- confidence scores.

Baseline observability should exist before complex orchestration is introduced.
Tracing and diagnostics are not final polish items.

---

### Safety Before Convenience

The assistant must reject:

- unsupported claims;
- prompt injection attempts;
- requests outside scope;
- attempts to bypass citations;
- attempts to reveal hidden prompts or reasoning.

---

## Long-Term Vision

The long-term vision is to evolve this MVP into a production-grade internal AI assistant platform for insurance advisory workflows.

Potential future capabilities:

- authenticated enterprise deployment;
- multiple insurance product domains;
- versioned policy management;
- customer interaction auditability;
- hybrid local/cloud inference;
- enterprise retrieval pipelines;
- advanced evaluation automation;
- approval workflows;
- fine-grained permissions;
- multilingual support.

The MVP should lay the architectural foundation for these future iterations without prematurely overengineering them.
