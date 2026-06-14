# Requirements

## Title

Align collective billing intent for suscripción retrieval.

## Context

The suscripción retrieval path now resolves the previous structure issues:

- broad policy prompts no longer lead with heading-only stubs;
- broad policy prompts now diversify across distinct sections;
- the collective billing subtree under `14.6` now exposes normalized lineage
  such as `14.6.1` and `14.6.2`.

One narrower retrieval-quality gap remains:

- for a query such as
  `cómo funciona la facturación de pólizas colectivas en movilidad`,
  live retrieval can still rank
  `13.11. Financiación de Pólizas Individuales`
  ahead of the more precise `14.6.*` collective billing sections.

This is now an intent-alignment problem between `facturación colectiva` and
adjacent `financiación individual` content inside the same document family.

## Scope

This slice should:

1. preserve the current suscripción section lineage and breadth behavior;
2. prefer collective billing sections when the prompt explicitly asks about
   facturación de pólizas colectivas;
3. keep the fix deterministic and narrow to this documented intent.

This slice should not:

- reopen markdown normalization;
- broaden into generic financing or payment intent across the repository;
- redesign the global reranking architecture beyond the smallest safe fix.

## Required Behavior

### 1. Intent alignment

Acceptance criteria:

- prompts about `facturación` plus `pólizas colectivas` or equivalent language
  prefer `14.6.*` collective billing sections over `13.11` financing
  individual sections when both are candidates;
- the fix is deterministic and covered by focused tests;
- existing suscripción breadth and heading-stub behavior remains intact.

### 2. Live retrieval improvement

Acceptance criteria:

- at least one live collective billing query returns a `14.6.*` section ahead
  of the financing-individual section;
- retrieval remains inside the suscripción document family.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records subsection-lineage normalization as complete;
- the roadmap records this collective-billing intent slice as the next
  remaining suscripción slice.
