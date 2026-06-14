# Requirements

## Title

Diversify movilidad PV benefit retrieval across broader sections and suppress duplicate section repeats.

## Context

The previous corrective slices resolved two important problems for the query
`qué beneficios incluye la propuesta de valor de movilidad`:

- retrieval is now constrained to the `PROPUESTA DE VALOR MOVILIDAD` document
  family;
- the live Qdrant collection now accepts the `document_name` filter once
  reindexed.

Live validation still shows one remaining quality gap inside the PV family:

- narrow service sections such as `Grúa de amplio alcance` can outrank broader
  benefit sections for a general benefits query;
- duplicate chunks from the same section such as repeated `Pérdidas totales`
  can consume multiple top-k slots.

The next narrow slice should improve breadth and suppress duplicate section
repeats for this explicit PV benefit-intent retrieval path without redesigning
the general reranker.

## Scope

This slice should:

1. Detect explicit movilidad PV benefit-intent queries after the existing
   curated expansion/reranking path runs.
2. Prefer breadth across distinct PV benefit sections before repeating the same
   section.
3. Favor broader benefit sections over narrow service-detail sections when the
   query asks generally about benefits.

This slice should not:

- change retrieval contracts;
- introduce new Qdrant metadata or filters;
- redesign ranking for non-PV queries;
- hardcode document ids outside the already-curated PV family seam.

## Required Behavior

### 1. PV benefit-intent diversification

When the query explicitly targets the movilidad value proposition and asks for
benefits, retrieval should diversify across distinct PV sections before
returning repeated sections.

Acceptance criteria:

- repeated chunks from the same PV section do not occupy multiple early top-k
  slots;
- the behavior applies only to the explicit PV benefit-intent path;
- non-PV retrieval keeps the current behavior.

### 2. Breadth preference

For that same explicit PV benefit-intent path, broader benefit sections should
be preferred over narrow single-service sections.

Acceptance criteria:

- chunks with richer benefit surfaces, such as multiple bullet items or broader
  multi-item text, can outrank narrow single-service sections;
- the preference remains deterministic and local;
- the public score/result contract stays unchanged.

### 3. Backward compatibility

Existing retrieval behavior outside this narrow scenario should remain stable.

Acceptance criteria:

- current retrieval tests still pass;
- coverage-intent, deductible-intent, and comparison-intent logic are not
  changed;
- unmatched queries return the current ordering behavior.

### 4. Documentation and roadmap

The roadmap should record that this is a narrow intra-PV ranking refinement.

Acceptance criteria:

- the new slice is listed in the roadmap;
- the implementation note describes duplicate-section suppression and breadth
  preference as PV-specific.
