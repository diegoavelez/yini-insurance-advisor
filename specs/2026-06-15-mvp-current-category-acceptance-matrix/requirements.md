# Requirements

## Slice

`mvp-current-category-acceptance-matrix`

## Goal

Shift execution focus from additional `rag/ingestion.py` decoupling to MVP
acceptance evidence for the categories already onboarded in the current corpus.

## Context

The roadmap now records the currently onboarded corpus categories as completed
or operational for the current MVP scope, including the active `ARL` cohort and
the completed `MOVILIDAD` and `EPS/PAC` PDF cohorts. The remaining documented
post-onboarding coupling slices are structural improvements, but they are no
longer the highest-value next step if the immediate objective is to prove the
current MVP works reliably with the categories already available.

The next work should therefore establish an explicit MVP acceptance matrix over
the current category set before opening new onboarding waves or continuing
non-blocking coupling refactors.

## Requirements

1. The repository must document that MVP execution focus is now the currently
   onboarded category set, not additional category growth or non-blocking
   decoupling.
2. The slice must define an acceptance matrix for the current corpus categories
   already in scope, at minimum:
   - `ARL`
   - `MOVILIDAD/AUTOS`
   - `MOVILIDAD/BICICLETAS Y PATINETAS`
   - `MOVILIDAD/MOTOS`
   - `MOVILIDAD/TRANSVERSALES` including `choque simple`
   - `MOVILIDAD/PV`
   - `MOVILIDAD/UTILITARIO Y PESADOS`
   - `MOVILIDAD/FINANCIACION`
   - `MOVILIDAD/VIAJES`
   - `MOVILIDAD/SUSCRIPCION`
   - `MUEVETE LIBRE`
   - `MOVILIDAD/SOAT`
   - `EPS/PAC` PDF cohorts
3. For each category or category-family, the acceptance matrix must require:
   - at least one real retrieval query;
   - at least one real grounded-answer query;
   - explicit evidence of intended citations or documentary basis;
   - documented limitations where the category is operational but fragile.
4. The roadmap must explicitly defer remaining post-onboarding coupling slices
   until this MVP acceptance pass is complete, unless a coupling slice becomes
   necessary to unblock MVP behavior directly.

## Non-Goals

- onboarding new categories;
- rescoping the MVP to include unsupported `.docx` inputs;
- executing the full acceptance matrix in this slice;
- removing or cancelling the remaining coupling slices from the roadmap.
