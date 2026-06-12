# Validation

## Status

- Planned on `2026-06-12`.
- Completed on `2026-06-12`.

## Required Checks

- A committed operator-curated equivalence file exists.
- Retrieval query aliases normalize deterministically.
- Retrieval filter aliases normalize deterministically.

## Required Scenarios

- A Spanish alias in the user query appends the configured canonical term.
- A product filter alias maps to the canonical product before Qdrant filtering.
- Existing retrieval behavior remains unchanged for unaffected values.

## Merge Readiness

This slice is ready when the operator has one explicit equivalence table and the
retrieval path uses it narrowly for deterministic normalization.

## Evidence

- A committed operator-curated equivalence file now exists at:
  - `ops/term-equivalences.json`
- Retrieval query alias expansion is covered by focused regression validation:
  - `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
  - includes a case where `carro` appends canonical `auto` before embedding
    generation.
- Retrieval filter alias canonicalization is covered by focused regression
  validation:
  - `./.venv/bin/python -m pytest tests/test_retrieval.py -q`
  - includes a case where product filter alias `vehículo` maps to canonical
    `auto` before Qdrant filter construction.
- The README now documents:
  - incremental `data/raw/` accumulation with `--overwrite false`;
  - the operator rule that term-equivalence canonical values should stay
    aligned with metadata-overlay canonical values.

## Recorded Outcome

- The repository now has one explicit operator-curated term-equivalence seam
  for incremental Spanish corpus growth.
- Retrieval normalization remains narrow, deterministic, and traceable to the
  curated file rather than to speculative synonym inference.
- The backend contract did not need redesign; the change fits inside the
  current retrieval normalization layer.
