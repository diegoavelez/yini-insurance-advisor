# Requirements

## Slice

`arl-remuneracion-policy-parent-child-heading-compaction`

## Goal

Remove remaining heading-only parent/child scaffold noise from ARL remuneration
policy retrieval surfaces.

## Context

The previous ARL remuneration-policy cleanup removed duplicated section headings,
but a narrower retrieval-quality gap remains in
`ARL/politica de remuneracion canal externo v4.pdf`:

- chunk `arl__politica-de-remuneracion-canal-externo-v4:v2:0021` is a
  standalone overlap chunk that contains only heading scaffolds,
  `## Clientes nuevos (venta) para el Canal Externo` and
  `## Pago de comisiones por Atracción`;
- that chunk can rank above richer `Clientes nuevos` chunks for broad retrieval
  queries even though it contains no substantive policy text.

## Requirements

1. Standalone overlap chunks made only of markdown headings and blank lines must
   not be emitted into the chunk bundle.
2. The fix must preserve chunks that contain any substantive non-heading body
   text, including lists, tables, numbered clauses, or paragraphs.
3. The fix must not weaken existing ARL/RUI FAQ or ARL guide normalizations.
4. The ARL remuneration policy must keep its richer `Clientes nuevos` and
   `Por cambio de intermediario` chunks available for retrieval after rebuild.

## Non-Goals

- redesign remuneration-policy hierarchy semantics;
- rewrite source markdown;
- retune ranking or answer-generation logic;
- alter unrelated chunk families outside this chunk-emission gap.
