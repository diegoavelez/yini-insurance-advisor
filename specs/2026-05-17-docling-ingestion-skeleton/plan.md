# Plan

1. Ingestion Entry Contract
   - Define the admin CLI command shape, expected inputs, and success/failure
     behavior.
   - Lock the canonical command name, required flags, optional flags, and exit
     conditions.

2. Storage Conventions
   - Define the baseline responsibilities of `data/raw/`, `data/markdown/`, and
     `data/processed/`.
   - Define how output paths remain traceable to the source PDF.
   - Define deterministic output naming and manifest location rules.

3. Processed-Document Contracts
   - Define typed metadata and status fields for processed documents.
   - Include explicit error reporting fields for failed conversions.
   - Define the initial ingestion status vocabulary and manifest record shape.

4. Docling Runtime Assumptions
   - Define local and container dependency expectations for Docling.
   - Define the non-network smoke path used to confirm dependency availability.

5. Re-run and Failure Policy
   - Define `--overwrite` and `--fail-fast` behavior.
   - Define when runs exit non-zero and how skipped attempts are reported.

6. Deferred Work Boundary
   - Explicitly defer cleaning heuristics, chunking, embeddings, and UI triggers
     to later slices.
