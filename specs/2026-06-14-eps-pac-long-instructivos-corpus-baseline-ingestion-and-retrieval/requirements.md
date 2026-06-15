# Requirements

## Title

Baseline-ingest the long `EPS/PLAN COMPLEMENTARIO PAC` instructivos cohort.

## Context

After the completed `PAC 60+ core`, `formularios / gestión básica`, and
`Global Web` cohorts, the next truthful PAC slice is the isolated long
instructivos cohort:

- `instructivo inclusion de asegurados cotizador v2.pdf`
- `instructivo formularios web novedades pac v6.pdf`

This cohort is the correct next step because:

- both PDFs belong to the same operational instructivos family;
- both are materially longer than the short PAC guides and therefore deserve an
  isolated extraction and retrieval pass;
- validating them together preserves a narrow cohort without mixing in the
  heavy isolated PAC PDFs.

## Scope

This slice should:

1. add canonical metadata support for the two long instructivos under
   `product=pac`;
2. create one dated baseline bundle for this cohort only;
3. validate retrieval for:
   - including insured members in the PAC quote flow,
   - managing PAC web forms and novedades;
4. keep the remaining PAC folder content deferred by cohort.

This slice should not:

- reopen `PAC 60+ core`, PAC forms, or `Global Web`;
- onboard `politicas asegurabilidad pac v16.pdf` in the same run;
- onboard `informacion canales transaccionales y apoyo v1.pdf`;
- onboard `clausulado pac tradicional sura v1.pdf`;
- add `.docx` support;
- broaden into all remaining PAC files.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- both documents persist with canonical `product=pac`;
- overlay-backed metadata persists both as `document_type=guide`.

### 2. Narrow cohort boundary

Acceptance criteria:

- the slice targets only the two long instructivos;
- the following remain explicitly deferred:
  - `politicas asegurabilidad pac v16.pdf`
  - `informacion canales transaccionales y apoyo v1.pdf`
  - `clausulado pac tradicional sura v1.pdf`
  - unsupported `.docx`.

### 3. Retrieval validation

Acceptance criteria:

- a query about including insured members in the PAC quote flow retrieves the
  `inclusion de asegurados cotizador` family;
- a query about PAC web forms or novedades retrieves the `formularios web
  novedades` family;
- if deterministic routing is required after live evidence, it remains narrowly
  scoped to this cohort.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects that PAC follow-on cohorts remain active after this
  cohort;
- the spec bundle records the exact operator sequence for this cohort;
- the validation file records the remaining deferred PAC groups.
