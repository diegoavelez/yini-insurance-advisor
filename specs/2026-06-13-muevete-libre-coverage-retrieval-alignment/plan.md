# Plan

## Objective

Improve `Muévete Libre` coverage-intent retrieval so policy coverage sections
outrank adjacent generic sections for queries such as
`¿Qué cubre Muévete Libre?`.

## Affected Files

- `ops/term-equivalences.json`
- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-13-muevete-libre-coverage-retrieval-alignment/requirements.md`
- `specs/2026-06-13-muevete-libre-coverage-retrieval-alignment/validation.md`

## Assumptions

- The current Docling output for `Muévete Libre` is sufficiently faithful for
  retrieval and does not need another ingestion-time normalization pass.
- The remaining gap is deterministic retrieval ranking rather than grounding or
  answer synthesis.

## Risks

- A coverage-intent preference that is too broad could affect unrelated
  products.
- Over-curated expansion terms could become too document-specific if the
  category corpus changes substantially.

## Verification Strategy

- Add focused unit tests for query normalization and retrieval ranking.
- Run focused `pytest` and `ruff` checks locally.
- Run one real `retrieve-chunks` and one real `answer-query` validation against
  Qdrant/Groq after implementation.
