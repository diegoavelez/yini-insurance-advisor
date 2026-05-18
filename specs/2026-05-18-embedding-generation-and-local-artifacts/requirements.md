# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 4 — Embeddings and Vector Store`.

The goal is to generate deterministic embeddings from persisted chunk bundles
and save them as local reproducible artifacts before any Qdrant indexing is
introduced.

This slice should establish the offline embedding pipeline and typed embedding
artifact contract without yet performing remote vector-store writes.

## In Scope

- Read persisted chunk bundles produced by the Phase 3 pipeline.
- Generate embeddings from chunk text using the configured provider and model.
- Define a typed local embedding artifact contract.
- Persist deterministic embedding artifacts to local storage.
- Define explicit vector payload shape for later indexing work.
- Preserve deterministic rerun behavior and explicit failure handling.

## Out of Scope

- Qdrant client wiring.
- Qdrant collection creation or writes.
- Retrieval-time ranking.
- Query-time embedding generation.
- Hosted app integration.
- Multi-provider routing beyond the single configured provider/model path.

## Execution Model

This slice should keep the offline CLI execution model used by earlier pipeline
phases.

The canonical path may remain under `python -m rag.ingestion` or move into a
dedicated offline pipeline command, but the implementation must stay:

- local-first;
- admin-triggered;
- reproducible;
- independent from the user-facing app runtime.

The execution path for this slice should be:

1. Read processed chunk artifacts from `data/processed/chunks/`.
2. Generate embeddings deterministically from chunk text.
3. Persist local embedding artifacts for later indexing.

## Input Contract

The embedding pipeline should consume the persisted `ChunkBundle` artifacts from
Phase 3.

At minimum, the embedding step must preserve:

- `source_pdf_id`
- `chunk_id`
- `chunk_schema_version`
- `document_name`
- `document_version`
- `section`
- `section_path`
- `chunk text`

The pipeline must not silently regenerate chunk ids or mutate chunk ordering.

## Embedding Configuration Contract

This slice should use the typed settings contract in `core.config.Settings`.

At minimum:

- `EMBEDDING_PROVIDER` must be read from config;
- `EMBEDDING_MODEL` must be read from config;
- startup/runtime validation should fail loudly if embedding generation is
  requested with invalid or unusable embedding configuration;
- configuration behavior must remain explicit and deterministic.

This slice does not need dynamic provider selection logic beyond the configured
provider/model path, but it must preserve a clear seam for later expansion.

## Local Embedding Artifact Contract

This slice should define a typed persisted artifact for embeddings.

At minimum, each persisted embedding item should include:

- `chunk_id`
- `source_pdf_id`
- `chunk_schema_version`
- `embedding_provider`
- `embedding_model`
- `vector_dimension`
- `vector`
- traceability metadata required for later indexing

The bundle-level artifact should also include:

- source chunk artifact path
- output embedding artifact path
- embedding schema version
- embedding provider/model used
- document-level traceability fields

## Persistence Rules

Embedding artifacts must be persisted locally before any vector-store indexing
is attempted.

The storage rules should be deterministic and reproducible.

The implementation should define a canonical output location under
`data/processed/embeddings/`.

At minimum:

- the output path must be deterministic for the same input bundle and schema;
- reruns with the same inputs and configuration must produce the same artifact
  path;
- overwrite/skip behavior must remain explicit and predictable.

## Determinism and Reproducibility

This slice must preserve:

- deterministic artifact paths;
- stable chunk ordering in embedding outputs;
- stable provider/model metadata in persisted artifacts;
- explicit schema versioning for embedding artifacts.

If exact numeric vector equality cannot be guaranteed across providers or
library versions, the implementation should still preserve deterministic input
ordering and explicit artifact provenance.

## Failure Behavior

If embedding generation fails:

- the run must fail loudly;
- the failure must not be treated as successful artifact generation;
- partial embedding artifacts must not be preserved as valid success artifacts;
- manifest or logging behavior should remain explicit and traceable.

If one input bundle fails and fail-fast is disabled, the implementation may
continue with other bundles, but the failure must be recorded clearly.

## Acceptance Criteria

- The pipeline reads persisted chunk bundles and generates local embedding
  artifacts.
- Embedding artifacts are typed, explicit, and traceable.
- Provider/model configuration is read from `Settings`.
- Local persistence is deterministic and reproducible.
- The slice stops before Qdrant writes.
- Failure behavior is loud and does not preserve partial success artifacts.
