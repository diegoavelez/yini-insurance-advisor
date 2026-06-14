# Requirements

## Title

Recover semantic section structure for the `suscripción` transversal mobility
policy after PDFium fallback onboarding.

## Context

The baseline `suscripción` cohort is now operational:

- ingestion succeeded with the existing Docling-first seam by using a lower
  operational timeout that triggered the PDFium fallback for the 64-page PDF;
- embeddings succeeded;
- Qdrant indexing succeeded;
- live retrieval stayed inside the correct document family.

The remaining problem is now intra-document quality, not family scoping:

- the cleaned markdown still preserves page-oriented boilerplate such as
  `Volver al inicio`, `Page N`, and table-of-contents noise;
- chunk sections are generic page labels instead of policy headings;
- live retrieval can return weak fragments like `Terceros y Asistencia.` or
  `iarios` ahead of more semantic underwriting-policy evidence.

This means the next narrow slice should improve the extracted policy surface so
retrieval can use actual suscripción section structure.

## Scope

This slice should:

1. suppress recurring page boilerplate and table-of-contents noise for this
   policy surface;
2. promote stronger semantic section labels from the numbered suscripción
   headings already present in the text;
3. regenerate chunks and re-run suscripción retrieval queries.

This slice should not:

- broaden into other transversal documents;
- change document-family filters;
- redesign the global chunking architecture beyond the minimum normalization
  needed for this document shape;
- reopen unrelated PV, financing, or choque-simple logic.

## Required Behavior

### 1. Semantic policy surface recovery

Acceptance criteria:

- the suscripción cleaned markdown no longer leads primarily with page-level
  boilerplate and table-of-contents fragments;
- chunk sections become more meaningful than `Page N` for the retrieved
  evidence path;
- obviously broken fragment chunks are reduced or removed from early retrieval.

### 2. Retrieval quality improvement

Acceptance criteria:

- at least one suscripción-oriented live query returns chunks anchored to
  semantic policy sections rather than generic page labels;
- retrieval continues to stay inside the suscripción document family;
- if another gap remains after structure recovery, it is documented as a new
  narrow slice.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records the baseline suscripción slice as complete;
- the roadmap records this section-structure remediation as the next remaining
  suscripción slice.
