# Requirements

## Title

Recover usable extraction structure for the `financiación` transversal guide.

## Context

The baseline `financiación` cohort run completed technically:

- ingestion succeeded;
- embeddings succeeded;
- Qdrant indexing succeeded.

However, artifact inspection showed the extracted content is not retrieval-ready:

- `data/processed/movilidad__transversales__instructivo-financiacion-de-polizas-v1.cleaned.md`
  currently contains only `sura`;
- `data/processed/chunks/movilidad__transversales__instructivo-financiacion-de-polizas-v1.chunks.json`
  currently contains exactly one chunk with `section=None` and text `sura`.

The failed live retrieval is therefore explained by extraction collapse, not by
missing query scoping alone. The next narrow slice should recover a truthful
text surface for this document before any financing-specific retrieval
alignment work.

## Scope

This slice should:

1. inspect why the current extraction collapsed to `sura`;
2. recover a materially richer cleaned-markdown surface for this document;
3. regenerate chunk artifacts and re-run financing retrieval checks.

This slice should not:

- broaden into `suscripción` or other transversal documents;
- add financing-specific reranking rules before extraction is usable;
- redesign the global ingestion architecture.

## Required Behavior

### 1. Extraction recovery

Acceptance criteria:

- the financing document no longer collapses to a single-token cleaned surface;
- cleaned markdown exposes enough procedural or commercial financing content to
  support retrieval;
- chunk generation produces more than one semantically meaningful chunk unless
  the recovered document truthfully has only one short section.

### 2. Retrieval readiness

Acceptance criteria:

- at least one financing-oriented retrieval query returns financing-document
  chunks instead of unrelated PV documents;
- if retrieval still misses after extraction recovery, that follow-on issue is
  documented as a separate ranking/scope corrective slice.

### 3. Documentation and roadmap

Acceptance criteria:

- the roadmap records the baseline run as completed and the extraction issue as
  the remaining narrow slice;
- the spec bundle captures the concrete failed artifact evidence.
