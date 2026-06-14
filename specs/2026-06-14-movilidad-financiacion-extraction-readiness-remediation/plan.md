# Plan

## Objective

Recover a usable extraction and chunking surface for
`instructivo financiacion de polizas v1.pdf` before attempting financing
retrieval alignment.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-financiacion-extraction-readiness-remediation/requirements.md`
- `specs/2026-06-14-movilidad-financiacion-extraction-readiness-remediation/plan.md`
- `specs/2026-06-14-movilidad-financiacion-extraction-readiness-remediation/validation.md`

## Assumptions

- the current failure is primarily extraction-related rather than a pure
  retrieval-ranking miss;
- the raw document contains more real financing content than the current
  single-token artifact shows;
- recovery may come from normalization or backend handling, not necessarily a
  taxonomy change.

## Risks

- the source PDF may be highly image-based or structurally degraded;
- extraction recovery may require a document-specific fallback path;
- financing retrieval might still need a later scope/ranking slice even after
  extraction improves.

## Steps

1. Inspect the raw/processed financing artifacts to characterize extraction collapse.
2. Apply the smallest extraction-focused remediation that restores usable text.
3. Rebuild cleaned markdown, chunks, embeddings, and index for this document.
4. Re-run financing retrieval queries.
5. Open a new retrieval corrective slice only if needed after extraction is fixed.

## Verification Strategy

- inspect the recovered cleaned markdown directly;
- confirm chunk count and chunk text are materially improved;
- re-run live financing retrieval queries.
