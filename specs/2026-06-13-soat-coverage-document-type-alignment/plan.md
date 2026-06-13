# Plan

## Objective

Close the validated SOAT retrieval gap where coverage questions drift into
tariff documents instead of the clausulado.

## Affected Files

- `contracts/ingestion.py`
- `contracts/__init__.py`
- `rag/ingestion.py`
- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- SOAT is the only category that currently needs this corrective behavior.
- The smallest safe seam is operator-curated query rules, not a new caller API.

## Risks

- Over-broad query matching could redirect unrelated SOAT queries toward the
  wrong document type.
- Expansion terms could bias reranking too aggressively if they are not kept
  narrow.

## Verification Strategy

- run focused retrieval tests for query normalization behavior;
- run lint on touched Python modules;
- rerun real SOAT retrieval and answer commands against Qdrant and Groq.
