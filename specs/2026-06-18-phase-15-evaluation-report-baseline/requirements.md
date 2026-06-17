# Requirements

## Title

Add the baseline Phase 15 evaluation report artifact.

## Context

The repository already has the core evaluation ingredients:

- a typed local evaluation dataset with golden behavior, retrieval, and
  citation expectation sets;
- deterministic local evaluation and hosted-like smoke runners;
- a committed MVP acceptance smoke dataset for the currently accepted category
  set;
- roadmap evidence that the live category-acceptance pass is closed.

What is still missing is a durable report surface that summarizes those assets,
their scope, their current baseline results, and their known limits.

## Scope

This slice should:

1. add a durable evaluation report artifact under a current-source
   documentation surface;
2. summarize the current deterministic evaluation assets and baseline results;
3. summarize the committed MVP acceptance smoke coverage for the current
   category set;
4. make the boundaries of the report explicit, especially what it does not
   claim about fresh live external execution.

This slice should not:

- redesign the evaluation runner architecture;
- add new scoring logic;
- claim fresh live Qdrant or Groq validation unless that work is actually run;
- reopen category remediation or coupling slices.

## Required Behavior

### 1. Durable report artifact

Acceptance criteria:

- a current-source evaluation report artifact exists under `docs/`;
- the report is readable without needing to inspect raw datasets first.

### 2. Baseline evaluation summary

Acceptance criteria:

- the report summarizes the current deterministic local evaluation asset set,
  including versions and counts;
- the report records the current baseline deterministic evaluation result for
  the local evaluation runner;
- the report records the current hosted-like citation smoke baseline.

### 3. MVP acceptance summary

Acceptance criteria:

- the report summarizes the committed MVP acceptance smoke dataset version and
  category-family coverage;
- the report lists the accepted category families protected by the smoke asset;
- the report distinguishes deterministic smoke coverage from earlier live
  acceptance evidence.

### 4. Boundaries and rerun guidance

Acceptance criteria:

- the report states that `.docx` forms are excluded from the MVP corpus;
- the report includes concise rerun commands for the deterministic evaluation
  surfaces used by the baseline;
- the report states what kinds of live validation are out of scope for this
  baseline artifact.

### 5. Roadmap and README sync

Acceptance criteria:

- the roadmap records `phase-15-evaluation-report-baseline`;
- the roadmap notes that the evaluation-report deliverable now has a durable
  artifact;
- the README points to the new report artifact as a current-source document.
