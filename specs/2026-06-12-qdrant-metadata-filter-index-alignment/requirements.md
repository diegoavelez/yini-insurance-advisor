# Requirements

## Title

Align Qdrant collection bootstrap with retrieval-facing metadata filters.

## Context

`Phase 18 — Corpus Metadata and Retrieval Traceability` already introduced
curated `document_type` and `product` metadata overlays plus retrieval-time
filter normalization. A live ARL retrieval check showed that filtered retrieval
can still fail at runtime when the target Qdrant collection contains payload
values but lacks payload indexes for those fields.

The next corrective slice should close that gap at the Qdrant bootstrap layer
without redesigning retrieval contracts or introducing broader collection
migration behavior.

## Scope

This slice should:

1. Ensure Qdrant collection bootstrap creates payload indexes for supported
   metadata filter fields.
2. Keep indexing compatible with client surfaces that do not expose payload
   index creation helpers.
3. Preserve the existing narrow metadata filter scope.

This slice should not:

- add new metadata filter fields;
- redesign indexing manifests;
- introduce destructive collection migration logic;
- depend on manual post-processing outside the indexing command.

## Required Behavior

### 1. Payload-index alignment

The indexing path should create the Qdrant payload indexes required for current
metadata filtering.

Acceptance criteria:

- collection bootstrap creates payload indexes for `document_type` and
  `product`;
- index creation happens after collection creation or collection validation;
- the field schema remains keyword-compatible for exact-match filters.

### 2. Runtime compatibility

The indexing path should remain safe on client versions or doubles that do not
expose payload-index creation.

Acceptance criteria:

- indexing still succeeds when the client lacks `create_payload_index`;
- the behavior degrades by skipping payload-index creation rather than failing
  before point upserts.

### 3. Regression coverage

The repository should cover both the aligned and compatibility paths.

Acceptance criteria:

- focused indexing tests verify payload-index creation on supported clients;
- focused indexing tests verify no crash when payload-index creation is
  unsupported.
