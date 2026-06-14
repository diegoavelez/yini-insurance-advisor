# Requirements

## Title

Reclassify `UTILITARIO Y PESADOS` from duplicated transversal onboarding to its
own canonical movilidad category.

## Context

The two `utilitarios y pesados` PDFs were onboarded under
`MOVILIDAD/TRANSVERSALES`, but the raw corpus actually exists under the
dedicated folder `MOVILIDAD/UTILITARIO Y PESADOS/` and should be treated as its
own category rather than a shared transversal cohort.

That mistaken assumption leaks into:

- metadata overlays and persisted `source_pdf_id` expectations;
- retrieval tests and manual validation commands;
- roadmap notes that describe the cohort as transversal;
- path-derived product inference, which currently has no canonical
  `utilitarios y pesados` product branch.

The next narrow corrective slice should fix the canonical classification seam
without broadening into a full mobility-taxonomy redesign.

## Scope

This slice should:

1. establish `MOVILIDAD/UTILITARIO Y PESADOS/` as the canonical raw path;
2. persist the cohort under a dedicated canonical product
   `utilitarios y pesados`;
3. update overlays, retrieval normalization, tests, and roadmap references to
   that canonical classification;
4. document the reingestion/indexing commands required to migrate runtime
   artifacts after the code correction.

This slice should not:

- redesign other movilidad categories;
- automatically delete old local artifacts or Qdrant points;
- broaden into additional document-family ranking work beyond preserving the
  existing guide/policy behavior.

## Required Behavior

### 1. Canonical category and product

Acceptance criteria:

- path-derived ingestion from `MOVILIDAD/UTILITARIO Y PESADOS/` resolves to the
  canonical product `utilitarios y pesados`;
- the canonical `source_pdf_id` values derive from the dedicated folder slug
  `movilidad__utilitario-y-pesados__...`;
- overlay-backed persisted metadata for the two PDFs uses those canonical ids
  and the dedicated product.

### 2. Retrieval compatibility

Acceptance criteria:

- the existing operator-curated guide-family rule for
  `Seguro de Autos Utilitarios y Pesados` remains active;
- when no explicit product filter is provided, the narrow guide-intent rule can
  still inject the canonical product/document family;
- canonical product filters for `utilitarios y pesados` are accepted by the
  normalization layer and targeted tests.

### 3. Transversal separation

Acceptance criteria:

- `movilidad-transversales` overlay coverage and tests no longer list the two
  `utilitarios y pesados` PDFs as shared transversal documents;
- retrieval fixtures referencing those PDFs use the dedicated category path and
  product.

### 4. Documentation and migration traceability

Acceptance criteria:

- the roadmap records that the previous transversal assumption was superseded by
  a category reclassification remediation;
- the spec bundle documents the exact batch commands needed to reingest,
  re-embed, re-index, and validate the canonical category after the code change.
