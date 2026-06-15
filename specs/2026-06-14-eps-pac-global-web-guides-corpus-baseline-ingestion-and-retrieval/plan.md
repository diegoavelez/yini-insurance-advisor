# Plan

## Objective

Onboard the short `Global Web` PAC guides as one isolated operational cohort.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json` if live evidence requires narrow routing
- `tests/test_ingestion.py`
- `tests/test_retrieval.py` if live evidence requires narrow routing
- `specs/roadmap.md`

## Assumptions

- the three targeted PDFs already exist under `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- path-derived `product=pac` remains stable;
- the cohort can be validated independently from the long instructivos and
  heavy PAC PDFs.

## Risks

- the three guides may surface noisy or generic marketing titles;
- broad PAC operational wording may drift into previously indexed PAC cohorts
  unless live retrieval is checked carefully;
- one or more process intents may need explicit family routing after first
  evidence.

## Execution

1. Add overlays and regression coverage for the three `Global Web` guides.
2. Create the dated spec bundle and update roadmap status for PAC follow-on
   onboarding.
3. Run ingestion, embeddings, and indexing for the three documents only.
4. Validate live retrieval with the three operational `Global Web` queries.
5. If needed, add narrow deterministic routing plus focused tests.

## Verification strategy

- run focused `pytest` checks for PAC overlay coverage and any new retrieval
  routing;
- confirm ingestion, embeddings, and indexing complete for the three files;
- confirm the three `Global Web` PAC queries retrieve the intended document
  families.
