# Plan

## Objective

Onboard the traditional PAC clausulado and remove the remaining `PAC 60+`
overcapture on generic PAC coverage queries.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- `clausulado pac tradicional sura v1.pdf` already exists under
  `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- the current PAC coverage gap is caused by overly broad `PAC 60+`
  clausulado routing rather than a missing backend capability;
- the traditional clausulado can be onboarded independently from the remaining
  operational support PDF.

## Risks

- the extracted `document_name` for the traditional clausulado may be noisy,
  requiring a narrow deterministic pin;
- changing PAC `60+` clausulado rules too broadly could regress the validated
  `60 Más` family behavior;
- the large PDF may take a longer Docling path, so the slice should keep the
  run isolated.

## Execution

1. Add the traditional clausulado overlay and regression coverage.
2. Ingest, embed, and index the traditional clausulado only.
3. Inspect the extracted `document_name` and live retrieval evidence.
4. Narrow the `PAC 60+` clausulado rules and add a general PAC clausulado rule
   if needed.
5. Validate live retrieval for both `PAC 60+` and generic PAC coverage intents.
6. Update roadmap and validation evidence.

## Verification strategy

- run focused `pytest` checks for PAC policy overlays and retrieval
  normalization;
- confirm ingestion, embeddings, and indexing complete for the traditional
  clausulado;
- confirm `PAC 60+` and generic PAC coverage retrievals land on the intended
  document families.
