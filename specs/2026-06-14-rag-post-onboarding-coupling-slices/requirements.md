# Requirements

## Title

Document deferred post-onboarding `rag` coupling-reduction slices.

## Context

Graph inspection of `rag/ingestion.py` identified additional extraction seams
that would reduce long-term coupling:

- document canonicalization helpers;
- markdown/chunk structural normalization helpers;
- ARL remuneration domain heuristics.

Those seams are technically valid, but they are not the correct immediate
priority while category onboarding and retrieval hardening are still active.
The repository needs these refactors documented for later evaluation without
promoting them to active MVP blockers today.

## Scope

This slice should:

1. record the remaining `rag` coupling-reduction candidates in the roadmap;
2. describe them as deferred post-onboarding refactor slices;
3. preserve the current roadmap truth that only active retrieval/onboarding
   work remains in the current operational sequence.

This slice should not:

- implement any of the deferred refactors;
- mark the deferred candidates as current blocking work;
- expand the scope into a new architectural phase.

## Required Behavior

### 1. Deferred candidate traceability

Acceptance criteria:

- the roadmap names the next three `rag` coupling-reduction slices explicitly;
- each candidate has a short rationale tied to observed `rag/ingestion.py`
  coupling.

### 2. Active-scope preservation

Acceptance criteria:

- the roadmap continues to distinguish current onboarding/retrieval work from
  later refactor work;
- the deferred candidates do not replace or obscure the currently active
  operational slice list.
