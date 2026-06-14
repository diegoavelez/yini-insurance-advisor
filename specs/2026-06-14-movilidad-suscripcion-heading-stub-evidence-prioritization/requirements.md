# Requirements

## Title

Prefer contentful suscripción policy evidence over bare section-heading stubs.

## Context

The suscripción section-structure remediation is now complete:

- fallback page boilerplate is suppressed;
- semantic policy headings are restored in cleaned markdown and chunk metadata;
- live retrieval stays inside the correct policy family.

One narrower quality gap remains in live retrieval:

- for broad policy questions such as
  `cuáles son las políticas de suscripción de movilidad`,
  heading-only chunks like `13. PROCEDIMIENTOS` and `14. PÓLIZAS COLECTIVAS`
  can still outrank richer chunks that actually contain underwriting-policy
  substance.

This is no longer a family-scoping or structure-recovery problem. It is now a
retrieval-quality issue about preferring contentful evidence over bare heading
stubs within the same document family.

## Scope

This slice should:

1. detect heading-only or near-empty suscripción chunks in the reranking path;
2. prefer richer intra-section chunks for broad suscripción policy queries;
3. preserve the current family scoping and semantic section labels.

This slice should not:

- reopen page-boilerplate cleanup;
- introduce new document-family filters;
- broaden into other mobility transversal cohorts;
- redesign the global ranking architecture beyond the smallest deterministic
  fix.

## Required Behavior

### 1. Heading-stub demotion

Acceptance criteria:

- heading-only suscripción chunks receive lower priority than contentful chunks
  from the same policy family when both are candidates;
- the fix is deterministic and testable;
- non-suscripción retrieval behavior remains unchanged unless the same generic
  pattern is already intentionally covered.

### 2. Retrieval evidence improvement

Acceptance criteria:

- for at least one broad suscripción policy query, live top-k retrieval returns
  a richer body chunk ahead of bare heading-only stubs;
- retrieval still stays inside the suscripción document family;
- if another issue remains after this fix, it is documented as a new narrow
  slice.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records the section-structure slice as complete;
- the roadmap records this heading-stub evidence prioritization slice as the
  next remaining suscripción slice.
