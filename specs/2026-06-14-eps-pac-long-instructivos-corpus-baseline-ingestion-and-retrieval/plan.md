# Plan

## Objective

Onboard the long PAC instructivos as one isolated operational cohort.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json` if live evidence requires narrow routing
- `tests/test_ingestion.py`
- `tests/test_retrieval.py` if live evidence requires narrow routing
- `specs/roadmap.md`

## Assumptions

- the two targeted PDFs already exist under `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- path-derived `product=pac` remains stable;
- the cohort can be validated independently from the short PAC guides and heavy
  isolated PAC PDFs.

## Risks

- the long instructivos may surface generic or noisy headings as extracted
  `document_name` values;
- long operational documents may generate broad chunks that drift into adjacent
  PAC cohorts unless live retrieval is checked carefully;
- one or both process intents may need explicit family routing after first
  evidence.

## Execution

1. Add overlays and regression coverage for the two long PAC instructivos.
2. Create the dated spec bundle for this cohort.
3. Run ingestion, embeddings, and indexing for the two documents only.
4. Validate live retrieval with one query per instructivo family.
5. If needed, add narrow deterministic routing plus focused tests.
6. Update roadmap and validation evidence once the cohort is confirmed.

## Verification strategy

- run focused `pytest` checks for PAC overlay coverage and any new retrieval
  routing;
- confirm ingestion, embeddings, and indexing complete for the two files;
- confirm the two PAC instructivo queries retrieve the intended document
  families.
