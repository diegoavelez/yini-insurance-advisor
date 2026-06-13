# Plan

## Objective

Onboard `MOVILIDAD/BICICLETAS Y PATINETAS` into the current RAG baseline with the smallest taxonomy and retrieval alignment needed for real queries.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-bicicletas-patinetas-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-13-bicicletas-patinetas-corpus-baseline-ingestion-and-retrieval/validation.md`
- generated artifacts under `data/markdown/`, `data/processed/`, and `data/processed/embeddings/`

## Assumptions

- the existing `movilidad` product bucket is sufficient for bicycles and scooters in this phase;
- the three source PDFs are enough for a first retrieval baseline;
- current Docling/PDFium seams are adequate for these documents.

## Risks

- path/filename aliases may still miss some operator phrasing;
- the new category may reveal retrieval gaps distinct from AUTOS;
- generated artifacts may need a second narrow corrective slice if real queries underperform.

## Steps

1. Add minimal `movilidad` aliases for bicycles and scooters.
2. Add minimal `guide` alias coverage for `pv` artifacts.
3. Ingest the category corpus and persist metadata.
4. Generate embeddings and index the new artifacts.
5. Validate a few real retrieval queries and record any next gap.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched files;
- run ingestion, embeddings, indexing, and real retrieval commands for the category.
