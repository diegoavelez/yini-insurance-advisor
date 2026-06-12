# Requirements

## Title

Add an operator-curated term-equivalence seam for incremental Spanish corpus use.

## Context

The corpus under `data/raw/` will grow incrementally over time. Operators will
leave previously ingested files in place and add only new files. In parallel,
the retrieval layer needs a narrow way to reconcile common Spanish naming
variants, abbreviations, and operator terminology without redesigning the
backend contract.

The repository already has:

- deterministic path-derived document ids;
- optional operator-curated metadata overlays for `document_type` and `product`;
- retrieval filters over curated metadata fields.

The next narrow slice should add a small operator-maintained term-equivalence
table that improves retrieval normalization while preserving those existing
contracts.

## Scope

This slice should:

1. Add one explicit operator-curated term-equivalence file in the repository.
2. Normalize retrieval query text with curated equivalent terms when helpful.
3. Normalize retrieval filter values for `document_type` and `product`.
4. Document the intended operator workflow.

This slice should not:

- auto-classify documents into products or document types;
- mutate ingested document artifacts after the fact;
- redesign the retrieval contract;
- introduce broad semantic expansion or probabilistic synonym inference.

## Required Behavior

### 1. Operator-curated equivalence file

The repository should expose one small operator-maintained file for term
equivalences.

Acceptance criteria:

- the file is committed and human-editable;
- the file supports query aliases and metadata-filter aliases;
- the file remains optional at runtime if an operator removes it locally.

### 2. Query normalization

Retrieval should append canonical equivalent terms when the user query contains
known aliases.

Acceptance criteria:

- the original query remains intact;
- appended terms are deterministic and traceable to the curated file;
- no query expansion occurs when no configured alias matches.

### 3. Filter normalization

Retrieval metadata filters should map aliases to canonical values before the
Qdrant filter is built.

Acceptance criteria:

- `document_type` aliases can normalize to curated canonical values;
- `product` aliases can normalize to curated canonical values;
- unsupported or unknown values pass through unchanged.

### 4. Operator documentation

The repository should explain how this seam relates to the incremental corpus.

Acceptance criteria:

- the docs explain that `data/raw/` can accumulate prior files safely;
- the docs explain that equivalence-table canonical values should stay aligned
  with any curated metadata overlay values;
- the docs keep the scope narrow and avoid promising automatic taxonomy
  management.
