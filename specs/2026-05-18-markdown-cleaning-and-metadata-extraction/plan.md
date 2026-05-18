# Plan

1. Processed Artifact Extension
   - Extend the processed-document contract to represent cleaned Markdown
     outputs explicitly.
   - Define the deterministic relationship between raw Markdown, cleaned
     Markdown, and processed metadata files.

2. Cleaning Rules
   - Implement a conservative Markdown cleaning pass.
   - Lock the allowed and disallowed transformations so retrieval evidence is
     preserved.

3. Metadata Extraction Boundary
   - Define the minimum metadata fields extracted in this slice.
   - Keep fallback values explicit when richer metadata cannot be extracted
     safely.

4. CLI Integration
   - Extend the existing ingestion command so cleaning and metadata extraction
     happen in the offline pipeline.
   - Keep failure behavior aligned with `--overwrite` and `--fail-fast`.

5. Failure and Re-run Behavior
   - Define how partial failures are recorded in the manifest.
   - Define when cleaned artifacts are skipped, regenerated, or rejected as
     incomplete.

6. Test Coverage
   - Add focused tests for cleaning determinism, metadata fallback behavior,
     cleaned artifact paths, and failure reporting.

7. Deferred Work Boundary
   - Explicitly defer semantic chunking, retrieval logic, and embeddings to the
     next roadmap phases.
