# Requirements

## Slice

`arl-remuneracion-policy-overview-vs-table-priority`

## Goal

Prefer explanatory overview evidence before dense table evidence for broad ARL
remuneration questions, while preserving table-first behavior for explicit
percentage or sector queries.

## Context

The previous ARL remuneration retrieval slice now surfaces the correct family of
sections first, but broad queries such as
`¿Cuál es el esquema de remuneración del canal externo ARL?` still lead with a
table-heavy `Pago de comisiones por Atracción` chunk. For broad schema
questions, operators benefit more from first seeing the explanatory
`Clientes nuevos (venta) para el Canal Externo` overview chunk. At the same
time, explicit sector/percentage questions should still prefer table evidence.

## Requirements

1. Broad ARL remuneration overview queries must rank the explanatory
   `Clientes nuevos (venta) para el Canal Externo` chunk ahead of table-heavy
   `Pago de comisiones por Atracción` chunks.
2. Explicit ARL remuneration table or percentage queries must continue to rank
   `Pago de comisiones por Atracción` first.
3. The behavior must remain narrow to the ARL remuneration-policy family.
4. The change must not disturb ARL FAQ or guide retrieval.

## Non-Goals

- changing chunk text or source markdown;
- changing answer-generation contracts;
- adding broader taxonomy or metadata layers.
