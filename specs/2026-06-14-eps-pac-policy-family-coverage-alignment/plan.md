# Plan

## Objective

Onboard the general PAC asegurabilidad policy and remove the remaining
`PAC 60+` overcapture on general asegurabilidad queries.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- `politicas asegurabilidad pac v16.pdf` already exists under
  `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- the current PAC retrieval gap is caused by overly broad `PAC 60+`
  asegurabilidad routing rather than a missing backend capability;
- the general PAC policy can be onboarded independently from the large isolated
  PDFs.

## Risks

- the extracted `document_name` for `v16` may be noisy, forcing a narrow
  deterministic pin;
- changing PAC `60+` rules too broadly could regress the validated `60 Más`
  family behavior;
- general PAC coverage queries may still remain unresolved until the heavy
  clausulado family is onboarded later.

## Execution

1. Add the `v16` overlay and regression coverage for policy metadata.
2. Ingest, embed, and index the `v16` policy only.
3. Inspect the extracted `document_name` and live retrieval evidence.
4. Narrow the `PAC 60+` asegurabilidad rule and add a general PAC
   asegurabilidad rule if needed.
5. Validate live retrieval for both `PAC 60+` and general PAC asegurabilidad
   intents.
6. Update roadmap and validation evidence.

## Verification strategy

- run focused `pytest` checks for PAC policy overlays and retrieval
  normalization;
- confirm ingestion, embeddings, and indexing complete for the `v16` policy;
- confirm `PAC 60+` and general PAC asegurabilidad retrievals land on the
  intended document families.
