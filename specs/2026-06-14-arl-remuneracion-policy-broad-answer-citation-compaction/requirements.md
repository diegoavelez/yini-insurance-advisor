# Requirements

## Slice

`arl-remuneracion-policy-broad-answer-citation-compaction`

## Goal

Compact documentary basis and citations for broad ARL remuneration-policy
answers so operators see a shorter evidence trail without losing direct support.

## Context

The current ARL remuneration policy flow is operationally correct: broad
queries already retrieve the right family and the grounded answer is supported.
However, broad overview prompts such as
`¿Cuál es el esquema de remuneración del canal externo ARL?` still surface too
many complementary policy chunks in `documentary_basis` and `citations`.

The current broad answer can cite:

- the overview chunk `Clientes nuevos (venta) para el Canal Externo`;
- the appetite/grouping chunk `Apetito Comercial por grupos...`;
- the table chunk `Pago de comisiones por Atracción`;
- the change-of-intermediary chunk `Por cambio de intermediario`;
- and a lateral policy chunk such as
  `Política de designación de intermediarios en la Solución de Riesgos Laborales`.

That fifth citation makes the evidence trail noisier than needed for overview
questions.

## Requirements

1. Broad ARL remuneration overview answers must keep high-confidence grounding
   while narrowing citations and documentary basis to direct support chunks.
2. The compacted evidence set must still preserve at least:
   - the overview chunk;
   - the appetite/table support needed for sector and commission details;
   - the change-of-intermediary support when present.
3. Lateral policy chunks that do not materially add to the broad overview
   answer should be excluded from `documentary_basis` and `citations`.
4. The change must remain narrow to broad ARL remuneration overview queries.

## Non-Goals

- changing retrieval ranking;
- changing chunk text or source markdown;
- changing citations for explicit ARL table/percentage queries;
- broadening this compaction logic to unrelated categories.
