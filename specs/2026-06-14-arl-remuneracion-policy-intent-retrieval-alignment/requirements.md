# Requirements

## Slice

`arl-remuneracion-policy-intent-retrieval-alignment`

## Goal

Align broad ARL remuneration-policy retrieval toward explicit remuneration
sections instead of introductory policy sections.

## Context

After chunk cleanup, the ARL remuneration policy remains operational, but broad
queries such as `¿Cuál es el esquema de remuneración del canal externo ARL?`
still rank introductory sections like `Canales para la afiliación a ARL SURA`
ahead of explicit remuneration sections such as:

- `Clientes nuevos (venta) para el Canal Externo`
- `Pago de comisiones por Atracción`
- `Requisitos indispensables para el pago de comisión`
- `Por cambio de intermediario`

This weakens first-page retrieval quality even though the relevant remuneration
chunks are already indexed in Qdrant.

## Requirements

1. Broad ARL remuneration-policy queries must prefer explicit remuneration
   sections over introductory document sections.
2. The reranking must remain narrow to the ARL remuneration-policy document
   family and must not alter unrelated ARL guides, FAQs, or other policy
   families.
3. Duplicate chunks from the same remuneration section should be compacted so
   richer representatives appear before repeated overlaps.
4. The retrieval candidate-pool expansion, if added, must remain narrow to this
   intent family.

## Non-Goals

- changing answer-generation contracts;
- altering citation narrowing behavior;
- rewriting source markdown or chunk text;
- broad document-type taxonomy changes.
