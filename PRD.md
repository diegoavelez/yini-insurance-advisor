# PRD — AI Insurance Advisor Support Agent

## 1. Product Overview

### 1.1 Product Name

**Yini - AI Insurance Advisor Support Agent**

Alternative working name:

**Grounded Insurance Policy Assistant**

---

### 1.2 Product Summary

Yini - The AI Insurance Advisor Support Agent - is an internal assistant designed to help a senior insurance advisor quickly retrieve, analyze, compare, and summarize information from official Sura insurance policy and procedure documents.

The system enables the advisor to ask natural-language questions about policy clauses, coverages, exclusions, restrictions, procedures, and requirements. It uses Retrieval-Augmented Generation (RAG), tool-based agent orchestration, multi-agent workflows, structured outputs, citation verification, evaluation pipelines, observability, and a human-in-the-loop review model.

The assistant does **not** interact directly with clients. It only supports the advisor, who remains responsible for reviewing, validating, editing, and communicating any answer to the final customer.

---

### 1.3 Business Context

Insurance advisors often need to answer customer questions based on detailed policy documents, clauses, exclusions, restrictions, and internal procedures. These answers may be available in official documentation, but manually reviewing long documents slows down the advisory process and increases the risk of incomplete or imprecise responses.

The core business problem is not the absence of information. The problem is the time and cognitive effort required to retrieve the correct clause, interpret it accurately, and structure a useful response with documentary support.

This project addresses that gap by creating an AI-powered internal support tool that retrieves grounded information from official documents and generates structured, cited, advisor-ready draft responses.

---

### 1.4 Problem Statement

A senior insurance advisor cannot always respond quickly to customer questions because the relevant answer may be buried inside official policy clauses, coverage conditions, exclusions, and procedure documents. The advisor must manually inspect documents before producing a reliable response.

This creates:

- slower response times;
- higher cognitive load;
- risk of missing relevant clauses;
- risk of incomplete explanations;
- inconsistent answer structure;
- dependency on manual document review.

The system must reduce search and analysis time while preserving accuracy, grounding, traceability, and human responsibility.

---

### 1.5 Product Goal

Build a public MVP demo, deployable with Docker on Hugging Face Spaces, that allows a senior insurance advisor to query official Sura PDF documents converted to Markdown, retrieve relevant clauses using RAG, extract and compare policy information, verify citations, and generate a structured response for human review.

The project must demonstrate professional AI Engineering capabilities, including RAG, agentic workflows, multi-agent orchestration, MCP integration, DSPy optimization, observability, guardrails, evaluation, Docker deployment, and clean software architecture.

---

## 2. Objectives and Success Criteria

### 2.1 Primary Objectives

1. Allow natural-language queries over official insurance documents.
2. Ingest PDF documents and convert them into structured Markdown using Docling.
3. Build a RAG pipeline with chunking, embeddings, Qdrant Cloud, and grounded generation.
4. Extract key clauses, exclusions, restrictions, coverages, procedures, and requirements.
5. Compare coverages or clauses across documents when requested.
6. Generate structured advisor-ready draft responses.
7. Include exact source citations whenever possible.
8. Use a controlled multi-agent workflow implemented with LangGraph.
9. Expose selected tools through an MCP server and consume them through an MCP client.
10. Use DSPy to optimize prompts or retrieval/generation components.
11. Include a human-in-the-loop model where the advisor validates all answers.
12. Instrument observability with Phoenix for latency, token usage, tool usage, and costs.
13. Implement guardrails against prompt injection, unsupported answers, and out-of-scope queries.
14. Create an evaluation dataset with 30 curated questions.
15. Deploy the MVP as a public demo on Hugging Face Spaces using Docker.

---

### 2.2 Success Criteria

The MVP will be considered successful if:

