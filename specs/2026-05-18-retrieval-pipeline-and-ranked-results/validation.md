# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- A query can be embedded with the configured provider/model.
- Retrieval fails loudly when required Qdrant config is missing or unusable.
- Qdrant search results map into typed `RetrievedChunk` outputs.
- Ranked ordering is preserved from the search response.
- Empty-result retrieval is explicit and not treated as failure.
- Malformed payload mapping is handled through an explicit, testable policy.
- The implementation remains scoped to retrieval and does not generate answers.

## Merge Readiness

This spec is ready when the first `Phase 5` slice is decision-complete for:

- query embedding generation;
- Qdrant search execution;
- typed retrieval result mapping;
- explicit failure and empty-result handling;
- retrieval smoke checks;

without drifting into answer generation, UI integration, or orchestration.
