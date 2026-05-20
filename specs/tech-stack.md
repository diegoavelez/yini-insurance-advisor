# Tech Stack

## Core Stack

| Layer               | Technology                        |
| ------------------- | --------------------------------- |
| Language            | Python 3.11+                      |
| Frontend            | Gradio                            |
| API Layer           | Optional FastAPI later            |
| Orchestration       | LangGraph                         |
| LLM Provider        | Groq API                          |
| Initial Model       | GPT-OSS-120B                      |
| Document Processing | Docling                           |
| Vector Database     | Qdrant Cloud                      |
| Contracts           | Pydantic v2                       |
| Optimization        | DSPy                              |
| MCP                 | MCP Server + Client               |
| Observability       | Phoenix                           |
| Testing             | Pytest                            |
| Linting             | Ruff                              |
| Containerization    | Docker                            |
| MVP Deployment      | Hugging Face Spaces               |
| Config              | python-dotenv + Pydantic Settings |
| Logging             | Structured logging                |

---

## Local Development

* Use Python virtual environment `.venv`.
* Never install dependencies globally.
* Use `requirements.txt` or `pyproject.toml` as dependency source of truth.
* Docker is for reproducibility and deployment, not the primary local dev loop.

---

## Architecture Rules

* Use explicit Pydantic contracts at system boundaries.
* Keep workflow state typed and explicit.
* Preserve modular boundaries:

  * `rag/`
  * `agents/`
  * `contracts/`
  * `data/eval/`
  * `ops/`
  * `mcp/`
* Avoid hidden mutable state.
* Avoid monolithic scripts.
* Avoid large untyped dictionaries.
* Avoid speculative abstractions.

---

## LLM Provider Rules

* Use Groq API with GPT-OSS-120B for the MVP.
* Keep provider access behind an explicit abstraction.
* Do not hardcode model names outside configuration.
* Future providers may include OpenAI, Gemini, Ollama, llama-cpp, or local Llama-compatible models.
* Do not run heavy local models in the public Hugging Face Spaces demo.

---

## RAG and Vector Store Rules

* Use Qdrant Cloud for MVP vector storage.
* Preserve metadata required for citations:

  * document name;
  * page;
  * section;
  * clause ID when available;
  * chunk ID.
* Retrieval quality is more important than model size.
* Avoid startup-time ingestion in hosted demo mode.

---

## Deployment Modes

The project must distinguish:

1. `public_mvp_demo`
2. `internal_production`

For `public_mvp_demo`:

* deploy on Hugging Face Spaces;
* use Docker;
* use approved documents only;
* prefer managed services;
* keep runtime lightweight.

For `internal_production`:

* preserve auditability;
* support future access controls;
* keep deployment targets replaceable behind contracts.

---

## Observability Rules

Use Phoenix for:

* latency;
* token usage;
* retrieval events;
* tool usage;
* errors;
* cost estimates;
* confidence scores.

Baseline observability must exist before complex orchestration grows further.

---

## Evaluation Rules

Track at minimum:

* groundedness;
* retrieval precision;
* retrieval recall;
* citation accuracy;
* latency;
* tool success rate.

Do not rely only on subjective manual inspection.

---

## Deployment Spine

Deployment readiness must be built incrementally.

Required:

* startup validation;
* explicit environment variable mapping;
* structured logs;
* request correlation when applicable;
* health/readiness checks;
* reproducible ingestion/indexing jobs;
* hosted smoke tests.

---

## Infrastructure Constraints

For Hugging Face Spaces, avoid:

* large local models;
* excessive memory use;
* startup-time ingestion;
* unnecessary background workers.

Prefer:

* lightweight containers;
* cloud inference;
* Qdrant Cloud;
* prebuilt or reproducible indexes.
