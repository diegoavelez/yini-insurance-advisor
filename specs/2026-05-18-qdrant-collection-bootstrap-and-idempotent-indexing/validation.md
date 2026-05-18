# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The pipeline reads persisted embedding artifacts and maps them into explicit
  Qdrant point shapes.
- `Settings` validation fails loudly when Qdrant configuration is missing or
  unusable.
- Collection bootstrap is repeatable and does not fail merely because the
  collection already exists.
- Incompatible collection shape is treated as a loud failure.
- Indexing reruns are idempotent and do not create duplicate logical point
  identities.
- Retry/backoff behavior is exercised for transient failures.
- Permanent failures are not treated as successful indexing.
- The implementation remains scoped to indexing, not retrieval-time behavior.

## Merge Readiness

This spec is ready when the second `Phase 4` slice is decision-complete for:

- Qdrant config validation;
- collection bootstrap and compatibility checks;
- deterministic point mapping;
- idempotent upsert behavior;
- explicit retry/failure handling;
- indexing smoke checks;

without drifting into retrieval orchestration or answer generation.
