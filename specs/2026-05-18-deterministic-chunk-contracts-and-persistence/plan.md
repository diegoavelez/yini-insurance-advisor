# Plan

1. Chunk Contract Definition
   - Define the first typed chunk record and any document-level chunk bundle
     contract.
   - Lock the minimum traceability fields required for later retrieval and
     citations.

2. Chunking Rules
   - Implement the first deterministic chunking pass for cleaned Markdown.
   - Make chunk ordering, boundaries, and fallback behavior predictable.

3. Configuration Boundary
   - Define explicit chunk size and overlap settings.
   - Keep configuration discoverable and testable instead of hiding it in
     untyped constants.

4. Identifier Strategy
   - Define deterministic chunk ids based on stable source inputs.
   - Ensure reruns with the same inputs reproduce the same ids.

5. Persistence Path
   - Persist chunk artifacts locally in a deterministic format and path.
   - Define skip or overwrite behavior for reruns.

6. Failure Handling
   - Define how chunk-generation failures are surfaced and how partial chunk
     artifacts are handled.
   - Keep success semantics strict and explicit.

7. Test Coverage
   - Add focused tests for deterministic chunk boundaries, id stability,
     metadata propagation, persistence format, and rerun behavior.

8. Deferred Work Boundary
   - Explicitly defer embeddings, Qdrant indexing, and retrieval-time ranking
     to later phases.