- The advisor can ask questions in Spanish through a Gradio interface.
- The system retrieves relevant chunks from Qdrant Cloud.
- Responses are grounded in official documents.
- Answers include citations with document name, section, page, and clause when available.
- The system supports policy summaries, coverage comparisons, exclusion explanations, procedure lookup, and advisor-ready draft generation.
- The system refuses or limits responses when documentary support is insufficient.
- The multi-agent workflow executes with traceable state transitions.
- At least two external tools are available to the agent; the target MVP implements five core tools.
- MCP is implemented for tool exposure and consumption.
- DSPy is used to optimize at least one retrieval or generation component.
- Phoenix captures traces for latency, tokens, costs, retrieval events, and tool usage.
- A 30-question evaluation dataset exists.
- Evaluation metrics are computed and documented.
- Docker build works locally.
- The demo is publicly accessible through Hugging Face Spaces.
- The repository includes clear documentation, setup instructions, architecture notes, and usage examples.

---

## 3. Users and Personas

### 3.1 Primary User

#### Senior Insurance Advisor

The primary user is a senior insurance advisor who needs to answer customer questions about policy clauses, coverages, exclusions, conditions, restrictions, and procedures.

The advisor needs to:

- ask questions in natural language;
- retrieve the relevant official policy information;
- understand the source clause quickly;
- compare policy terms when needed;
- generate a clear response draft;
- validate the answer before communicating it to the client.

---

### 3.2 Secondary Users — Future Iterations

Future versions may support:

- junior advisors;
- commercial insurance teams;
- back-office teams;
- product teams;
- training teams;
- internal customer support teams.

These personas are out of scope for the MVP.

---

## 4. Scope

### 4.1 In Scope

The MVP includes:

- ingestion of approximately 20 official PDF documents;
- PDF-to-Markdown conversion using Docling;
- document cleaning and normalization;
- semantic chunking;
- metadata extraction;
- embeddings generation;
- Qdrant Cloud vector storage;
- semantic retrieval;
- grounded answer generation;
- clause extraction;
- coverage and policy comparison;
- citation verification;
- structured advisor response drafting;
- LangGraph-based multi-agent orchestration;
- summarized reasoning trace;
- human-in-the-loop review model;
- MCP server and MCP client integration;
- DSPy optimization for selected prompt/retrieval components;
- Phoenix observability;
- prompt injection guardrails;
- input validation;
- usage limits;
- 30-question evaluation dataset;
- automated and manual evaluation;
- Docker deployment;
- public Hugging Face Spaces demo;
- README and project documentation.

---

### 4.2 Out of Scope

The MVP does not include:

- direct customer-facing chatbot behavior;
- policy approval;
- document modification;
- final legal or contractual interpretation;
- integration with Sura production systems;
- customer databases;
- personally identifiable information processing;
- health records or sensitive customer data;
- CRM integration;
- WhatsApp or omnichannel integration;
- premium calculation;
- real policy issuance;
- production-grade enterprise authentication;
- production-grade access control;
- automatic client communication;
- automatic sales recommendations.

---

## 5. Product Constraints

### 5.1 Domain Constraints

The system operates in a high-stakes insurance advisory context. It must prioritize:

- accuracy;
- grounding;
- traceability;
- source citations;
- compliance;
- refusal when information is insufficient.

The assistant must not invent interpretations or make claims that are not explicitly supported by the retrieved documents.

---

### 5.2 Human-in-the-Loop Constraint

The advisor is always in the loop.

The system generates internal draft responses only. The advisor must validate, edit, accept, or discard any generated answer before communicating with the customer.

---

### 5.3 Public Demo Constraint

The MVP will be publicly accessible as a bootcamp final project demo. Since real documents will be used, the project must avoid exposing confidential, personal, or sensitive customer information.

Only official documents approved for this demo should be included.

---

## 6. Functional Requirements

### FR-001 — PDF Document Ingestion

The system must ingest official PDF documents and convert them into Markdown using Docling.

#### Acceptance Criteria

- The system processes an initial set of approximately 20 PDF documents.
- Each PDF is converted into Markdown.
- The conversion preserves useful structure when possible, including headings, sections, tables, lists, clause numbers, and reading order.
- Converted Markdown files are stored under `data/markdown/`.
- Raw PDFs are stored under `data/raw/`.
- Processing logs are captured.
- Failed conversions are reported explicitly.

---

### FR-002 — Document Cleaning and Normalization

The system must clean and normalize Markdown files before chunking.

