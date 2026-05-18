# Requirements

## Feature Summary

This feature defines the first narrow implementation slice of
`Phase 3 — Semantic Chunking`.

The goal is to turn cleaned Markdown artifacts into deterministic,
retrieval-ready chunk records without introducing embeddings or vector indexing
yet.

This slice should establish:

- the first chunk contract for cleaned Markdown inputs;
- deterministic chunk identifiers;
- configurable chunk size and overlap behavior;
- metadata propagation from processed documents into chunks;
- local chunk persistence for later indexing work.

## In Scope

- Define the first chunk contract and persisted chunk artifact shape.
- Define the chunking execution path for cleaned Markdown outputs.
- Define configurable chunk size and overlap settings for the local chunking
  pass.
- Define deterministic chunk identifier rules.
- Define how processed-document metadata is propagated into chunks.
- Define local persisted chunk artifact paths and rerun behavior.

## Out of Scope

- Embeddings generation.
- Qdrant indexing.
- Retrieval ranking logic.
- LLM answer generation.
- Clause extraction semantics.
- UI chunking triggers.
- Advanced semantic segmentation heuristics beyond the first deterministic pass.

## Execution Model

This slice should remain an admin-only offline pipeline step.

The chunking flow should extend the existing local document-processing path,
not introduce an app route or interactive UI entrypoint.

### CLI Contract

This slice should keep `python -m rag.ingestion ingest-pdfs ...` as the
canonical execution path.

The existing ingestion command should now perform:

1. PDF to raw Markdown conversion.
2. Raw Markdown to cleaned Markdown conversion.
3. Cleaned Markdown to persisted chunk artifact generation.

This slice should add explicit optional chunking flags to that command:

- `--chunk-size`
- `--chunk-overlap`

with deterministic defaults defined in code.

## Chunking Contract

The first chunking pass should be deterministic and conservative.

The chunker should:

- split cleaned Markdown into retrieval-ready text units;
- preserve ordering from the cleaned document;
- avoid arbitrary reordering of clauses and headings;
- propagate traceable source metadata into every chunk.

The chunker should not:

- summarize content;
- infer policy meaning;
- merge unrelated sections based on semantic guesses;
- introduce LLM-dependent segmentation.

## Chunk Configuration

This slice should define explicit local configuration for:

- `chunk_size`
- `chunk_overlap`

The values do not need to be globally optimal yet, but the behavior must be
predictable and testable.

Configuration may initially live in code or typed settings, but the boundary
must be explicit and not buried in magic constants.

## Chunk Identifier Rules

Each chunk must have a deterministic `chunk_id`.

At minimum, the identifier should be reproducible from stable source inputs
such as:

- `source_pdf_id`
- chunk order or stable offset
- optional chunk schema version

The same cleaned Markdown input with the same chunking parameters should
produce the same chunk identifiers across reruns.

## Metadata Propagation

Each chunk record should preserve the essential traceability fields needed for
later retrieval and citation work, including:

- `chunk_id`
- `source_pdf_id`
- `document_name`
- `document_version`
- `source_pdf_path`
- `cleaned_markdown_output_path`
- chunk text
- chunk order index
- optional section or heading context when deterministically available

This slice should prefer explicit propagated metadata over recomputation later.

## Persistence Contract

This slice should persist chunk artifacts locally before any Qdrant indexing.

Baseline artifact expectations:

- chunk artifact path should be deterministic from `source_pdf_id`
- chunk persistence should live under `data/processed/chunks/`
- each per-document chunk artifact should be stored at
  `data/processed/chunks/<source_pdf_id>.chunks.json`
- reruns should either:
  - replace the per-document chunk artifact deterministically; or
  - skip when artifacts already exist and overwrite is disabled

The persisted format for this slice should be explicit and typed JSON containing
a document-level chunk bundle with:

- bundle metadata
- chunk configuration used
- ordered chunk records

## Failure Behavior

If cleaned Markdown exists but chunk generation fails:

- the run must fail loudly;
- the failure must be recorded in a deterministic local artifact or manifest
  path when the implementation already uses one;
- partial chunk output must not be treated as successful completion.

If metadata propagation is incomplete but chunking succeeds:

- the run may still succeed only when missing fields are optional and fallback
  values are explicitly defined;
- the implementation must not silently drop required traceability fields.

## Reproducibility Rules

This slice must preserve reproducibility:

- the same cleaned Markdown input and chunk settings produce the same chunk
  boundaries;
- the same inputs produce the same chunk identifiers;
- persisted chunk paths remain deterministic;
- metadata propagation remains stable across reruns.

## Acceptance Criteria

- A first chunk contract is defined for cleaned Markdown outputs.
- The existing ingestion CLI remains the canonical execution path and exposes
  explicit chunk configuration flags.
- Chunk size and overlap behavior are explicit.
- Chunk identifiers are deterministic.
- Chunk metadata preserves source traceability.
- Chunk persistence exists locally at deterministic
  `data/processed/chunks/<source_pdf_id>.chunks.json` paths before vector
  indexing.
- Failure behavior is explicit and does not treat partial chunk output as
  success.
- The slice stops before embeddings and Qdrant integration.
