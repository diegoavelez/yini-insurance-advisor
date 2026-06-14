# Requirements

## Title

Baseline-ingest the `EPS/PLAN COMPLEMENTARIO PAC` `PAC 60+ core` cohort and
document the remaining onboarding sequence for the folder.

## Context

The `data/raw/EPS/PLAN COMPLEMENTARIO PAC/` folder is the next post-movilidad
category candidate, but it is operationally mixed:

- it contains a coherent `PAC 60+` product cohort;
- it contains shorter operational PAC forms and Global Web guides;
- it contains two longer instructivos that should stay isolated;
- it contains two large PDF outliers that should run one by one;
- it contains two `.docx` files that are out of scope for the current
  PDF-only ingestion tooling.

The next truthful slice is not the full folder. It is the narrow
`PAC 60+ core` baseline cohort:

- `clausulado pac 60 mas sura v1.pdf`
- `politicas asegurabilidad pac 60 mas.pdf`
- `preguntas frecuentes pac 60 mas.pdf`
- `tips asesores pac 60 mas v2.pdf`
- `tarifas pac con iva 2026.pdf`

## Scope

This slice should:

1. add canonical metadata support for the `PAC 60+ core` PDFs under
   `product=pac`;
2. admit direct PAC queries into supported scope;
3. create one dated baseline bundle for the `PAC 60+ core` cohort only;
4. document the deferred cohort sequence for the rest of the folder;
5. explicitly defer the two `.docx` files until the repo supports non-PDF
   ingestion.

This slice should not:

- ingest the whole `EPS/PLAN COMPLEMENTARIO PAC` folder in one run;
- add `.docx` ingestion support;
- onboard the two large PDF outliers into the baseline cohort;
- add PAC-specific reranking or document-family routing before live evidence.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- path-derived product inference resolves `EPS/PLAN COMPLEMENTARIO PAC/` to
  the canonical product `pac`;
- `PAC 60+` aliases normalize into `product=pac`;
- overlay-backed metadata persists:
  - `clausulado` as `policy`
  - `politicas asegurabilidad` as `policy`
  - `preguntas frecuentes` as `faq`
  - `tips asesores` as `guide`
  - `tarifas` as `guide`;
- supported-scope admission recognizes direct PAC product queries.

### 2. Narrow cohort boundary

Acceptance criteria:

- the baseline bundle targets only the five `PAC 60+ core` PDFs;
- the remaining PDFs are explicitly grouped into deferred cohorts:
  - forms / gestión básica
  - short Global Web guides
  - long instructivos
  - large isolated PDFs;
- the two `.docx` files are documented as deferred, not silently ignored.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records `PAC 60+` as the next planned onboarding target;
- the spec bundle records the exact operator sequence for the baseline cohort;
- the validation file records the deferred cohorts and the large-PDF isolation
  rule so future onboarding stays consistent.

