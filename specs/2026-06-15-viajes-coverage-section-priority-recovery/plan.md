# Plan

## Objective

Prioritize substantive coverage sections for VIAJES coverage queries without changing product routing or contracts.

## Affected Files

- `ops/term-equivalences.json`
- `tests/test_retrieval.py`
- `specs/2026-06-15-viajes-coverage-section-priority-recovery/requirements.md`
- `specs/2026-06-15-viajes-coverage-section-priority-recovery/validation.md`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`

## Assumptions

- `SECCIÓN I QUÉ CUBRE ESTE SEGURO` chunks are already present in the VIAJES clausulados.
- Candidate-pool size is already sufficient once lexical expansion points at the right coverage surfaces.

## Risks

- Overly broad coverage terms could distort unrelated VIAJES policy queries.
- International and national queries must remain disambiguated by the existing document-name rules.

## Verification Strategy

- Run focused `pytest` and `ruff` for retrieval rules.
- Run live national retrieval and international grounded answering.
- Update roadmap and the acceptance matrix only if the row passes.