#### Acceptance Criteria

- Repeated headers and footers are removed when possible.
- Empty sections are removed.
- Formatting artifacts are reduced.
- Tables are preserved as Markdown when possible.
- Each processed document keeps a reference to its original PDF.
- Cleaned documents are stored under `data/processed/`.

---

### FR-003 — Semantic Chunking

The system must split documents into semantically meaningful chunks suitable for retrieval.

#### Acceptance Criteria

- Chunks should avoid splitting clauses in ways that destroy meaning.
- Chunk size and overlap are configurable.
- Chunk metadata includes:
  - document name;
  - document type;
  - page number when available;
  - section;
  - clause ID when available;
  - version when available;
  - source file path;
  - chunk ID.
- Chunking strategy is documented.

---

### FR-004 — Embeddings Generation

The system must generate embeddings for all chunks.

#### Acceptance Criteria

- Every indexed chunk has an embedding vector.
- Embedding provider is configurable.
- Embedding failures are logged.
- Embedding generation can be rerun safely.
- The system prevents duplicate indexing when possible.

---

### FR-005 — Qdrant Cloud Vector Store

The system must store document embeddings and metadata in Qdrant Cloud.

#### Acceptance Criteria

- The system connects to Qdrant Cloud using environment variables.
- Collections are created or reused safely.
- Points include vectors and metadata payloads.
- Retrieval supports semantic search.
- Retrieval supports metadata filters when available.
- The system documents how to configure Qdrant Cloud credentials.

---

### FR-006 — Natural Language Query Interface

The system must allow the advisor to ask questions in Spanish through a Gradio interface.

#### Acceptance Criteria

- The advisor can submit a natural-language query.
- The interface returns a structured answer.
- The interface displays source citations.
- The interface displays confidence level.
- The interface displays summarized trace information.
- The interface does not expose full chain-of-thought.

---

### FR-007 — Document Retrieval Tool

The system must provide a retrieval tool that searches Qdrant Cloud for relevant chunks.

#### Input Contract

```json
{
  "query": "string",
  "top_k": 5,
  "filters": {
    "document_type": "optional",
    "product": "optional",
    "document_name": "optional",
    "version": "optional"
  }
}
```

#### Output Contract

```json
{
  "chunks": [
    {
      "chunk_id": "string",
      "text": "string",
      "document_name": "string",
      "page": "integer | null",
      "section": "string | null",
      "clause_id": "string | null",
      "score": "float"
    }
  ]
}
```

#### Acceptance Criteria

- The tool returns relevant chunks with metadata.
- The tool supports configurable `top_k`.
- The tool returns retrieval scores.
- The tool logs retrieval events to Phoenix.
- The tool handles empty results gracefully.

---

### FR-008 — Clause Extraction Tool

The system must extract clauses, exclusions, restrictions, requirements, procedures, and exceptions from retrieved context.

#### Acceptance Criteria

- The tool identifies relevant clauses from retrieved chunks.
- Each extracted item is classified as one of:
  - coverage;
  - exclusion;
  - restriction;
  - requirement;
  - procedure;
  - exception.
- Each extracted item includes a summary and source metadata.
- The tool must not extract information not present in the retrieved context.

---

### FR-009 — Policy Comparison Tool

The system must compare coverages, exclusions, procedures, or clauses across documents when the query requires it.

#### Acceptance Criteria

- The tool compares two or more retrieved contexts.
- Differences are organized by comparison criteria.
- Each comparison point includes source references.
- The tool indicates when there is insufficient information to compare.
- The result is structured and easy for the advisor to review.

---

### FR-010 — Citation Verifier Tool

The system must verify whether the generated draft answer is supported by retrieved sources.

#### Acceptance Criteria

- The tool checks whether relevant claims are grounded in retrieved chunks.
- The tool identifies unsupported claims.
- The tool identifies missing citations.
- The tool assigns a confidence level:
  - high;
  - medium;
  - low.
- The system must block or downgrade answers with poor grounding.

---

### FR-011 — Response Draft Tool

The system must generate a structured response draft for the advisor.

#### Acceptance Criteria

The response must include:

