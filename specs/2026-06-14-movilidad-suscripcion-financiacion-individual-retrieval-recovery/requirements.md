# Requirements

## Title

Recover direct retrieval for suscripción `13.11 Financiación de Pólizas Individuales` queries.

## Context

Post-remediation live validation over `politicas de suscripcion de movilidad` has
one remaining known suscripción gap:

- the query `¿Cómo funciona la financiación de pólizas individuales en movilidad?`
  is inside supported scope;
- the indexed suscripción corpus already contains the relevant `13.11`
  subsection chunks;
- however, live retrieval currently returns zero chunks for that query, so the
  answer path degrades to insufficient evidence instead of surfacing the
  financing rules already present in the corpus.

This is now a narrow retrieval-recovery and intent-alignment problem for the
existing `13.11` evidence.

## Scope

This slice should:

1. preserve the current supported-scope behavior for the documented query pattern;
2. recover direct retrieval for the existing `13.11` financing-individual chunks;
3. keep the fix deterministic and narrow to this suscripción financing intent.

This slice should not:

- reopen ingestion or markdown normalization for the suscripción PDF;
- broaden into generic financing retrieval for unrelated document families;
- redesign the global retrieval algorithm beyond the smallest safe fix.

## Required Behavior

### 1. Financing-individual retrieval recovery

Acceptance criteria:

- representative suscripción financing-individual queries retrieve the existing
  `13.11. Financiación de Pólizas Individuales` evidence;
- retrieval remains inside the suscripción document family under the existing
  movilidad policy scope.

### 2. Live answer recovery

Acceptance criteria:

- at least one live `answer-query` run for
  `¿Cómo funciona la financiación de pólizas individuales en movilidad?`
  returns grounded suscripción evidence instead of zero-retrieval degradation;
- the leading documentary basis points to `13.11` financing-individual content.

### 3. Traceability

Acceptance criteria:

- the roadmap records this slice as closed once live retrieval is restored;
- the dated validation file records the zero-result baseline and the recovery
  evidence.
