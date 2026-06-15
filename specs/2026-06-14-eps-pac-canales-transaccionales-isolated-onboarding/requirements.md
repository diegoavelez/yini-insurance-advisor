# Requirements

## Title

Onboard the isolated `EPS/PLAN COMPLEMENTARIO PAC` transactional channels and
support guide.

## Context

After the completed `PAC 60+ core`, `formularios / gestión básica`,
`Global Web`, long instructivos, PAC policy follow-on, and traditional
clausulado slices, the final PAC slice is:

- `informacion canales transaccionales y apoyo v1.pdf`

This slice is the correct next step because:

- it is the last remaining PAC PDF in the current roadmap scope;
- it belongs to the operational/support family rather than policy-family
  retrieval;
- onboarding it closes the PAC category while keeping the unsupported `.docx`
  files explicitly deferred.

## Scope

This slice should:

1. add canonical metadata support for
   `informacion canales transaccionales y apoyo v1.pdf` under `product=pac`;
2. onboard the document through ingestion, embeddings, and Qdrant indexing;
3. validate at least one transactional/support retrieval intent against the new
   family;
4. close the PAC operational roadmap rollup after successful onboarding.

This slice should not:

- reopen previous PAC cohorts;
- add `.docx` support;
- introduce broad PAC reranking unrelated to transactional/support intents.

## Required Behavior

### 1. Canonical metadata support

Acceptance criteria:

- `informacion canales transaccionales y apoyo v1.pdf` persists with canonical
  `product=pac`;
- overlay-backed metadata persists it as the correct retrieval-facing
  `document_type`.

### 2. Isolated onboarding

Acceptance criteria:

- the slice targets only this single remaining PAC PDF;
- the two `.docx` files remain explicitly deferred.

### 3. Retrieval validation

Acceptance criteria:

- a PAC transactional/support query retrieves this document family first;
- if deterministic routing is required, it remains narrowly scoped to this
  document family and does not perturb previously validated PAC policy lanes.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap reflects PAC cohort onboarding as completed after this slice;
- the validation file records the remaining deferred `.docx` items only.
