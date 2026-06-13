# Plan

## Objective

Improve retrievability of structurally fragmented PDFs by prefixing missing section-path headings into chunk text.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-section-context-prefixed-chunk-remediation/requirements.md`
- `specs/2026-06-13-section-context-prefixed-chunk-remediation/validation.md`

## Assumptions

- headings carry important comparative vocabulary that embeddings need to see inside the chunk text;
- preserving section-path text is safer than product-specific retrieval heuristics;
- moderate chunk-length inflation is acceptable if deterministic and bounded.

## Risks

- duplicating headings when detection is too loose;
- slightly increasing chunk size beyond the previous soft target;
- affecting retrieval behavior for already-good documents.

## Steps

1. Add a helper that renders `section_path` into markdown headings.
2. Prefix that context only when the current chunk text does not already include it.
3. Add regression tests for follow-on chunk context retention and duplication avoidance.
4. Update roadmap with the corrective slice.

## Verification Strategy

- run focused chunking tests;
- run Ruff on touched files;
- inspect regenerated retrieval behavior for the AUTOS comparison query.
