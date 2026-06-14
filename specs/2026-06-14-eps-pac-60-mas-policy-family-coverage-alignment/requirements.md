# Requirements

## Title

Close the remaining `PAC 60+` policy-family retrieval gap after baseline
onboarding evidence.

## Context

The `PAC 60+ core` baseline cohort is operational through ingestion,
embeddings, Qdrant indexing, and first retrieval validation.

Initial live validation showed a narrow policy-family gap inside the
`product=pac`, `document_type=policy` lane, but root-cause review revised the
diagnosis:

- the persisted `clausulado pac 60 mas sura v1.pdf` chunk and embedding
  artifacts were stale, because they had been generated before PAC overlays
  existed and were then skipped by the `overwrite=false` incremental path;
- once those artifacts were regenerated with resolved PAC metadata, broad PAC
  coverage queries started returning the clausulado family correctly;
- one remaining deterministic gap persisted: explicit `asegurabilidad` queries
  still needed to stay pinned to the asegurabilidad family rather than drifting
  back to the clausulado family.

## Scope

This slice should:

1. regenerate stale PAC processed/chunk/embedding artifacts when resolved
   metadata no longer matches existing persisted outputs;
2. keep broad PAC coverage and explicit clausulado intents aligned to the
   clausulado family;
3. keep explicit asegurabilidad queries aligned to the asegurabilidad document
   family;
4. reuse the existing incremental-ingestion and operator-curated normalization
   seams rather than adding broader reranking logic.

This slice should not:

- reopen the full PAC folder onboarding sequence;
- change `faq` or `tarifas` behavior without evidence;
- introduce broad product-level reranking unrelated to PAC policy-family
  disambiguation.

## Required Behavior

Acceptance criteria:

- stale PAC artifacts are regenerated automatically when overlay-resolved
  metadata no longer matches persisted processed/chunk/embedding outputs;
- `¿Qué cubre el PAC 60 Más?` prefers the clausulado family over
  asegurabilidad-family chunks;
- `¿Qué cubre el clausulado PAC 60 Más?` prefers the clausulado family over
  asegurabilidad-family chunks;
- `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` prefers the
  asegurabilidad family;
- the closure is covered by focused regression tests plus live retrieval
  evidence.
