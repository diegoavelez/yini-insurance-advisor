# Requirements

## Title

Align grounded-answer evidence with the ARL commissions guide family.

## Context

The ARL commissions guide chunk is now structurally clean and retrieves first
for explicit commissions queries. However, live `answer-query` validation still
pulls a lateral second guide into `documentary_basis` and `citations`:

- `Actualización de cuenta bancaria para pago de comisiones ARL SURA`

That second guide is related to commissions operationally, but it is not
needed when the commissions guide already contains the complete procedural
answer.

## Scope

This slice should:

1. add narrow answer-evidence selection for explicit ARL commissions guide
   queries;
2. keep retrieval ranking unchanged;
3. narrow only the answer-facing evidence/citation surface when the primary
   commissions guide already answers the request sufficiently.

This slice should not:

- add a generic ARL document-family filter framework;
- alter the public answer contract;
- suppress lateral guide retrieval for other ARL guide questions;
- change Qdrant indexing or embeddings.

## Required Behavior

### 1. Narrow guide-family answer evidence

Acceptance criteria:

- explicit ARL commissions-guide queries use the commissions guide as the
  answer-facing evidence source;
- lateral ARL guide chunks do not appear in `documentary_basis` or `citations`
  for that narrow query family when the commissions guide is present.

### 2. Preserve confidence and answer quality

Acceptance criteria:

- grounded answers for the commissions query still complete successfully;
- confidence remains high when the commissions guide is sufficient on its own.

### 3. Traceability

Acceptance criteria:

- focused automated coverage proves the narrowed evidence selection;
- live `answer-query` validation shows only the commissions guide in
  documentary basis and citations.
