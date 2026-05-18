# Plan

1. Boundary Rules
   - Refine chunk boundary selection to be heading-aware and clause-safe.
   - Keep all boundary decisions deterministic and local-only.

2. Structural Grouping
   - Improve grouping of headings, clause markers, and short related content.
   - Reduce tiny structurally meaningless chunks where possible.

3. Metadata Refinement
   - Improve section metadata propagation into chunk records.
   - Keep fallback section behavior explicit and typed.

4. Schema Version Policy
   - Define when chunk schema version changes are required.
   - Ensure ids remain stable within a schema version and config set.

5. Failure and Rerun Handling
   - Preserve strict failure behavior for partial chunk outputs.
   - Preserve deterministic rerun behavior despite better boundary logic.

6. Test Coverage
   - Add tests for heading-aware grouping, clause-safe splitting, schema
     version behavior, metadata propagation, and deterministic reruns.

7. Deferred Work Boundary
   - Explicitly defer embeddings, vector indexing, retrieval ranking, and
     answer generation.
