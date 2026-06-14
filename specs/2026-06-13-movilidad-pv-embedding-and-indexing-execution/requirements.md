# Requirements

## Title

Execute embeddings and indexing for the transversal mobility `PV` cohort.

## Context

The `PV` corpus has already cleared the structural cleanup slices and the
embedding runtime seam now fails fast with an explicit warm-up path.

After the operator runs `warmup-embedding-assets`, the next step is operational:

- generate local embeddings for the `PV` chunk artifacts;
- index those embeddings into Qdrant;
- verify that retrieval over the `PV` cohort works end-to-end.

## Scope

This slice should:

- generate embeddings only for the `PV` transversal chunk artifacts;
- index only the resulting `PV` embedding artifacts into the configured Qdrant
  collection;
- run at least one retrieval validation against the indexed `PV` cohort;
- capture the exact commands and outcome in validation docs.

This slice should not:

- change embedding or retrieval code;
- re-open corpus-cleanup logic unless the operational run surfaces a new defect.

## Acceptance Criteria

### 1. Embeddings

- `PV` embeddings are generated successfully from the latest chunk artifacts.

### 2. Indexing

- The generated `PV` embedding artifacts are indexed successfully into Qdrant.

### 3. Retrieval verification

- At least one retrieval/query validation confirms that indexed `PV` evidence is
  reachable through the live pipeline.
