# Requirements

## Title

Align deterministic supported-scope classification with ARL/RUI queries already
supported by retrieval.

## Context

The public Hugging Face Space now serves the updated Spanish UI and the indexed
ARL corpus, but a real ARL question still fails in the end-to-end app flow with
`unsupported_scope_refusal`. The same topic already works at the retrieval
layer, so the remaining gap is the deterministic supported-scope classifier
that runs before retrieval.

The next corrective slice should widen that classifier only enough to admit the
already-supported ARL/RUI document workflow.

## Scope

This slice should:

1. Add narrow deterministic token support for ARL/RUI insurance-document
   queries.
2. Cover the new path in both query-scope and UI-facing tests.
3. Keep the change limited to scope admission, not retrieval semantics.

This slice should not:

- add fuzzy matching or probabilistic classification;
- broaden support to unrelated domains;
- redesign refusal messaging;
- change retrieval, embeddings, or Qdrant behavior.

## Required Behavior

### 1. ARL/RUI scope admission

Supported-scope classification should recognize ARL/RUI insurance-document
queries as in-scope.

Acceptance criteria:

- queries mentioning ARL or common RUI/intermediation wording classify as
  `supported`;
- previously supported Spanish insurance-document queries remain supported;
- unrelated non-insurance queries remain unsupported.

### 2. UI flow compatibility

The app-facing query handler should no longer refuse the ARL/RUI path before
calling grounded-answer generation.

Acceptance criteria:

- a representative ARL/RUI question reaches the grounded-answer path in UI
  tests;
- the result no longer reports `unsupported_scope_refusal`.

### 3. Regression coverage

The repository should cover both the classifier seam and the user-facing path.

Acceptance criteria:

- focused tests cover ARL/RUI scope classification;
- focused tests cover the ARL/RUI UI query path.
