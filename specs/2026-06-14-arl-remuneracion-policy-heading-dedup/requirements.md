# Requirements

## Title

Deduplicate heading scaffolds in the ARL remuneration policy chunk surface.

## Context

The current `ARL` policy corpus is operational, but the chunk surface for:

- `ARL/politica de remuneracion canal externo v4.pdf`

still carries duplicated heading scaffolds after section-path prefixing. For
example, live chunk text can surface:

- repeated `## Canales para la afiliación a ARL SURA`
- repeated `## Clientes nuevos (venta) para el Canal Externo`
- repeated `## Por cambio de intermediario`

These duplicates make retrieval evidence harder to read even though the
document family and ranking path already work.

## Scope

This slice should:

1. remove duplicated leading heading scaffolds when the chunk already starts
   with headings covered by its `section_path`;
2. preserve the current retrieval semantics and document family;
3. validate the refreshed chunk surface locally and through a live policy
   retrieval query.

This slice should not:

- redesign the full heading hierarchy of the remuneration policy;
- change policy ranking or answer-evidence selection;
- alter unrelated ARL guides or FAQs.

## Required Behavior

### 1. Heading deduplication

Acceptance criteria:

- chunk text no longer repeats the same leading heading already represented by
  `section_path`;
- leading heading scaffolds anchored to the same section path are removed
  before prefix injection.

### 2. Chunk readability recovery

Acceptance criteria:

- representative remuneration-policy chunks still preserve their policy text;
- duplicated leading headings are reduced to one readable section prefix.

### 3. Live retrieval validation

Acceptance criteria:

- a representative remuneration-policy query still retrieves the policy family;
- returned chunk surfaces no longer contain the duplicated leading headings
  observed in the baseline.
