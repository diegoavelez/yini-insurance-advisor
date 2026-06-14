# Plan

## Objective

Onboard the next short PAC operational cohort without mixing it with the longer
or heavier deferred PAC documents.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json` if live evidence requires narrow routing
- `tests/test_ingestion.py`
- `tests/test_retrieval.py` if live evidence requires narrow routing
- `specs/roadmap.md`

## Assumptions

- the four targeted PDFs already exist under `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- path-derived `product=pac` remains stable;
- operational PAC questions can be validated independently from the `PAC 60+`
  policy cohort.

## Risks

- short operational PDFs may expose noisy titles or weak semantic retrieval;
- broad PAC wording may drift back toward the already indexed `PAC 60+`
  documents unless the live evidence is checked carefully;
- the extra `politicas asegurabilidad pac v16.pdf` file can create operator
  ambiguity if it is not documented as deferred.

## Execution

1. Add overlays and regression coverage for the four cohort documents.
2. Create the dated spec bundle and update roadmap status for PAC follow-on
   onboarding.
3. Run ingestion, embeddings, and indexing for the four documents only.
4. Validate live retrieval with the four operational PAC queries.
5. If a narrow deterministic routing rule is required, apply it with focused
   tests and evidence.

## Verification strategy

- run focused `pytest` checks for PAC overlay coverage and any new retrieval
  routing;
- confirm ingestion, embeddings, and indexing complete for the four files;
- confirm the four operational PAC queries retrieve the intended document
  families.
