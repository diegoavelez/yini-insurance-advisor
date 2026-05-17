# Requirements

## Feature Summary

This feature continues `Phase 1 — Configuration and Contracts` by introducing
the first shared contract foundation for Yini.

The goal is to define reusable Pydantic models for:

- retrieval outputs;
- clause extraction outputs;
- policy comparison outputs;
- grounding verification outputs;
- advisor response outputs;
- workflow state.

These contracts must be explicit, typed, and aligned with the PRD so future
pipeline, tool, and LangGraph work shares the same vocabulary.

## In Scope

- Add `contracts/documents.py` for document and retrieval-related contracts.
- Add `contracts/tools.py` for tool input/output contracts.
- Add `contracts/responses.py` for citations, verification, and advisor draft
  response contracts.
- Add `contracts/state.py` for the shared workflow state contract.
- Export the public contract surface through `contracts/__init__.py`.
- Add tests that validate the contract shapes and key business constraints.

## Out of Scope

- PDF ingestion logic.
- Retrieval implementation.
- Qdrant client integration.
- Agent orchestration logic.
- MCP server/client behavior.
- UI rendering logic.

## Contract Decisions

### Retrieval and Document Contracts

The retrieval contract should mirror the PRD output shape for
`document_retrieval_tool` while using typed Python/Pydantic models instead of
raw dictionaries.

The base retrieval item should include:

- `chunk_id`
- `text`
- `document_name`
- `page`
- `section`
- `clause_id`
- `score`

### Clause Extraction Contracts

Extracted clauses must classify into the PRD categories only:

- coverage
- exclusion
- restriction
- requirement
- procedure
- exception

Each clause must carry a summary, source reference fields, and enough metadata
to remain traceable to retrieved evidence.

### Tool Contracts

The first tool contract set must cover:

- retrieval query input
- retrieval result output
- clause extraction output
- policy comparison output
- grounding verification output

Only define the structures needed by the PRD today. Do not invent speculative
tool-specific runtime fields.

### Response Contracts

The advisor response contract must follow the PRD structure:

- suggested answer
- documentary basis
- citations
- confidence level
- limitations
- advisor review notice

The contract should support structured composition first; markdown formatting
can remain a later presentation concern.

### Workflow State Contract

The state model must align with the PRD recommended `AgentState` and keep the
fields explicit and typed. The model should include the core shared state fields
but avoid embedding runtime-only objects.

## Acceptance Criteria

- Contracts are implemented as Pydantic models.
- Retrieval and response contracts align with the PRD structures.
- Clause category values are restricted to the approved enum set.
- Confidence values are restricted to `high`, `medium`, or `low`.
- Workflow state can represent an end-to-end run without untyped dictionaries.
- Tests verify valid construction and key invalid cases.

## Guidance

- Prefer small explicit models over clever inheritance trees.
- Keep contracts reusable across modules.
- Match the naming and typing conventions already established in the repo.
