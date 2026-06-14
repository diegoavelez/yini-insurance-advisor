# Requirements

## Title

Consolidate category-onboarding slice scope so future bundles stay
root-cause-sized instead of query-sized.

## Context

The repository now has a strong ingestion-and-retrieval onboarding workflow,
but recent category remediation has started to over-fragment into many
same-seam dated bundles. This increases documentation overhead and makes the
roadmap harder to read without improving implementation clarity.

The process needs a clearer rule: open new bundles when the root-cause family
changes, not when each new query variant surfaces inside the same seam.

## Scope

This slice should:

1. update the category-onboarding playbook with a root-cause-sized slicing
   policy;
2. define an operational cap for active onboarding/remediation bundles per
   category;
3. make the roadmap easier to scan by adding compact cohort rollups and
   reframing the long slug lists as traceability indexes.

This slice should not:

- rewrite historical spec bundles;
- delete historical slice slugs from the roadmap;
- change current implementation status for any category.

## Required Behavior

### 1. Root-cause-sized bundle policy

Acceptance criteria:

- the playbook says new dated bundles should be opened per root-cause family;
- the playbook explicitly says query variants should be recorded in
  `validation.md` before opening a new bundle.

### 2. Operational cap

Acceptance criteria:

- the playbook caps future category work to one active onboarding bundle and
  one active remediation bundle at a time;
- the default category lifecycle is expressed as a small number of bundle
  families rather than an open-ended chain of micro-bundles.

### 3. Roadmap readability

Acceptance criteria:

- the roadmap contains a compact rollup summary for the current category
  cohorts;
- the long dated slug lists are labeled as indexes/traceability rather than the
  primary operational view.
