# Requirements

## Title

Align SOAT coverage intent with retrieval-facing `document_type`.

## Context

The baseline `MOVILIDAD/SOAT` slice ingests both a `policy` document
(`clausulado soat.pdf`) and a `guide` document (`tarifas soat 2026.pdf`).
Runtime validation showed a concrete failure mode:

- `¿Cuáles son las tarifas del SOAT 2026?` retrieves tariff chunks correctly.
- `¿Qué cubre el SOAT?` drifts into tariff chunks unless the caller manually
  forces `document_type=policy`.

This is a retrieval-intent alignment gap, not an ingestion failure: valid
coverage chunks already exist in the indexed `policy` corpus.

## Scope

This corrective slice should:

1. add a narrow operator-curated default filter rule for SOAT coverage intent;
2. preserve explicit caller-provided filters;
3. add a small SOAT coverage query-expansion bundle to improve reranking inside
   the policy corpus;
4. record the corrective slice in the roadmap.

This slice should not:

- redesign the backend retrieval contract;
- introduce generic product-wide document-type inference for all categories;
- change chunking or re-ingestion behavior.

## Required Behavior

### 1. Coverage intent defaults to policy

Acceptance criteria:

- a SOAT query about coverage or amparos can default `document_type=policy`
  when the caller did not explicitly provide `document_type`;
- explicit `document_type` filters remain authoritative.

### 2. Tariff intent stays guide-oriented

Acceptance criteria:

- SOAT tariff queries can default `document_type=guide` when no explicit
  document type is provided.

### 3. Backward compatibility

Acceptance criteria:

- focused retrieval tests pass;
- the retrieval contract surface remains backward compatible for callers that
  already pass explicit filters.
