# Requirements

## Title

Align grounded-answer evidence with the ARL account-update guide family.

## Context

The commissions-guide answer-evidence slice is already closed, but the
symmetric ARL guide query still carries one lateral secondary guide in its
answer-facing evidence:

- primary guide: `Actualización de cuenta bancaria para pago de comisiones ARL SURA`
- lateral guide: `Consulta liquidación de comisiones para intermediarios de Riesgos Laborales`

For explicit account-update queries, the primary guide already contains the
full procedural answer by itself.

## Scope

This slice should:

1. add narrow answer-evidence selection for explicit ARL account-update guide
   queries;
2. keep retrieval ranking unchanged;
3. narrow only `documentary_basis` and `citations` when the account-update
   guide is already sufficient.

This slice should not:

- broaden into a generic ARL multi-guide framework;
- alter the answer contract or retrieval backend;
- suppress lateral guide retrieval for unrelated ARL guide questions.

## Required Behavior

### 1. Narrow guide-family answer evidence

Acceptance criteria:

- explicit ARL account-update queries keep the account-update guide as the
  answer-facing evidence source;
- the lateral commissions guide no longer appears in `documentary_basis` or
  `citations` for that narrow query family when the account-update guide is
  present.

### 2. Preserve confidence and answer quality

Acceptance criteria:

- grounded answers for the account-update query still complete successfully;
- confidence remains high when the account-update guide is sufficient on its
  own.

### 3. Traceability

Acceptance criteria:

- focused automated coverage proves the narrowed evidence selection;
- live `answer-query` validation shows only the account-update guide in
  documentary basis and citations.
