# Plan

## Objective

Bias broad ARL remuneration-policy retrieval toward explicit remuneration
evidence while preserving narrow scope and deterministic behavior.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/2026-06-14-arl-remuneracion-policy-intent-retrieval-alignment/requirements.md`
- `specs/2026-06-14-arl-remuneracion-policy-intent-retrieval-alignment/plan.md`
- `specs/2026-06-14-arl-remuneracion-policy-intent-retrieval-alignment/validation.md`
- `specs/roadmap.md`

## Assumptions

- Relevant remuneration chunks already exist in Qdrant but are under-ranked by
  generic semantic similarity.
- The existing deterministic reranking framework for movilidad policies can be
  reused safely for this ARL family.

## Risks

- Over-broad intent detection could affect unrelated ARL policy questions.
- Overweighting tables or numeric sections could prefer low-context table chunks
  over better explanatory remuneration chunks.

## Verification Strategy

- Add focused retrieval tests for broad remuneration-policy intent.
- Run targeted `pytest` and `ruff`.
- Validate live `retrieve-chunks` against Qdrant with the representative broad
  remuneration query.
