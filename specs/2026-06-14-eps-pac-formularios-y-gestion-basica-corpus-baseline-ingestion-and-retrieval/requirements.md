# Requirements

## Title

Baseline-ingest the `EPS/PLAN COMPLEMENTARIO PAC` forms and basic-operations
cohort after the completed `PAC 60+ core` baseline.

## Context

The next truthful PAC slice is the short operational cohort that stays separate
from the longer instructivos, heavy PDFs, and unsupported `.docx` assets.

This cohort contains:

- `formulario de afiliacion pac v2.pdf`
- `formato firma cliente pac v1.pdf`
- `politica cambio de asesor pac v4.pdf`
- `tips medios de pago v3.pdf`

It should be onboarded as one narrow operational cohort because:

- the documents are short and process-oriented;
- they are not broad product-coverage evidence;
- they should validate PAC operational retrieval without reopening the `PAC 60+`
  policy baseline.

## Scope

This slice should:

1. add canonical metadata support for the four operational PAC PDFs under
   `product=pac`;
2. create one dated baseline bundle for this cohort only;
3. validate operational retrieval for affiliation, client-signature,
   advisor-change, and payment-media questions;
4. keep the remaining PAC folder content explicitly deferred by cohort.

This slice should not:

- reopen the `PAC 60+ core` policy baseline;
- onboard the long instructivos in the same run;
- onboard the two large PAC PDFs in the same run;
- add `.docx` support;
- broaden into all remaining PAC files.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- overlay-backed metadata persists:
  - `formulario de afiliacion` as `form`
  - `formato firma cliente` as `form`
  - `politica cambio de asesor` as `policy`
  - `tips medios de pago` as `guide`;
- all four documents persist with canonical `product=pac`.

### 2. Narrow cohort boundary

Acceptance criteria:

- the slice targets only the four operational PDFs listed above;
- the following remain explicitly deferred:
  - short Global Web guides
  - long instructivos
  - large isolated PDFs
  - unsupported `.docx`
  - `politicas asegurabilidad pac v16.pdf` as a future PAC policy cohort.

### 3. Retrieval validation

Acceptance criteria:

- `¿Cómo diligencio el formulario de afiliación PAC?` retrieves the
  `formulario de afiliacion pac v2.pdf` family;
- `¿Cómo funciona el formato de firma del cliente PAC?` retrieves the
  `formato firma cliente pac v1.pdf` family;
- `¿Cómo se hace el cambio de asesor en PAC?` retrieves the
  `politica cambio de asesor pac v4.pdf` family;
- `¿Qué medios de pago tiene PAC?` retrieves the `tips medios de pago v3.pdf`
  family;
- if deterministic routing is required after live evidence, it must stay
  narrowly scoped to this cohort.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects that PAC follow-on cohorts remain active after the
  completed `PAC 60+ core` slice;
- the spec bundle records the exact operator sequence for this cohort;
- the validation file records the remaining deferred PAC groups.
