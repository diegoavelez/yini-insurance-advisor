# Requirements

## Title

Recover vehicle-category labels for `SOAT` tariff answering.

## Context

The first live P1 MVP acceptance pass left `MOVILIDAD/SOAT` at
`fragile-pass`.

Observed live behavior:

- retrieval for `¿Cuáles son las tarifas SOAT 2026?` correctly lands on
  `MOVILIDAD/SOAT/tarifas soat 2026.pdf`;
- however, the retrieved chunks expose mostly raw markdown-table fragments, and
  the grounded answer only enumerates numeric values without stable
  vehicle-category labels.

Artifact inspection shows the root cause is structural:

- the cleaned markdown preserves the tariff PDF as large repeated markdown
  tables;
- chunk generation splits those tables mid-row, producing chunks that contain
  partial numeric fragments without enough category context.

## Scope

This slice should:

1. normalize SOAT tariff tables into retrieval-friendly statement blocks that
   preserve category labels and row labels;
2. keep the fix narrow to SOAT tariff-style tables rather than rewriting all
   markdown tables globally;
3. rebuild the `tarifas soat 2026` artifacts and validate live retrieval plus
   grounded answering.

This slice should not:

- change SOAT coverage/clausulado routing;
- redesign answer formatting for all tabular documents;
- broaden into a generic table engine beyond what this tariff PDF needs.

## Required behavior

### 1. Table normalization

Acceptance criteria:

- SOAT tariff table blocks are rewritten into statement-style text that keeps
  the vehicle family visible, for example `Motos` or `Autos familiares`;
- each tariff row preserves enough context to bind numeric values to a
  category/descriptor rather than exposing bare numbers only.

### 2. Retrieval and answer behavior

Acceptance criteria:

- live retrieval for `¿Cuáles son las tarifas SOAT 2026?` returns chunks whose
  text includes vehicle-category labels plus tariff values;
- live grounded answering for the same query remains inside
  `tarifas soat 2026.pdf` and surfaces labeled tariff evidence rather than a
  flat list of amounts.

### 3. Documentation

Acceptance criteria:

- the MVP acceptance matrix can promote `MOVILIDAD/SOAT` from `fragile-pass`
  to `pass` only if the live answer now preserves usable labels;
- the roadmap records closure of the SOAT tariff-label blocker when the live
  validation succeeds.