- suggested answer;
- documentary basis;
- exact citations when available;
- confidence level;
- limitations;
- advisor review disclaimer.

#### Response Format

```md
## Suggested Answer

...

## Documentary Basis

- Document:
- Page:
- Section:
- Clause:

## Confidence Level

High / Medium / Low

## Limitations

...

## Advisor Review Notice

This response is a draft for advisor review. It must be validated before being communicated to a customer.
```

---

### FR-012 — MCP Tool Exposure

The system must expose selected tools through an MCP server and consume them through an MCP client.

#### Initial MCP Tools

The MVP should expose at least:

1. `document_retrieval_tool`
2. `clause_extraction_tool`

Optional MCP exposure for MVP:

3. `policy_comparison_tool`
4. `citation_verifier_tool`
5. `response_draft_tool`

#### Acceptance Criteria

- MCP server starts successfully.
- MCP client can call exposed tools.
- Tool contracts are documented.
- Tool errors are handled and logged.
- MCP implementation is optional in the runtime path if deployment constraints require a simpler demo path, but the MCP integration must be demonstrable in the repository.

---

### FR-013 — DSPy Optimization

The system must use DSPy to optimize at least one prompt or retrieval/generation component.

#### Recommended MVP Target

Use DSPy to optimize one of:

- query rewriting for retrieval;
- answer generation signature;
- citation-aware response drafting;
- classification of query type.

#### Acceptance Criteria

- A DSPy module is implemented.
- A training/evaluation subset from the 30-question dataset is used.
- A metric is defined.
- Before/after performance is documented.
- The optimized component can be used in the pipeline or reported as an experiment.

---

### FR-014 — Summarized Reasoning Trace

The system must provide a summarized reasoning trace without exposing full chain-of-thought.

#### Acceptance Criteria

The visible trace may include:

- detected intent;
- tools used;
- retrieved documents;
- confidence level;
- grounding verification result;
- limitations;
- fallback behavior.

The system must not expose full private chain-of-thought.

---

## 7. Multi-Agent Orchestration

### 7.1 Required Pattern

The system must use LangGraph to implement a controlled state-machine workflow instead of a fully open-ended ReAct loop.

### 7.2 Required Workflow

```text
User Query
   ↓
Input Guardrail
   ↓
Planner Agent
   ↓
Retriever Agent
   ↓
Policy Analyst Agent
   ↓
Citation Verifier
   ↓
Response Formatter Agent
   ↓
Advisor Review
```

---

### 7.3 Agent Roles

#### Planner Agent

Responsibilities:

- classify query intent;
- decide required tools;
- detect out-of-scope requests;
- define search strategy;
- route the workflow.

The Planner Agent must not generate the final answer.

---

#### Retriever Agent

Responsibilities:

- call the retrieval tool;
- retrieve relevant chunks;
- apply filters when available;
- return metadata-rich results;
- handle empty retrievals.

---

#### Policy Analyst Agent

Responsibilities:

- analyze retrieved clauses;
- extract relevant restrictions, coverages, exclusions, procedures, and requirements;
- perform policy comparisons when requested;
- identify missing or insufficient evidence.

---

#### Citation Verifier

Responsibilities:

- check whether claims are grounded;
- detect unsupported statements;
- assign confidence level;
- block or downgrade ungrounded responses.

---

#### Response Formatter Agent

Responsibilities:

- produce the final structured draft;
- include citations;
- include advisor review notice;
- keep tone clear, professional, and actionable.

---

### 7.4 Shared State

The workflow state should be defined with Pydantic.

Recommended state fields:

```python
class AgentState(BaseModel):
    user_query: str
    query_type: str | None
    plan: list[str]
    retrieved_chunks: list[RetrievedChunk]
    extracted_clauses: list[Clause]
    comparison_result: PolicyComparison | None
    draft_answer: str | None
    citations: list[Citation]
    verification: GroundingVerification | None
    final_answer: str | None
    confidence: Literal["high", "medium", "low"]
    requires_human_review: bool = True
    trace_summary: list[str]
    errors: list[str]
```

---

## 8. Non-Functional Requirements

### NFR-001 — Accuracy

