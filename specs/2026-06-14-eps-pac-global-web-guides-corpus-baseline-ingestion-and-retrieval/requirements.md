# Requirements

## Title

Baseline-ingest the `EPS/PLAN COMPLEMENTARIO PAC` `Global Web` guides cohort.

## Context

After the completed `PAC 60+ core` and `formularios / gestión básica` cohorts,
the next truthful PAC slice is the short `Global Web` guides cohort:

- `instructivo actualizacion correo para factura global web v2.pdf`
- `instructivo descarga carta de declinacion y pospuestos global web v2.pdf`
- `instructivo informe de relacion de asegurados global web v2.pdf`

This cohort is the correct next step because:

- all three PDFs belong to the same operational family;
- all three are short and low-risk compared with the long instructivos;
- they can be validated through process-oriented retrieval without reopening the
  broader PAC folder.

## Scope

This slice should:

1. add canonical metadata support for the three `Global Web` PDFs under
   `product=pac`;
2. create one dated baseline bundle for this cohort only;
3. validate retrieval for:
   - updating the email used for billing,
   - downloading declination/pospuestos letters,
   - obtaining the insured-members report;
4. keep the remaining PAC folder content deferred by cohort.

This slice should not:

- reopen `PAC 60+ core` or the PAC forms cohort;
- onboard the long instructivos in the same run;
- onboard the two large PAC PDFs in the same run;
- add `.docx` support;
- broaden into all remaining PAC files.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- the three documents persist with canonical `product=pac`;
- overlay-backed metadata persists all three as `document_type=guide`.

### 2. Narrow cohort boundary

Acceptance criteria:

- the slice targets only the three `Global Web` guide PDFs;
- the following remain explicitly deferred:
  - long instructivos
  - large isolated PDFs
  - `politicas asegurabilidad pac v16.pdf`
  - unsupported `.docx`.

### 3. Retrieval validation

Acceptance criteria:

- `¿Cómo actualizar el correo para factura global web en PAC?` retrieves the
  `actualizacion correo` family;
- `¿Cómo descargar la carta de declinación y pospuestos en PAC?` retrieves the
  `declinacion y pospuestos` family;
- `¿Cómo obtener el informe de relación de asegurados en PAC?` retrieves the
  `relacion de asegurados` family;
- if deterministic routing is required after live evidence, it remains narrowly
  scoped to this cohort.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects that PAC follow-on cohorts remain active after this
  cohort;
- the spec bundle records the exact operator sequence for this cohort;
- the validation file records the remaining deferred PAC groups.
