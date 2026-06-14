# Plan

## Objective

Correct the canonical classification seam for `UTILITARIO Y PESADOS` so the two
documents no longer masquerade as part of `MOVILIDAD/TRANSVERSALES`.

## Affected files

- `ops/document-metadata-overlays.json`
- `ops/term-equivalences.json`
- `core/query_scope.py`
- `tests/test_ingestion.py`
- `tests/test_query_scope.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- `data/raw/MOVILIDAD/UTILITARIO Y PESADOS/` is the intended canonical source
  location going forward;
- the duplicate copies under `MOVILIDAD/TRANSVERSALES/` are operational debt,
  not the intended source of truth;
- runtime artifacts can be regenerated after the classification seam is fixed.

## Risks

- explicit retrieval commands still using `--product movilidad` for this cohort
  will stop matching the corrected artifacts;
- stale local/Qdrant artifacts under the old ids can coexist until the operator
  reruns the documented migration commands;
- if supported-scope admission does not recognize category-specific wording,
  direct user queries such as `qué cubre el plan de utilitarios y pesados`
  could still be rejected upstream.

## Execution

1. Add the canonical `utilitarios y pesados` product aliases and keep the
   existing guide-family rule aligned with that product.
2. Move overlay ownership and ingestion expectations from the transversal ids to
   the canonical dedicated-category ids.
3. Update retrieval and ingestion tests to assert the new path/product/id
   contract.
4. Update roadmap notes and validation commands so the next operator run uses
   only the canonical category path.

## Verification strategy

- run focused `pytest` selections for ingestion, retrieval, and supported-scope
  coverage touching `utilitarios y pesados`;
- confirm the roadmap/spec text no longer describes the cohort as a transversal
  source of truth;
- leave live data migration as explicit operator commands in `validation.md`
  rather than silently mutating local/Qdrant state during the code fix.