The system must prioritize accuracy over fluency or speed.

It must not invent policy interpretations.

---

### NFR-002 — Grounding

Every substantive answer must be grounded in retrieved documents.

If the system cannot find sufficient support, it must state that the available documents do not provide enough evidence.

---

### NFR-003 — Latency

Target latency for the MVP:

```text
Simple query: under 15 seconds
Complex comparison query: under 30 seconds
```

These are target values, not hard production SLAs.

---

### NFR-004 — Observability

The system must use Phoenix to capture:

- latency;
- token usage;
- estimated costs;
- tool usage;
- retrieval events;
- errors;
- confidence scores;
- query type;
- fallback behavior.

---

### NFR-005 — Security and Guardrails

The system must implement defenses against:

- prompt injection;
- attempts to ignore source documents;
- requests to reveal prompts or hidden reasoning;
- unsupported answer generation;
- out-of-scope questions;
- excessive input length;
- direct customer-facing behavior;
- policy approval or modification requests.

---

### NFR-006 — Maintainability

The codebase must be modular, typed, documented, and testable.

Required engineering practices:

- Pydantic contracts;
- `.env` configuration;
- structured logging;
- error handling;
- clear module boundaries;
- tests;
- linting;
- Docker support.

---

### NFR-007 — Deployment

The system must be deployable using Docker on Hugging Face Spaces.

The first MVP interface will use Gradio.

---

### NFR-008 — LLM Provider Abstraction

The system must include an LLM provider interface.

Primary MVP provider:

```text
Groq API using GPT-OSS-120B as the test model
```

Future/local provider support:

```text
Ollama / llama-cpp / Llama-compatible local models
```

The public demo should prioritize reliability and responsiveness over local model execution.

---

## 9. Technical Architecture

### 9.1 Recommended Stack

```text
Language: Python
Interface: Gradio
Orchestration: LangGraph
LLM Provider: Groq API
Test Model: GPT-OSS-120B
Document Processing: Docling
Vector DB: Qdrant Cloud
Contracts: Pydantic
MCP: MCP Server + MCP Client
Optimization: DSPy
Observability: Phoenix
Testing: Pytest
Linting: Ruff
Deployment: Docker + Hugging Face Spaces
Environment: .env
```

---

### 9.2 High-Level Architecture

```text
Official PDF Documents
   ↓
Docling PDF-to-Markdown Conversion
   ↓
Document Cleaning and Normalization
   ↓
Semantic Chunking
   ↓
Embeddings Generation
   ↓
Qdrant Cloud Vector Store
   ↓
LangGraph Multi-Agent Workflow
   ↓
MCP Tool Calls / Native Tool Calls
   ↓
Citation Verification
   ↓
Structured Advisor Draft Response
   ↓
Gradio Public Demo UI
```

---

### 9.3 Runtime Architecture

```text
Advisor
   ↓
Gradio UI
   ↓
Input Guardrail
   ↓
LangGraph Workflow
   ↓
Tools
   ├── Document Retrieval Tool
   ├── Clause Extraction Tool
   ├── Policy Comparison Tool
   ├── Citation Verifier Tool
   └── Response Draft Tool
   ↓
Phoenix Tracing
   ↓
Structured Response + Citations + Trace Summary
```

---

### 9.4 Deployment Architecture

```text
GitHub Repository
   ↓
Docker Build
   ↓
Hugging Face Space
   ↓
Gradio App
   ↓
Groq API
   ↓
Qdrant Cloud
   ↓
Phoenix Tracing
```

---

## 10. Evaluation Requirements

### 10.1 Evaluation Dataset

The MVP must include a curated evaluation dataset with **30 questions** derived from examples and relevant content found in the official PDFs.

Each evaluation item should include:

- question;
- expected answer;
- source document;
- page or section;
- clause ID when available;
- query type;
- difficulty;
- expected citations;
- evaluation rubric.

Example:

```json
{
  "question": "What exclusions apply to hospitalization coverage?",
  "expected_answer": "...",
  "source_document": "...",
  "page": 14,
  "clause_id": "3.2.1",
  "query_type": "exclusion_explanation",
  "difficulty": "medium",
  "expected_citations": ["..."]
}
```

