# Requirements

## Title

Bring `MOVILIDAD/TRANSVERSALES` into the current mobility RAG baseline.

## Context

The raw corpus now includes multiple documents under
`data/raw/MOVILIDAD/TRANSVERSALES`. These documents are not a standalone
product; instead they span shared mobility guidance, policy, process, and
portfolio material that can support more than one mobility category.

The next narrow slice should onboard this folder without inventing a new
product taxonomy or broadening retrieval behavior beyond persisted baseline
metadata.

## Scope

This slice should:

1. assign curated baseline metadata for the current `TRANSVERSALES` documents;
2. persist them under the existing `product=movilidad` umbrella;
3. preserve truthful `document_type` values per file using operator-curated
   overlays;
4. record the slice in the roadmap.

This slice should not:

- create a new canonical `transversales` product value;
- add new query-expansion or reranking behavior;
- introduce a new normative document type taxonomy yet;
- broaden supported-query scope for shared operational intents.

## Acceptance Criteria

### 1. Shared mobility product baseline

- Current `MOVILIDAD/TRANSVERSALES` documents persist as `product=movilidad`.

### 2. Curated document-type baseline

- Current `TRANSVERSALES` documents persist with truthful baseline
  `document_type` assignments through the operator-curated overlay layer.

### 3. Backward compatibility

- Focused ingestion tests pass.
- Existing product and document-type inference behavior remains unchanged for
  the already onboarded mobility products.
