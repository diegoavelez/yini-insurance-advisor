# Requirements

## Title

Normalize subsection lineage for suscripción collective-policy headings.

## Context

The suscripción retrieval path now resolves the previous ranking issues:

- broad queries no longer return heading-only stubs first;
- broad queries now surface distinct contentful policy sections in the top
  results.

One narrower structural gap remains in the extracted section labels:

- under `14. PÓLIZAS COLECTIVAS`, some child headings still surface as
  `2.1. Facturación agrupada` and
  `2.2. Facturación (cobro) agrupada con devolución por asegurado`
  instead of preserving the parent `14.*` lineage.

This is now a subsection-label normalization problem inside the same
suscripción document family.

## Scope

This slice should:

1. preserve the current suscripción ranking behavior;
2. normalize mis-scoped subsection headings under collective-policy sections;
3. keep the fix narrow and document-specific if necessary.

This slice should not:

- reopen retrieval ranking logic beyond what is already working;
- broaden into other mobility documents;
- redesign the general chunking algorithm without evidence.

## Required Behavior

### 1. Subsection lineage recovery

Acceptance criteria:

- child headings under `14. PÓLIZAS COLECTIVAS` preserve consistent lineage in
  cleaned markdown and chunk metadata;
- mis-scoped headings like `2.1` and `2.2` no longer appear as if they were
  top-level subsection numbers inside that section;
- the fix is deterministic and covered by focused tests.

### 2. Retrieval traceability improvement

Acceptance criteria:

- at least one live suscripción retrieval result shows normalized collective
  subsection labels where the current artifacts were previously inconsistent;
- retrieval remains inside the suscripción document family.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records breadth diversification as complete;
- the roadmap records this subsection-lineage slice as the next remaining
  suscripción slice.
