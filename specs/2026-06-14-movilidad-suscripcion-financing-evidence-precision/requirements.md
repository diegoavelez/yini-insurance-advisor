# Requirements

## Title

Tighten evidence precision for suscripción financing-individual answers.

## Context

After closing the `13.11` financing-individual retrieval-recovery slice, the
remaining suscripción financing gap is narrower:

- the query `¿Cómo funciona la financiación de pólizas individuales en movilidad?`
  is now supported and retrieves grounded evidence;
- live retrieval now correctly ranks `13.11. Financiación de Pólizas Individuales`
  first;
- however, the remaining top-k and documentary basis can still include lateral
  sections such as `14.1. Cotización de Pólizas Colectivas` or generic policy
  context that is not needed to answer the financing question itself.

This is now an intra-family evidence-precision problem, not a scope, ingestion,
or cross-document routing gap.

## Scope

This slice should:

1. preserve the current supported financing-individual answer path;
2. keep `13.11` as the leading evidence for representative financing queries;
3. reduce lateral suscripción sections in top-k, documentary basis, and
   citations when direct financing evidence is already sufficient.

This slice should not:

- reopen the finished `13.11` retrieval-recovery slice;
- redesign generic ranking across unrelated movilidad families;
- change corpus content, markdown normalization, or indexing contracts.

## Required Behavior

### 1. Financing evidence precision

Acceptance criteria:

- representative financing-individual suscripción queries keep `13.11` first;
- directly supporting financing sections such as `13.11` and, when useful,
  `13.1.2 Cambio de Plan de Pagos Anual Financiado` rank ahead of unrelated
  lateral sections such as `14.1` collective quotation;
- the fix remains deterministic and narrow to the financing-individual intent.

### 2. Live documentary-basis precision

Acceptance criteria:

- at least one live `answer-query` run for the documented financing question
  still returns a grounded supported answer;
- the leading documentary basis and citations focus on direct financing
  evidence rather than unrelated collective-policy sections when enough
  financing evidence is available.

### 3. Traceability

Acceptance criteria:

- the roadmap records this slice as the next active suscripción financing gap;
- the dated validation file records the current lateral-evidence baseline and
  the intended completion checks.
