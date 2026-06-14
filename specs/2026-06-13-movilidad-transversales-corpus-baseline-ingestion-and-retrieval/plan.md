# Plan

## Objective

Onboard `MOVILIDAD/TRANSVERSALES` with the smallest truthful metadata baseline
needed for ingestion and later retrieval.

## Affected Files

- `ops/document-metadata-overlays.json`
- `tests/test_ingestion.py`
- `specs/roadmap.md`
- `specs/2026-06-13-movilidad-transversales-corpus-baseline-ingestion-and-retrieval/requirements.md`
- `specs/2026-06-13-movilidad-transversales-corpus-baseline-ingestion-and-retrieval/validation.md`

## Assumptions

- `TRANSVERSALES` is a shared mobility corpus, not a standalone product.
- `product=movilidad` is the correct first baseline.
- A more detailed retrieval split for `choque simple`, `utilitarios y pesados`,
  or financing can happen in later slices.

## Risks

- Some files may later deserve a narrower subtype or intent family than the
  baseline used here.
- The `ley 2251` document may ultimately want a more specific taxonomy than
  `guide`, but that is intentionally deferred.

## Verification Strategy

- Add a repository-level overlay coverage test for the current `TRANSVERSALES`
  corpus.
- Add one focused ingestion test proving the overlay is applied in runtime.
- Run focused `pytest` and `ruff`.