---

### 10.2 Evaluation Dimensions

The system must be evaluated across five dimensions:

#### Accuracy

Does the answer contain legally and factually correct information according to the documents?

#### Grounding

Does the answer stay within the retrieved document context?

#### Completeness

Does the answer include all critical elements required to avoid misleading the advisor?

#### Clarity

Is the response understandable, actionable, and well-structured?

#### Compliance

Does the response respect privacy, security, ethical boundaries, and system scope?

---

### 10.3 Metrics

Minimum metrics:

```text
faithfulness
groundedness
retrieval precision
retrieval recall
answer correctness
citation accuracy
tool success rate
latency
token usage
estimated cost per query
```

---

### 10.4 Evaluation Modes

The system must support:

- automated evaluation;
- manual review;
- golden dataset evaluation;
- DSPy optimization evaluation;
- evaluation report generation.

---

## 11. Guardrails and Safety Requirements

### 11.1 Prompt Injection Defense

The system must detect and reject attempts to:

- ignore source documents;
- bypass grounding rules;
- reveal internal prompts;
- reveal hidden reasoning;
- act as a final customer-facing advisor;
- approve or modify policies;
- generate unsupported claims.

---

### 11.2 Scope Guardrails

The system must only answer based on loaded documents.

If support is insufficient, it should respond with a controlled refusal such as:

```text
I could not find sufficient support in the loaded documents to answer this question reliably.
```

---

### 11.3 Mandatory Citation Policy

Every substantive response must include citations.

If no citations are available, the system must either:

- refuse to answer;
- return a low-confidence response;
- explicitly state that documentary support is insufficient.

---

### 11.4 Human Review Notice

Every final response must include an advisor review notice.

Example:

```text
This response is a draft for advisor review. It must be validated before being communicated to a customer.
```

---

## 12. Repository Structure

Recommended structure:

```text
project/
├── AGENTS.md
├── constitution.md
├── core/
│   ├── config.py
│   ├── logging.py
│   ├── llm.py
│   └── tracing.py
│
├── prompting/
│   ├── planner.md
│   ├── analyst.md
│   ├── verifier.md
│   └── formatter.md
│
├── contracts/
│   ├── state.py
│   ├── documents.py
│   ├── tools.py
│   └── responses.py
│
├── rag/
│   ├── ingestion.py
│   ├── pdf_to_markdown.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── retrieval.py
│
├── agents/
│   ├── graph.py
│   ├── planner.py
│   ├── retriever.py
│   ├── policy_analyst.py
│   ├── citation_verifier.py
│   ├── response_formatter.py
│   └── tools.py
│
├── memory/
│   └── session_store.py
│
├── evals/
│   ├── datasets/
│   │   └── golden_questions.jsonl
│   ├── metrics.py
│   ├── runner.py
│   └── reports/
│
├── mcp/
│   ├── server.py
│   ├── client.py
│   └── tools.py
│
├── ops/
│   ├── guardrails.py
│   ├── phoenix.py
│   └── monitoring.py
│
├── deploy/
│   ├── Dockerfile
│   └── start.sh
│
├── app/
│   └── ui.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   ├── test_tools.py
│   ├── test_graph.py
│   ├── test_mcp.py
│   ├── test_dspy.py
│   └── test_evals.py
│
├── data/
│   ├── raw/
│   ├── markdown/
│   ├── processed/
│   └── eval/
│
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── evaluation.md
│   └── deployment.md
│
├── specs/
│   ├── 001-document-ingestion.md
│   ├── 002-rag-retrieval.md
│   ├── 003-agent-orchestration.md
│   ├── 004-tools-contracts.md
│   ├── 005-mcp-integration.md
│   ├── 006-dspy-optimization.md
│   ├── 007-evaluation.md
│   ├── 008-observability.md
│   ├── 009-deployment.md
│   └── 010-guardrails.md
│
├── .env.example
├── requirements.txt
├── pyproject.toml
├── README.md
└── Makefile
```

---

## 13. Environment Variables

The project should define at least the following environment variables:

