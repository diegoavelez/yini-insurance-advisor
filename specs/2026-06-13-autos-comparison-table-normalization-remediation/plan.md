# Plan

## Objective

Make comparison tables more retrievable by converting structured markdown-table text into semantic plan-oriented statements before chunking.

## Affected Files

- `rag/ingestion.py`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-autos-comparison-table-normalization-remediation/requirements.md`
- `specs/2026-06-13-autos-comparison-table-normalization-remediation/validation.md`

## Assumptions

- the comparative information is present but encoded too literally as table rows;
- deterministic table-to-text normalization is safer than adding lexical retrieval fallback first;
- the same approach may help similar structured PDFs beyond AUTOS.

## Risks

- misreading malformed tables and emitting low-quality prose;
- duplicating content if both raw and normalized forms survive together;
- increasing text volume beyond what helps embeddings.

## Steps

1. Add a narrow helper that recognizes markdown table-like blocks with plan labels.
2. Convert qualifying rows into semantic statements.
3. Use the normalized block text in chunk generation.
4. Add focused tests for positive and negative cases.
5. Regenerate, re-embed, reindex, and measure the AUTOS comparison retrieval.

## Verification Strategy

- run focused ingestion tests;
- run Ruff on touched files;
- regenerate the comparative artifact path and measure retrieval again.
