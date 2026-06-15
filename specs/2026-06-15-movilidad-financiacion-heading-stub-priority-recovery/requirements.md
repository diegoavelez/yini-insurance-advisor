# Requirements

## Title

Prefer contentful financing-guide chunks over heading-only stubs.

## Context

`MOVILIDAD/FINANCIACION` already reaches the correct guide family:

- retrieval stays inside `instructivo financiacion de polizas v1.pdf`;
- grounded answers stay inside the same documentary surface with
  `confidence=high`.

The remaining gap is narrower:

- the top retrieved chunk can still be the section stub
  `Manual Procedimiento Financiacion de polizas individuales / Procedimientos:`;
- richer chunks such as `Paso a paso` and `Notas Importantes` remain below that
  stub even though they contain the actual procedural evidence.

This is no longer a family-scoping problem. It is an intra-family evidence
ordering problem similar to the prior suscripción heading-stub slice.

## Scope

This slice should:

1. detect heading-only or near-empty financing-guide chunks in reranking;
2. prefer contentful financing-guide chunks for explicit financing-guide
   queries;
3. preserve the existing document-family filter behavior.

This slice should not:

- reopen Docling extraction;
- redesign the financing query-filter rules;
- broaden into suscripción policy retrieval;
- introduce global ranking changes outside this guide family.

## Required Behavior

### 1. Heading-stub demotion inside the financing guide

Acceptance criteria:

- chunks with no meaningful body after markdown headings are demoted relative
  to richer chunks from the same financing guide family;
- `Paso a paso` procedural chunks can outrank the `Procedimientos:` stub for
  explicit financing-guide prompts;
- the behavior is deterministic and testable.

### 2. Retrieval-quality recovery

Acceptance criteria:

- live retrieval for
  `¿Cómo funciona la financiación de pólizas individuales?`
  returns a contentful chunk ahead of the heading-only stub;
- retrieval still stays inside
  `Manual Procedimiento Financiacion de polizas individuales`;
- grounded answers continue to stay inside the same guide family.

### 3. Backward compatibility

Acceptance criteria:

- current retrieval behavior for non-financing queries remains unchanged;
- existing financing family scoping tests still pass;
- the public CLI contract stays unchanged.
