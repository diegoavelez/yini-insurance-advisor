# Plan

## Objective

Close the PAC 60+ policy-family gap by regenerating stale artifacts when
metadata drifts and by pinning the remaining PAC policy intents to the correct
document family.

## Affected files

- `ops/term-equivalences.json`
- `rag/ingestion.py`
- `tests/test_embedding_generation.py`
- `tests/test_ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`

## Assumptions

- the stale-artifact path can be fixed safely without forcing operators into
  full `overwrite=true` reruns;
- broad PAC reranking is unnecessary if persisted metadata stays fresh and the
  remaining family disambiguation is handled deterministically;
- explicit asegurabilidad wording should remain mapped to the asegurabilidad
  family.

## Risks

- stale-artifact detection that is too weak would preserve bad persisted
  metadata and hide the true correction;
- overly broad PAC policy routing could hide legitimate asegurabilidad content;
- a clausulado-specific rule that depends on the current document title may
  need revisiting if PAC document-name normalization changes later.

## Execution

1. Make the incremental ingestion and embedding paths regenerate stale PAC
   artifacts when resolved metadata no longer matches persisted outputs.
2. Add focused PAC policy-family routing logic through the existing
   normalization seam.
3. Add regression coverage for stale-artifact refresh plus broad coverage,
   explicit clausulado, and asegurabilidad-preservation cases.
4. Validate live against Qdrant with the observed PAC queries.

## Verification strategy

- run focused `pytest` checks for stale-artifact refresh and PAC retrieval
  routing;
- confirm live retrieval moves broad coverage and explicit clausulado queries to
  the clausulado family;
- confirm asegurabilidad queries still stay in the asegurabilidad family.