```text
GROQ_API_KEY=
GROQ_MODEL=gpt-oss-120b
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=
EMBEDDING_PROVIDER=
EMBEDDING_MODEL=
PHOENIX_PROJECT_NAME=
PHOENIX_ENDPOINT=
APP_ENV=development
LOG_LEVEL=INFO
MAX_INPUT_CHARS=4000
TOP_K=5
```

Additional variables may be added during implementation.

---

## 14. Development Methodology

### 14.1 Spec-Driven Development

The project will follow Spec-Driven Development.

Development flow:

```text
PRD
 ↓
constitution.md
 ↓
specs/
 ↓
implementation plan
 ↓
tasks
 ↓
code
 ↓
tests
 ↓
evals
 ↓
deployment
```

---

### 14.2 Required Specs

The project should include the following specs:

```text
001-document-ingestion.md
002-rag-retrieval.md
003-agent-orchestration.md
004-tools-contracts.md
005-mcp-integration.md
006-dspy-optimization.md
007-evaluation.md
008-observability.md
009-deployment.md
010-guardrails.md
```

Each spec should include:

- user story;
- functional requirements;
- technical requirements;
- acceptance criteria;
- data contracts;
- test strategy;
- risks;
- implementation notes.

---

## 15. Milestones

### Milestone 1 — Project Foundation

- Create repository structure.
- Add `AGENTS.md`.
- Add `constitution.md`.
- Add `.env.example`.
- Configure Ruff, Pytest, and logging.
- Configure base Dockerfile.
- Create initial README.

---

### Milestone 2 — Document Processing Pipeline

- Implement Docling PDF-to-Markdown conversion.
- Clean Markdown documents.
- Extract metadata.
- Implement semantic chunking.
- Store processed files.

---

### Milestone 3 — RAG Pipeline

- Generate embeddings.
- Configure Qdrant Cloud.
- Index chunks.
- Implement retrieval.
- Validate retrieval quality manually.

---

### Milestone 4 — Core Tools

- Implement `document_retrieval_tool`.
- Implement `clause_extraction_tool`.
- Implement `policy_comparison_tool`.
- Implement `citation_verifier_tool`.
- Implement `response_draft_tool`.

---

### Milestone 5 — LangGraph Multi-Agent Workflow

- Define agent state.
- Implement Planner Agent.
- Implement Retriever Agent.
- Implement Policy Analyst Agent.
- Implement Citation Verifier.
- Implement Response Formatter Agent.
- Add fallbacks.

---

### Milestone 6 — MCP Integration

- Implement MCP server.
- Expose core tools.
- Implement MCP client.
- Add MCP tests.
- Document MCP usage.

---

### Milestone 7 — DSPy Optimization

- Define DSPy module.
- Select optimization target.
- Use evaluation subset.
- Run optimization.
- Document before/after results.

---

### Milestone 8 — Evaluation

- Build 30-question dataset.
- Implement metrics.
- Implement evaluation runner.
- Generate evaluation report.
- Document baseline performance.

---

### Milestone 9 — Observability and Guardrails

- Integrate Phoenix.
- Add tracing for LLM calls.
- Add tracing for retrieval and tools.
- Implement prompt injection guardrails.
- Add input validation and usage limits.

---

### Milestone 10 — Demo and Deployment

- Build Gradio UI.
- Connect UI to workflow.
- Dockerize app.
- Deploy to Hugging Face Spaces.
- Validate public demo.
- Finalize README and documentation.

---

## 16. Risks and Mitigations

### Risk 1 — Retrieval Quality Is Poor

#### Impact

The system may retrieve irrelevant clauses and generate weak answers.

#### Mitigation

- Use semantic chunking.
- Preserve metadata.
- Tune `top_k`.
- Evaluate retrieval precision and recall.
- Use DSPy for retrieval query optimization.

---

### Risk 2 — Hallucinated or Unsupported Answers

#### Impact

High risk because insurance guidance must be accurate and grounded.

#### Mitigation

- Mandatory citations.
- Citation verifier.
- Strict prompts.
- Refusal behavior.
- Confidence scoring.

---

### Risk 3 — Public Demo Uses Real Documents

#### Impact

