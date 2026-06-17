# Requirements

## Title

Automate the current MVP category-acceptance matrix as a deterministic smoke asset.

## Context

The current MVP category-acceptance matrix is now operationally closed:

- the onboarded category set has manual live evidence for retrieval and
  grounded-answer acceptance;
- the roadmap still carries that evidence mostly as narrative notes and one
  manual matrix artifact;
- there is no typed smoke asset or deterministic runner that protects the
  accepted category set from regression without repeating ad hoc manual review.

This means the next MVP slice is no longer another retrieval correction. The
next narrow gap is regression protection and execution focus traceability for
the already accepted corpus.

## Scope

This slice should:

1. encode the accepted category set into a typed MVP acceptance-smoke dataset;
2. add a deterministic runner that can validate retrieval-family and
   grounded-answer evidence alignment through injected runtime callables;
3. sync the roadmap so the manual matrix is no longer the only acceptance
   artifact.

This slice should not:

- rerun or replace the existing live Qdrant/Groq validation notes;
- redesign the broader evaluation dataset;
- open new category waves;
- resume deferred `rag` coupling slices inside the same implementation.

## Required Behavior

### 1. Typed acceptance-smoke dataset

Acceptance criteria:

- a committed typed dataset exists for the current accepted category set;
- each case records:
  - category family;
  - retrieval smoke query;
  - grounded-answer smoke query;
  - optional validated filters;
  - expected retrieval evidence surface;
  - expected grounded-answer evidence surface;
- the dataset uses stable ids and validation rules.

### 2. Deterministic smoke runner

Acceptance criteria:

- a runner can load the typed acceptance-smoke dataset;
- the runner accepts injected retrieval and grounded-answer callables;
- for each case, the runner determines whether:
  - the top retrieval evidence matches the expected retrieval family;
  - the grounded-answer documentary basis / citations stay inside the expected
    answer evidence family;
- the runner returns typed, per-case results without depending on live
  external services during tests.

### 3. Regression coverage

Acceptance criteria:

- focused tests validate dataset loading and uniqueness;
- focused tests validate a matched case and a mismatched case in the smoke
  runner;
- the slice remains deterministic and locally executable.

### 4. Roadmap sync

Acceptance criteria:

- the roadmap records `mvp-current-category-acceptance-smoke-automation` as the
  next MVP hardening slice;
- once implemented, the roadmap records that the accepted category set is now
  protected by a committed smoke asset in addition to the live acceptance
  matrix.
