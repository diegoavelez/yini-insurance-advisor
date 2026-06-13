# Requirements

## Title

Align AUTOS plan-comparison retrieval with operator-curated expansion rules.

## Context

The AUTOS corpus now includes a comparative document (`diferenciales planes autos.pdf`) plus plan-specific FAQ and guide documents. Real retrieval validation shows that comparative Spanish queries such as "¿Qué diferencias hay entre el plan básico y los otros planes de autos?" continue to rank only the Plan Básico FAQ, even after Docling-based ingestion and reindexing of the comparative PDF.

The repository already has:

- operator-curated metadata overlays;
- operator-curated term-equivalence normalization;
- stable retrieval contracts and CLI seams.

The next narrow slice should improve comparative AUTOS retrieval without redesigning retrieval contracts or adding probabilistic query rewriting.

## Scope

This slice should:

1. Add a deterministic operator-curated query-expansion rule seam.
2. Use that seam to enrich comparative AUTOS plan queries.
3. Keep existing alias expansion and metadata-filter normalization behavior unchanged.
4. Document the narrow operator workflow.

This slice should not:

- change the retrieval contract;
- introduce LLM-based query rewriting;
- modify indexed chunk payload contracts;
- add broader product-specific heuristics outside the curated file.

## Required Behavior

### 1. Operator-curated expansion rules

The repository should support a small operator-maintained set of retrieval query expansion rules.

Acceptance criteria:

- rules are optional at runtime;
- rules are committed and human-editable;
- each rule matches deterministically on curated phrases;
- each rule appends deterministic curated terms only.

### 2. Comparative AUTOS plan enrichment

When a query clearly expresses plan-comparison intent in AUTOS, retrieval should append comparison-oriented canonical terms that help the comparative document compete.

Acceptance criteria:

- a query that combines AUTOS context, Plan Básico context, and comparison intent appends curated comparison terms;
- the original user query remains intact;
- non-comparative AUTOS queries do not receive the comparison bundle;
- appended terms remain traceable to the curated operator file.

### 3. Backward compatibility

Existing alias expansion and filter canonicalization should remain valid.

Acceptance criteria:

- current query alias expansion tests still pass;
- current filter alias normalization tests still pass;
- unknown rules or missing files do not break retrieval.

### 4. Operator documentation

The repository should explain how to maintain these comparison-oriented rules.

Acceptance criteria:

- docs explain that these rules are narrow retrieval hints, not taxonomy inference;
- docs explain that canonical appended terms should stay aligned with real document names and overlays;
- docs avoid promising guaranteed ranking outcomes across the full corpus.
