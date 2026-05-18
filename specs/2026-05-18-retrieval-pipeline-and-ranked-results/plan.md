# Plan

1. Retrieval Contracts
   - Reuse or refine typed retrieval input/output contracts.
   - Keep the public retrieval interface explicit and typed.

2. Query Embedding Path
   - Reuse the configured embedding provider/model for query embeddings.
   - Fail loudly for invalid or unavailable embedding prerequisites.

3. Qdrant Search Flow
   - Add the first retrieval search path against the configured collection.
   - Preserve deterministic ranking order from the search response.

4. Payload Mapping
   - Map Qdrant hits back into `RetrievedChunk` results.
   - Preserve traceability metadata and explicit optional-field behavior.

5. Failure and Empty-Result Handling
   - Distinguish explicit failures from successful empty retrieval results.
   - Keep response-mapping problems visible and testable.

6. Smoke Validation
   - Add narrow smoke checks for query embedding plus Qdrant search execution.
   - Keep validation focused on retrieval readiness, not answer quality.

7. Deferred Work Boundary
   - Explicitly stop before answer generation, citations in final responses,
     UI integration, and orchestration logic.
