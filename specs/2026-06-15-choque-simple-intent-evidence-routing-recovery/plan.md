# Plan

## Objective

Separate photo-intent and procedure-intent evidence routing inside the choque simple transversal family.

## Affected Files

- `ops/term-equivalences.json`
- `rag/evidence_selection.py`
- `tests/test_retrieval.py`
- `specs/2026-06-15-choque-simple-intent-evidence-routing-recovery/requirements.md`
- `specs/2026-06-15-choque-simple-intent-evidence-routing-recovery/validation.md`
- `specs/roadmap.md`
- `specs/2026-06-15-mvp-current-category-acceptance-matrix/matrix.md`

## Assumptions

- The current corpus already includes `como tomar fotos choque simple v2.pdf`, `proceso atencion choque simple v2.pdf`, and `circular choque simple.pdf`.
- Candidate pool size is already sufficient once intent-specific recall and reranking are in place.

## Risks

- Over-broad photo keywords could hijack generic choque simple questions.
- Procedure prioritization must not discard the circular when it is the clearest normative support.

## Verification Strategy

- Run focused `pytest` and `ruff`.
- Run live photo retrieval and live procedure answering.
- Update roadmap and matrix only if the row passes.
