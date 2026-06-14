# Requirements

## Title

Align renewal billing-mode intent for suscripción collective-policy queries.

## Context

After closing the `facturación por asegurado` scope/retrieval gap, the next
suscripción issue is narrower:

- the query `¿Se puede cambiar la modalidad de facturación en la renovación de una póliza colectiva?`
  already returns a grounded answer with `supported=true`;
- however, live retrieval still prioritizes `13.10` and `13.1.2` business rules
  for individual payment-plan changes ahead of the collective-policy evidence in
  `14.6.2`, even though the target answer is specifically about collective
  billing modality in renewal.

This is now a narrow intent-alignment and evidence-prioritization gap, not a
scope-admission problem.

## Scope

This slice should:

1. preserve the current supported response for the documented query pattern;
2. prioritize the collective-policy `14.6.2` evidence that states collective
   policies do not allow billing-mode changes in renewal;
3. keep the fix deterministic and narrow to this renewal-specific collective
   billing intent.

This slice should not:

- redesign global renewal or payment-change ranking;
- reopen the finished `facturación por asegurado` scope slice;
- change unrelated financing-individual retrieval behavior.

## Required Behavior

### 1. Renewal-specific collective billing intent alignment

Acceptance criteria:

- for representative renewal-specific collective billing queries, retrieval
  ranks the collective-policy evidence from `14.6.2` ahead of individual-payment
  change sections such as `13.10` and `13.1.2`;
- the fix is deterministic and covered by focused retrieval tests.

### 2. Live answer grounding improvement

Acceptance criteria:

- at least one live `answer-query` run for the documented renewal question still
  returns `supported=true`;
- the leading documentary basis / citations now foreground the collective-policy
  evidence rather than individual-plan-change sections.

### 3. Traceability

Acceptance criteria:

- the roadmap keeps this slice as the next active suscripción gap ahead of the
  financing-individual retrieval-recovery slice;
- the dated validation file records the baseline evidence and completion checks.