Real documents may contain confidential or restricted information.

#### Mitigation

- Review all documents before inclusion.
- Do not include personal customer data.
- Use only documents approved for demo exposure.
- Add disclaimers.
- Avoid exposing raw document download links if not required.

---

### Risk 4 — MVP Scope Becomes Too Large

#### Impact

MCP, DSPy, Phoenix, RAG, LangGraph, and deployment may overload the timeline.

#### Mitigation

- Implement core RAG first.
- Add LangGraph second.
- Add MCP and DSPy after core functionality works.
- Keep Gradio UI simple.
- Prioritize end-to-end demo over excessive polish.

---

### Risk 5 — Hugging Face Spaces Resource Limits

#### Impact

The app may be slow or unstable if heavy local models are used.

#### Mitigation

- Use Groq API for public demo inference.
- Use Qdrant Cloud instead of local vector DB.
- Avoid local Llama execution in public demo.
- Keep Docker image lightweight.

---

### Risk 6 — MCP Adds Deployment Complexity

#### Impact

MCP server/client architecture may complicate the public demo runtime.

#### Mitigation

- Keep native tool calls as fallback.
- Expose MCP tools for demonstration and tests.
- Avoid making MCP the only execution path in the MVP.

---

## 17. MVP Prioritization

### Must Have

- Docling PDF-to-Markdown ingestion.
- RAG pipeline with Qdrant Cloud.
- Groq API LLM provider.
- LangGraph workflow.
- Core five tools.
- Citation verification.
- Gradio UI.
- Phoenix tracing.
- Guardrails.
- 30-question evaluation dataset.
- Docker deployment.
- Hugging Face Spaces demo.
- README and documentation.

---

### Should Have

- MCP server and client.
- DSPy optimization experiment.
- GitHub Actions with lint, tests, and Docker build.
- Evaluation report.
- Confidence scoring.
- Basic session memory.

---

### Could Have

- Advanced reranking.
- Local Llama provider.
- Caching.
- Authentication.
- More advanced UI.
- Multiple document collections.

---

### Won’t Have in MVP

- CRM integration.
- Customer-facing chatbot.
- Production authentication.
- Real customer data.
- Policy approval flows.
- Premium calculation.
- WhatsApp integration.

---

## 18. Definition of Done

The MVP is complete when:

- The app is deployed and publicly accessible on Hugging Face Spaces.
- The advisor can ask questions through Gradio.
- The system retrieves relevant policy information from Qdrant Cloud.
- The system generates structured, cited draft responses.
- Unsupported questions are refused or marked as insufficiently grounded.
- The LangGraph workflow runs end-to-end.
- MCP integration is implemented and demonstrable.
- DSPy optimization is implemented and documented.
- Phoenix traces latency, tokens, costs, retrieval, and tool usage.
- The 30-question evaluation dataset exists.
- Evaluation metrics can be executed.
- Docker build works.
- Tests for core modules pass.
- README explains setup, architecture, usage, evaluation, and deployment.
- The project satisfies the technical requirements of the AI Engineering bootcamp.

---

## 19. Final Technical Decisions

| Decision Area | Selected Option |
|---|---|
| Cloud LLM Provider | Groq API |
| Test Model | GPT-OSS-120B |
| Vector Database | Qdrant Cloud |
| PDF-to-Markdown | Docling |
| Frontend | Gradio |
| Orchestration | LangGraph |
| MCP | Included in MVP |
| DSPy | Included in MVP |
| Observability | Phoenix |
| Deployment | Docker on Hugging Face Spaces |
| Evaluation Dataset Size | 30 curated questions |
| Documents | Real official documents approved for demo use |
| Local Models | Supported as future provider through Ollama/llama-cpp architecture |

---

## 20. Key Lessons Embedded in the PRD

1. The system must optimize for grounding and traceability, not generative creativity.
2. The assistant supports the advisor but never replaces the advisor.
3. Citation verification is a core safety mechanism, not an optional feature.
4. LangGraph provides controlled orchestration better suited to insurance workflows than an open-ended agent loop.
5. MCP and DSPy add portfolio value, but core RAG quality must be implemented first.

