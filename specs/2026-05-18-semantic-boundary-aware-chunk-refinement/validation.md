# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The same cleaned Markdown input still produces deterministic chunk artifacts
  across reruns.
- Headings stay attached to relevant nearby body content when possible.
- Clause-like markers are not arbitrarily split from their following clause
  content when the chunk size allows them to remain together.
- Tiny structural markers do not become standalone chunks unless required by
  hard size constraints.
- Chunk schema version behavior is explicit when boundary logic changes.
- Chunk ids remain deterministic for the same inputs, configuration, and schema
  version.
- Improved section metadata remains typed and deterministic.
- Failure during refined chunk generation is not treated as successful output.

## Merge Readiness

This spec is ready when the next `Phase 3` slice is decision-complete for:

- heading-aware chunk refinement;
- clause-safe boundary behavior;
- explicit chunk schema version advancement;
- improved deterministic section metadata propagation;

without drifting into embeddings, indexing, or retrieval-time reasoning.
