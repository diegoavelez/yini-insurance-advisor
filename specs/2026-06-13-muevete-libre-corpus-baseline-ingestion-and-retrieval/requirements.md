# Requirements

## Title

Bring `MOVILIDAD/MUEVETE LIBRE` into the current RAG baseline.

## Context

One new source PDF now exists under `data/raw/MOVILIDAD/MUEVETE LIBRE`:

- `clausulado muevete libre v2.pdf`

The repository does not yet expose a canonical retrieval-facing `muevete libre`
product value, curated overlay metadata for this document, or explicit
supported-scope admission for Muévete Libre queries.

## Scope

This slice should:

1. add canonical `muevete libre` query and filter aliases;
2. add minimal supported-scope admission for Muévete Libre queries;
3. add curated overlay metadata for the current source PDF;
4. ensure path-derived product inference can resolve `product=muevete libre`;
5. record the baseline slice in the roadmap.

This slice should not:

- redesign document-type taxonomy;
- implement corrective retrieval tuning before runtime evidence exists;
- broaden the `movilidad` taxonomy beyond this category.

## Required Behavior

### 1. Muévete Libre taxonomy baseline

Acceptance criteria:

- `muevete libre` is a canonical retrieval-facing `product` value;
- queries mentioning `Muévete Libre` normalize toward that canonical value;
- metadata filter aliases can resolve `muevete libre`.

### 2. Supported query scope

Acceptance criteria:

- representative queries such as `¿Qué cubre Muévete Libre?` classify as
  supported.

### 3. Overlay baseline

Acceptance criteria:

- `clausulado muevete libre v2` persists as `document_type=policy` and
  `product=muevete libre`.

### 4. Backward compatibility

Acceptance criteria:

- focused query-scope and ingestion tests pass;
- existing category behavior remains unchanged.
