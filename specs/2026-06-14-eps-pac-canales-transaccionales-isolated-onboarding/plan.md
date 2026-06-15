# Plan

## Objective

Onboard the final PAC operational support PDF and close the PAC category in the
current roadmap scope.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json` if live evidence requires narrow routing
- `tests/test_ingestion.py`
- `tests/test_retrieval.py` if live evidence requires narrow routing
- `specs/roadmap.md`

## Assumptions

- the targeted PDF already exists under `data/raw/EPS/PLAN COMPLEMENTARIO PAC/`;
- the document belongs to an operational/support lane, not the PAC policy lane;
- the document can be validated independently from previous PAC cohorts.

## Risks

- the document is large and may take a longer Docling path;
- the extracted `document_name` may be noisy, requiring a narrow deterministic
  pin for operator-friendly retrieval;
- the PDF may be highly visual, reducing markdown quality.

## Execution

1. Add the overlay and regression coverage for the remaining PAC PDF.
2. Ingest, embed, and index the PDF in isolation.
3. Inspect extracted metadata and live retrieval evidence.
4. If needed, add a narrow PAC transactional/support routing rule plus focused
   tests.
5. Update roadmap and validation evidence to mark PAC completed.

## Verification strategy

- run focused `pytest` checks for overlay coverage and any new retrieval
  routing;
- confirm ingestion, embeddings, and indexing complete for the PDF;
- confirm at least one PAC transactional/support query retrieves the intended
  document family first.
