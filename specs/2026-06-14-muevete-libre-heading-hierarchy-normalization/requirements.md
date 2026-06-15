# Requirements

## Title

Normalize `Muévete Libre` heading hierarchy so chunk structure and citations stay semantic.

## Context

`MOVILIDAD/MUEVETE LIBRE/clausulado muevete libre v2.pdf` is already onboarded,
indexed, and answers real coverage queries correctly. However, the current
cleaned markdown keeps a flattened heading surface where almost every semantic
label is emitted as `## ...`.

That flattened structure creates two visible quality issues:

- `section_path` loses the parent-child hierarchy between section groups such as
  `2. Gastos de defensa judicial` and child clauses such as `2.1. Cobertura`;
- chunk text and grounded citations expose duplicated heading scaffolds like
  repeated `## 1.1. Cobertura` or mixed parent/child heading echoes.

This is now a narrow ingestion-time normalization problem for one already-live
document family.

## Scope

This slice should:

- keep the existing `Muévete Libre` product/document metadata unchanged;
- normalize the cleaned markdown for
  `clausulado muevete libre v2.pdf` into a semantic heading hierarchy;
- ensure chunk assembly no longer emits duplicated leading heading scaffolds for
  representative `Muévete Libre` coverage sections;
- ensure reindexing can replace older legacy points for the same
  `source_pdf_id` so live retrieval reflects the corrected chunk structure;
- preserve the current successful retrieval/answer behavior for
  `¿Qué cubre Muévete Libre?`.

This slice should not:

- redesign generic chunk-prefix behavior for every document family;
- reopen retrieval ranking for unrelated mobility products;
- change response contracts or UI rendering.

## Acceptance Criteria

### 1. Semantic heading hierarchy

- the `Muévete Libre` cleaned markdown promotes `PLAN MUÉVETE LIBRE` to a root
  heading;
- section-group headings such as `SECCIÓN 1 Coberturas principales` and
  `2. Gastos de defensa judicial` are represented at distinct semantic levels;
- child clause headings such as `2.1. Cobertura` remain nested under their
  parents instead of flattening into one repeated level.

### 2. Cleaner chunk structure

- representative chunk records for `Muévete Libre` coverage sections no longer
  duplicate the same heading surface at the start of the chunk body;
- representative `section_path` values retain the expected parent-child lineage.

### 3. Retrieval compatibility

- focused ingestion/retrieval regression tests pass;
- source-level reindexing can safely prune existing points for the same
  `source_pdf_id` before upsert;
- real `retrieve-chunks` and `answer-query` runs for
  `¿Qué cubre Muévete Libre?` remain supported after the normalization path is
  updated.
