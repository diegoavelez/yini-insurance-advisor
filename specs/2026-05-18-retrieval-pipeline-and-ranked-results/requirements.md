# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 5 — Basic RAG MVP`.

The goal is to implement the first retrieval pipeline over the indexed Qdrant
collection and return typed, traceable ranked results without yet generating
final answers.

This slice should validate that the system can turn a user query into query
embeddings, search Qdrant, and map the results into durable retrieval
contracts.

## In Scope

- Generate query embeddings through the configured embedding path.
- Query the indexed Qdrant collection.
- Map raw search hits into typed `RetrievedChunk` results.
- Preserve traceability metadata needed for later citations.
- Define retrieval failure behavior and smoke validation.
- Add the first callable retrieval pipeline seam for later RAG orchestration.

## Out of Scope

- Final answer generation.
- Citation rendering in user-facing answers.
- Gradio query UI.
- Multi-turn orchestration.
- Query rewriting or decomposition.
- Re-ranking beyond the base Qdrant result order.

## Execution Model

This slice may remain CLI-first or be introduced as an internal callable
pipeline function, but it must stay:

- deterministic where possible;
- explicitly configured;
- testable independently of UI;
- reusable by later tools and RAG layers.

The execution path for this slice should be:

1. Accept a query and retrieval settings.
2. Generate a query embedding using the configured embedding provider/model.
3. Query Qdrant against the configured collection.
4. Map hits into typed retrieval results.
5. Return explicit, traceable ranked outputs.

## Configuration Contract

This slice must use the typed settings contract in `core.config.Settings`.

At minimum:

- `EMBEDDING_PROVIDER` and `EMBEDDING_MODEL` must be valid for query embedding;
- `QDRANT_URL`, `QDRANT_API_KEY`, and `QDRANT_COLLECTION` must be required when
  retrieval is requested;
- `TOP_K` should remain the default retrieval limit unless explicitly
  overridden by a typed retrieval input contract;
- config validation must fail loudly for invalid retrieval prerequisites.

## Retrieval Input Contract

This slice should use or refine the existing typed retrieval input contract in
`contracts.tools`.

At minimum, retrieval inputs must support:

- query text;
- `top_k`;
- optional metadata filters;
- explicit validation bounds.

The retrieval path must not accept untyped ad hoc dictionaries as its primary
public interface.

## Retrieval Output Contract

This slice should use the existing typed retrieval output contract centered on
`RetrievedChunk`.

At minimum, each returned result should preserve:

- `chunk_id`
- `text`
- `document_name`
- `section`
- `score`
- any traceable metadata available from indexed payloads

The output order should reflect the retrieval ranking returned by the search
workflow.

## Qdrant Query Mapping

This slice should define the explicit mapping from indexed Qdrant payloads back
into retrieval contracts.

At minimum:

- point payloads must map back into typed retrieval results consistently;
- missing optional metadata should degrade gracefully;
- malformed or incompatible payloads must fail loudly or be handled through an
  explicit policy;
- retrieval result ordering must remain stable for a given Qdrant response.

## Failure Behavior

If retrieval fails:

- failures must be explicit and not treated as empty successful retrieval;
- config failures must fail loudly before search;
- malformed response mapping must remain traceable;
- if no results are found, that should be represented explicitly as an empty
  successful retrieval result, not as a hidden error.

## Smoke Validation

This slice should include lightweight retrieval smoke validation.

At minimum:

- a successful path confirms query embedding and Qdrant search can execute;
- ranked results are returned in typed form;
- empty-result behavior is explicit and distinguishable from failure.

## Acceptance Criteria

- A query can be embedded and searched against Qdrant.
- Ranked results map into typed `RetrievedChunk` outputs.
- Traceability metadata survives retrieval mapping.
- Config and response-mapping failures are explicit.
- The slice stops before final answer generation and UI work.
