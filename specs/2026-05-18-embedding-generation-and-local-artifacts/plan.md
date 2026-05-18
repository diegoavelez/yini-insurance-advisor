# Plan

1. Embedding Contract
   - Define typed embedding record and embedding bundle contracts.
   - Keep traceability fields explicit and aligned with chunk artifacts.

2. Configuration Integration
   - Reuse `core.config.Settings` for embedding provider/model inputs.
   - Fail loudly when embedding generation is requested with invalid config.

3. Offline Generation Flow
   - Add a deterministic offline step that reads chunk bundles and generates
     embeddings.
   - Keep execution local-first and independent from app runtime.

4. Artifact Persistence
   - Persist embedding outputs under a deterministic local path.
   - Preserve explicit overwrite/skip behavior and stable artifact naming.

5. Failure and Rerun Handling
   - Ensure partial embedding outputs are cleaned up on failure.
   - Preserve deterministic rerun behavior for the same inputs and config.

6. Validation Coverage
   - Add tests for typed artifacts, config usage, deterministic ordering,
     failure handling, and local persistence behavior.

7. Deferred Work Boundary
   - Explicitly stop before Qdrant collection bootstrap, upserts, retrieval,
     and app integration.
