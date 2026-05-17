# Tech Stack

## Philosophy

The stack is intentionally optimized for:

- fast iteration;
- strong observability;
- production-oriented architecture;
- modularity;
- low operational complexity for MVP deployment.

The goal is not maximal complexity.
The goal is a clean, reliable, extensible AI Engineering system.

---

# Core Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Frontend | Gradio |
| API Layer | Optional FastAPI integration later |
| Orchestration | LangGraph |
| LLM Provider | Groq API |
| Initial Model | GPT-OSS-120B |
| Document Processing | Docling |
| Vector Database | Qdrant Cloud |
| Contracts | Pydantic v2 |
| Optimization | DSPy |
| MCP | MCP Server + Client |
| Observability | Phoenix |
| Testing | Pytest |
| Linting | Ruff |
| Containerization | Docker |
| MVP Deployment | Hugging Face Spaces |
| Production Deployment | Internal environment, defined later |
| Config Management | python-dotenv + Pydantic Settings |
| Logging | Structured logging |

---

# Why These Technologies

## Python

Python provides:

- mature AI ecosystem;
- LangGraph compatibility;
- DSPy support;
- MCP compatibility;
- strong tooling for RAG systems.

---

## Gradio

Chosen because:

- minimal frontend overhead;
- fast MVP iteration;
- native Hugging Face Spaces compatibility;
- sufficient for demo workflows.

Avoid building React or complex frontend infrastructure during MVP.

---

## LangGraph

Chosen because:

- explicit workflow control;
- state-machine architecture;
- predictable execution;
- better fit for insurance workflows than open-ended ReAct loops;
- supports multi-agent orchestration cleanly.

The project should avoid unconstrained autonomous agent loops.

---

## Groq API + GPT-OSS-120B

Chosen because:

- fast inference;
- simple integration;
- good performance/cost ratio for MVP;
- suitable for public demo environments.

The architecture must support provider abstraction.

Future support:

- OpenAI;
- Gemini;
- Ollama;
- llama-cpp;
- local Llama-compatible providers.

---

## Docling

Chosen because:

- high-quality PDF extraction;
- strong document structure preservation;
- suitable for policy documents;
- modern document-processing pipeline.

Document quality is critical for retrieval quality.

---

## Qdrant Cloud

Chosen because:

- production-oriented vector database;
- managed infrastructure;
- metadata filtering;
- strong Python integration;
- easier public demo deployment than local persistence.

Avoid local vector databases for public demo persistence.

---

## DSPy

Chosen because:

- programmatic optimization of prompts and pipelines;
- evaluation-driven improvement;
- valuable AI Engineering portfolio capability.

DSPy should optimize targeted components only.
Avoid premature optimization everywhere.

---

## MCP

Chosen because:

- emerging interoperability standard;
- valuable architecture skill demonstration;
- enables reusable tool exposure.

MCP should complement the architecture, not dominate it.

---

## Phoenix

Chosen because:

- LLM observability;
- tracing;
- retrieval inspection;
- latency analysis;
- cost monitoring;
- evaluation support.

Observability is mandatory for debugging and evaluation.

---

# Architecture Principles

## Explicit State

All shared workflow state should be typed and explicit.

Use:

- Pydantic models;
- typed contracts;
- structured tool IO.

Avoid hidden mutable state.

---

## Local Development Environment

All local development must use a Python virtual environment.

Recommended setup:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Modular Boundaries

The repository should preserve clear boundaries:

- rag/
- agents/
- contracts/
- evals/
- ops/
- mcp/

Avoid monolithic scripts.

---

## Cloud-First Demo

The MVP deployment prioritizes:

- reliability;
- simplicity;
- low deployment friction.

Therefore:

- use Groq cloud inference;
- use Qdrant Cloud;
- avoid heavy local models during public deployment.

Local models remain future-compatible through provider abstraction.

## Dual Deployment Modes

The project must distinguish between:

- public MVP demo deployment;
- internal production deployment.

For the MVP:

- optimize for safe public demonstration;
- deploy on Hugging Face Spaces;
- use sanitized, approved documents only;
- prefer managed services and simple operations.

For future production:

- support internal access controls;
- preserve auditability and observability;
- keep deployment targets replaceable behind explicit contracts.

---

## Evaluation-Driven Development

Features should be evaluated continuously.

Important metrics:

- groundedness;
- retrieval precision;
- retrieval recall;
- citation accuracy;
- latency;
- tool success rate.

Avoid subjective-only evaluation.

## Deployment Spine

Deployment readiness must be built incrementally rather than deferred to the
final deployment phase.

Required early operational capabilities:

- startup validation;
- structured logs with request correlation when applicable;
- health/readiness checks for hosted environments;
- explicit environment variable mapping;
- reproducible offline jobs for ingestion and indexing;
- hosted smoke tests before full public deployment.

---

# Coding Standards

## Required

- type hints everywhere;
- Pydantic contracts;
- modular functions;
- structured logging;
- explicit error handling;
- small diffs;
- testable components.

---

## Avoid

- massive utility files;
- hidden globals;
- speculative abstractions;
- unnecessary frameworks;
- giant orchestrator functions;
- long untyped dictionaries.

---

# Infrastructure Constraints

## Hugging Face Spaces Constraints

The deployment environment has limited resources.

Avoid:

- large local models;
- excessive memory usage;
- startup-time ingestion;
- unnecessary background workers.

Prefer:

- prebuilt indexes;
- lightweight containers;
- cloud inference.

---

# Future-Compatible Decisions

The architecture should remain compatible with:

- local model inference;
- enterprise authentication;
- multiple collections;
- production observability;
- multi-user workflows;
- advanced evaluation systems.

But these should not block MVP delivery.
