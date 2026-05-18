# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The pipeline reads persisted chunk bundles and produces typed local embedding
  artifacts.
- Embedding artifacts preserve chunk ordering and traceability metadata.
- Provider/model configuration is read from `Settings` and reflected in the
  artifact output.
- Artifact paths are deterministic for the same input bundle and schema.
- Overwrite/skip behavior is explicit and reproducible.
- Failure during embedding generation is not treated as successful output.
- Partial embedding artifacts are not preserved as valid success artifacts.
- The implementation stops before Qdrant writes.

## Merge Readiness

This spec is ready when the first `Phase 4` slice is decision-complete for:

- typed embedding artifact contracts;
- local offline embedding generation;
- deterministic local embedding persistence;
- config-driven provider/model usage;
- explicit failure and rerun behavior;

without drifting into Qdrant collection setup or indexing behavior.
