# Requirements

## Title

Prefer the clean leading billing chunk within suscripción collective billing.

## Context

The suscripción retrieval path now resolves the prior billing-intent issue:

- prompts about `facturación de pólizas colectivas` now rank the `14.6.*`
  collective billing subtree ahead of `13.11` financing-individual content.

One narrower intra-section quality gap remains:

- inside `14.6.2. Facturación (cobro) agrupada con devolución por asegurado`,
  the live top result can still surface a later fragment that begins with
  `onciliación.` even though an earlier chunk from the same subsection contains
  a cleaner and more complete explanation lead.

This is now a within-subsection evidence-quality problem, not a family, intent,
or structure problem.

## Scope

This slice should:

1. preserve the existing collective billing intent alignment;
2. prefer the cleaner leading chunk when multiple chunks belong to the same
   `14.6.2` subsection;
3. keep the fix deterministic and narrow to this documented pattern.

This slice should not:

- reopen markdown normalization;
- broaden into generic chunk-quality ranking for the whole repository;
- redesign the global retrieval algorithm beyond the smallest safe fix.

## Required Behavior

### 1. Leading-chunk preference

Acceptance criteria:

- when multiple chunks share the same `14.6.2` subsection, the chunk with the
  cleaner and more complete billing explanation lead ranks ahead of late
  fragmentary continuation chunks;
- the fix is deterministic and covered by focused tests;
- the earlier collective billing intent alignment remains intact.

### 2. Live retrieval improvement

Acceptance criteria:

- at least one live collective billing query returns the cleaner `14.6.2`
  chunk ahead of later fragmentary chunks from the same subsection;
- retrieval remains inside the suscripción document family.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records collective-billing intent alignment as complete;
- the roadmap records this leading-chunk prioritization slice as the next
  remaining suscripción slice.
