# Plan

1. Indexing Contracts
   - Define any typed indexing manifest or result contracts needed for Qdrant
     writes.
   - Keep mapping explicit from `EmbeddingBundle` inputs to Qdrant point shape.

2. Settings Validation
   - Reuse `core.config.Settings` and centralized startup validation seams for
     Qdrant requirements.
   - Fail loudly for missing or unusable Qdrant config.

3. Collection Bootstrap
   - Add deterministic collection bootstrap and compatibility checks.
   - Ensure reruns behave safely when the collection already exists.

4. Point Upsert Flow
   - Add deterministic point-id generation and payload mapping.
   - Implement idempotent upsert behavior from local embedding artifacts.

5. Retry and Failure Handling
   - Add explicit retry/backoff behavior for transient failures.
   - Preserve explicit failure reporting and fail-fast semantics.

6. Smoke Validation
   - Add narrow operational smoke checks for configured collection usability.
   - Keep checks focused on indexing readiness, not retrieval quality.

7. Test Coverage
   - Add tests for config validation, collection bootstrap, point mapping,
     idempotent reruns, retry behavior, and failure reporting.

8. Deferred Work Boundary
   - Explicitly stop before retrieval orchestration, answer generation, and UI
     integration.
