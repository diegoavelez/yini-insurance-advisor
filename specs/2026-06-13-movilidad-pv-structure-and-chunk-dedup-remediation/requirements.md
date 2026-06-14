# Requirements

## Title

Remediate `PV` commercial structure and chunk duplication for transversal
mobility documents.

## Context

The baseline `PV` audit confirmed that both commercial mobility documents
ingest successfully, but they generate too many repetitive chunks because of
slide-style structure:

- repeated `PLANES QUE APLICA` blocks;
- repeated commercial slogan lines;
- fragmented benefit blocks that should stay paired with applicability lists.

The next narrow slice should improve chunk density and readability before any
embeddings or retrieval alignment work.

## Scope

This slice should:

- normalize narrow `PV` commercial boilerplate inside blocks;
- canonicalize applicability headings consistently;
- merge a benefit block with its following `PLANES QUE APLICA` block when both
  belong to the same `PV` slide flow and fit safely in one chunk.

This slice should not:

- redesign generic chunking for the whole corpus;
- add retrieval heuristics;
- index the `PV` cohort yet.

## Acceptance Criteria

### 1. PV block cleanup

- Slogan-only commercial lines do not survive as standalone evidence.
- `Planes que aplica` variants normalize consistently.

### 2. PV chunk deduplication

- Feature blocks can absorb the immediately following applicability block when
  that pairing is structurally obvious and size-safe.

### 3. Backward compatibility

- Focused ingestion tests pass.
