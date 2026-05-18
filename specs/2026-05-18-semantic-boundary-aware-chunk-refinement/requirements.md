# Requirements

## Feature Summary

This feature defines the next narrow implementation slice of
`Phase 3 — Semantic Chunking`.

The goal is to refine the first deterministic chunking pass so chunk boundaries
better preserve semantic meaning and avoid arbitrary clause splitting while
remaining deterministic and local-only.

This slice should improve chunk quality without introducing embeddings,
retrieval ranking, or LLM-driven segmentation.

## In Scope

- Refine chunk boundary logic to be more heading-aware and clause-safe.
- Improve section metadata propagation into chunk records.
- Define when a chunk schema version must advance because chunk boundary logic
  changes.
- Preserve deterministic rerun behavior while improving chunk quality.
- Define explicit validation expectations for clause-safe boundary behavior.

## Out of Scope

- Embeddings generation.
- Qdrant indexing.
- Retrieval ranking.
- LLM-assisted segmentation.
- Clause extraction as a separate reasoning step.
- User-facing UI changes.
- Dynamic optimization of chunk settings.

## Execution Model

This slice should keep the existing offline ingestion command as the canonical
execution path:

```bash
python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "*.pdf" \
  --overwrite false \
  --fail-fast false \
  --chunk-size 1200 \
  --chunk-overlap 200
```

The execution path should still remain:

1. PDF to raw Markdown conversion.
2. Raw Markdown to cleaned Markdown conversion.
3. Cleaned Markdown to persisted chunk artifact generation.

This slice refines only stage 3.

## Boundary Refinement Contract

The chunker should now incorporate deterministic semantic-boundary cues from
cleaned Markdown, especially:

- heading boundaries;
- short section transitions;
- numbered clause-like lines when clearly present;
- paragraph grouping that avoids splitting tiny related fragments across
  neighboring chunks.

The refined logic should prefer boundaries that:

- keep headings with their immediately relevant body content when possible;
- avoid splitting a short clause header from the clause text that follows;
- avoid isolated tiny chunks created only by structural markers;
- preserve ordering exactly as it appears in cleaned Markdown.

The refined logic must not:

- summarize or rewrite text;
- infer hidden policy structure;
- depend on LLM calls;
- reorder sections;
- create non-deterministic boundaries.

## Clause-Safe Splitting Rules

This slice should explicitly reduce arbitrary clause splitting.

Examples of boundary-safe behavior:

- a numbered clause marker should remain attached to its immediately following
  clause text when the combined text still fits the chunking constraints;
- a heading should not become a standalone tiny chunk if the following content
  can fit with it;
- overlap should preserve continuity without duplicating excessive unrelated
  structure.

If a clause-sized block exceeds the chunk size limit, deterministic fallback
splitting is allowed, but the implementation must:

- minimize the number of forced splits;
- preserve stable ordering;
- surface the same result across reruns.

## Section Metadata Propagation

This slice should improve section metadata in chunk records so later retrieval
and citation steps have more precise structure hints.

The implementation may refine:

- current section label propagation;
- heading context selection;
- chunk-level structural context fields;

but must keep the contract explicit and typed.

## Chunk Schema Versioning

This slice should define when a chunk schema version advances.

At minimum:

- if boundary logic changes in a way that can alter chunk ids or chunk
  boundaries, the implementation should advance the chunk schema version;
- the schema version should remain explicit in persisted chunk records and
  bundles;
- reruns with the same schema version and same inputs must still be
  deterministic.

## Reproducibility Rules

This slice must preserve:

- deterministic chunk boundaries for the same cleaned Markdown input;
- deterministic chunk ids for the same schema version and configuration;
- deterministic persisted chunk artifact paths;
- stable metadata propagation across reruns.

Improved chunk quality must not come at the cost of unpredictable reruns.

## Failure Behavior

If refined boundary logic fails during chunk generation:

- the run must fail loudly;
- the failure must not be treated as successful chunk output;
- partial chunk artifacts must not be preserved as valid success artifacts.

If refined section metadata cannot be determined:

- chunk generation may still succeed if required traceability fields remain
  present;
- fallback section behavior must be explicit and deterministic.

## Acceptance Criteria

- Chunk boundaries become more heading-aware and clause-safe.
- Tiny structural fragments are less likely to become standalone chunks.
- Chunk schema version behavior is explicit when boundary logic changes.
- Section metadata propagation improves while staying typed and deterministic.
- Chunk ids and persistence remain deterministic across reruns.
- The slice remains local-only and stops before embeddings or retrieval logic.
