# Plan

## Objective

Refine ARL remuneration-policy reranking so overview queries prefer explanatory
chunks and explicit percentage queries prefer table chunks.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/2026-06-14-arl-remuneracion-policy-overview-vs-table-priority/requirements.md`
- `specs/2026-06-14-arl-remuneracion-policy-overview-vs-table-priority/plan.md`
- `specs/2026-06-14-arl-remuneracion-policy-overview-vs-table-priority/validation.md`
- `specs/roadmap.md`

## Assumptions

- The existing ARL remuneration intent reranking is the right place to encode
  overview-vs-table preference.
- Query wording gives enough lexical signal to distinguish broad overview prompts
  from explicit table/percentage prompts.

## Risks

- Table-intent detection may be too weak and accidentally demote explicit
  percentage questions.
- Overview preference may be too strong and suppress useful commission tables in
  broad but semi-specific prompts.

## Verification Strategy

- Add focused retrieval tests for overview and table intents.
- Run targeted `pytest` and `ruff`.
- Validate live `retrieve-chunks` for one broad remuneration query and one
  explicit percentage/table query.
