# Requirements

## Title

Diversify broad suscripción retrieval across distinct policy sections.

## Context

The suscripción retrieval path now clears the previous two issues:

- cleaned markdown and chunk metadata already expose semantic policy headings;
- broad suscripción prompts no longer surface heading-only stubs ahead of
  contentful body evidence.

One narrower gap remains in the live broad query surface:

- `cuáles son las políticas de suscripción de movilidad`
  now returns contentful chunks, but it can still place multiple chunks from
  the same subsection such as `14.1. Cotización de Pólizas Colectivas` before
  surfacing broader distinct policy sections.

This is now a breadth problem inside one correctly scoped and contentful
document family.

## Scope

This slice should:

1. preserve the current suscripción family scoping;
2. preserve the preference for contentful body evidence over heading-only
   stubs;
3. improve breadth for broad suscripción policy prompts so repeated subsection
   chunks do not dominate the first results.

This slice should not:

- reopen markdown normalization;
- introduce new ingestion steps;
- broaden into other mobility cohorts;
- redesign generic retrieval ranking beyond the smallest deterministic fix.

## Required Behavior

### 1. Distinct-section breadth

Acceptance criteria:

- for broad suscripción policy prompts, top retrieval results prefer distinct
  policy sections before repeating multiple chunks from the same subsection;
- if multiple chunks represent the same subsection, the richer one stays
  preferred;
- the behavior is deterministic and covered by focused tests.

### 2. Live retrieval improvement

Acceptance criteria:

- at least one broad suscripción live query returns contentful evidence from
  more than one distinct policy section in the first results;
- retrieval remains inside the suscripción document family.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records heading-stub prioritization as complete;
- the roadmap records this breadth-diversification slice as the next remaining
  suscripción slice.
