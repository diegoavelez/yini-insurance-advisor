# Plan

## Objective

Reduce `rag/ingestion.py` coupling by extracting the stabilized ARL
remuneration-policy domain to a dedicated `rag` module while preserving
behavior.

## Affected Files

- `rag/ingestion.py`
- `rag/arl_remuneration.py`
- `specs/roadmap.md`
- `specs/2026-06-14-rag-arl-remuneration-domain-seam-extraction/requirements.md`
- `specs/2026-06-14-rag-arl-remuneration-domain-seam-extraction/plan.md`
- `specs/2026-06-14-rag-arl-remuneration-domain-seam-extraction/validation.md`

## Assumptions

- The current ARL remuneration behavior is correct and should be preserved.
- The domain can be extracted without pulling unrelated ingestion helpers into
  the same slice.

## Risks

- Import boundaries could accidentally change helper behavior if shared utility
  logic is reimplemented incorrectly.
- A partial extraction could leave stale duplicate logic in `rag/ingestion.py`.

## Verification Strategy

- Run focused ARL remuneration tests.
- Run a focused lint check on touched files.
- Run one live `answer-query` validation for the broad ARL remuneration query.
