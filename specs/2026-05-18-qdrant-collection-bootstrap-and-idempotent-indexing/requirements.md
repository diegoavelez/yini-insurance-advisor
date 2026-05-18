# Requirements

## Feature Summary

This feature defines the second narrow implementation slice of
`Phase 4 — Embeddings and Vector Store`.

The goal is to bootstrap a Qdrant collection and index locally persisted
embedding artifacts into it with deterministic, idempotent behavior.

This slice should turn the local embedding outputs into a repeatable Qdrant
indexing workflow without yet building retrieval orchestration or answer
generation.

## In Scope

- Read persisted embedding artifacts produced by the first Phase 4 slice.
- Initialize or validate the target Qdrant collection.
- Map typed local embedding payloads into Qdrant points.
- Upsert vectors into Qdrant with idempotent behavior.
- Define explicit retry/backoff behavior for transient indexing failures.
- Add indexing smoke checks that validate the configured collection is usable.

## Out of Scope

- Retrieval ranking logic.
- End-user QA flows.
- Query-time answer generation.
- Gradio retrieval UI.
- Multi-vector or hybrid search strategies.
- Advanced relevance tuning.

## Execution Model

This slice should keep the offline admin-triggered execution model.

The canonical path may remain under `python -m rag.ingestion` or move into a
dedicated indexing command, but it must stay:

- local-first for control;
- explicitly configured;
- reproducible;
- separate from user-facing runtime.

The execution path for this slice should be:

1. Read persisted embedding artifacts from local storage.
2. Validate Qdrant configuration from `Settings`.
3. Bootstrap or verify the target collection.
4. Upsert points idempotently into Qdrant.
5. Emit explicit manifest or logging results for indexing attempts.

## Configuration Contract

This slice must use the typed settings contract in `core.config.Settings`.

At minimum:

- `QDRANT_URL` must be required when indexing is requested;
- `QDRANT_API_KEY` must be required when indexing is requested;
- `QDRANT_COLLECTION` must be required and explicit;
- startup/runtime validation must fail loudly when indexing is requested with
  invalid Qdrant configuration.

This slice should continue to use explicit settings validation seams rather than
scattered environment access.

## Input Contract

The indexing pipeline should consume the persisted `EmbeddingBundle` artifacts
from the first Phase 4 slice.

At minimum, indexing must preserve:

- `chunk_id`
- `source_pdf_id`
- `chunk_schema_version`
- `embedding_schema_version`
- `embedding_provider`
- `embedding_model`
- vector values
- payload metadata needed for later filtering and traceability

The indexing step must not silently regenerate chunk identifiers or mutate
embedding ordering.

## Qdrant Collection Contract

This slice should define the initial collection bootstrap behavior.

At minimum:

- the collection name must come from `Settings`;
- vector size must match the embedding artifact dimension;
- collection creation must be repeatable;
- reruns must not fail merely because the collection already exists;
- collection validation must fail loudly if an incompatible collection shape is
  detected.

This slice does not need advanced collection tuning beyond what is required for
correct and repeatable bootstrap behavior.

## Qdrant Point Mapping

This slice should define the explicit mapping from local embedding artifacts to
Qdrant points.

At minimum:

- point identifiers should be deterministic and derived from stable chunk
  identity;
- payloads must preserve the traceability fields needed for future retrieval
  filtering and citations;
- vector values must be passed through from the local embedding artifact
  without hidden mutation.

## Idempotent Indexing Behavior

This slice should make indexing safe to rerun.

At minimum:

- repeated indexing runs for the same embedding artifact should upsert rather
  than duplicate;
- reruns should preserve deterministic point identity;
- overwrite behavior should remain explicit where relevant;
- successful reruns should not corrupt or fan out duplicate point state.

## Retry and Failure Behavior

This slice should define explicit retry/backoff behavior for transient Qdrant
failures.

At minimum:

- transient client failures should be retried deterministically;
- permanent failures should fail loudly;
- partial indexing success must remain explicitly traceable;
- failure must not be silently treated as successful indexing.

If one artifact fails and fail-fast is disabled, later artifacts may still be
attempted, but failure reporting must remain explicit.

## Smoke Validation

This slice should include lightweight indexing smoke validation against the
configured collection.

At minimum:

- a successful run should confirm the collection is reachable and usable;
- indexing smoke checks should validate that at least one point can be written
  and recognized as indexed through the intended workflow;
- the smoke checks should remain narrow and operational, not retrieval-quality
  evaluation.

## Acceptance Criteria

- The pipeline reads persisted embedding artifacts and writes them into Qdrant.
- Collection bootstrap is explicit and repeatable.
- Point identity and payload mapping are deterministic and traceable.
- Indexing is idempotent across reruns.
- Qdrant config is validated through `Settings`.
- Retry/failure behavior is explicit and testable.
- The slice stops before retrieval orchestration or answer generation.
