# Requirements

## Title

Align Qdrant collection bootstrap with retrieval-time `document_name` filters.

## Context

The repository already supports retrieval-time `document_name` filters and now
uses that seam to constrain explicit movilidad PV benefit-intent queries to the
`PROPUESTA DE VALOR MOVILIDAD` document family.

Live validation showed that the new retrieval path fails at runtime against the
existing Qdrant Cloud collection with:

- `400 Bad Request`
- `Index required but not found for "document_name"`

This means the retrieval contract is valid, but collection bootstrap still does
not create the payload index required for the new exact-match `document_name`
filter.

The next corrective slice should extend the existing payload-index bootstrap
behavior narrowly enough to cover `document_name` without redesigning retrieval
or collection migration behavior.

## Scope

This slice should:

1. Ensure Qdrant collection bootstrap creates a keyword payload index for
   `document_name`.
2. Preserve existing payload-index behavior for `document_type` and `product`.
3. Keep compatibility with clients that do not expose payload-index helpers.

This slice should not:

- redesign retrieval contracts;
- add destructive migration logic;
- introduce new metadata filters beyond the active `document_name` need;
- require manual collection recreation.

## Required Behavior

### 1. Payload-index bootstrap

Collection bootstrap should create a keyword payload index for
`document_name` alongside the existing retrieval-facing metadata filters.

Acceptance criteria:

- `document_name` is included in the bootstrap payload-index field set;
- supported clients receive a keyword payload-index creation call for
  `document_name`;
- existing `document_type` and `product` bootstrap behavior remains intact.

### 2. Compatibility

The indexing path should remain safe on client surfaces that do not support
payload-index creation.

Acceptance criteria:

- indexing still succeeds when `create_payload_index` is unavailable;
- the code degrades by skipping payload-index creation rather than failing.

### 3. Regression coverage

The repository should cover the expanded bootstrap field set.

Acceptance criteria:

- focused indexing tests assert `document_name` payload-index creation on
  supported clients;
- compatibility-path tests still pass;
- retrieval-focused tests remain green after the bootstrap change.

### 4. Operator follow-up

Because the remote collection already exists, the new bootstrap behavior must be
applied by rerunning an indexing command against that collection.

Acceptance criteria:

- validation notes state that operator rerun is required for the live
  collection;
- the docs do not imply that changing code alone backfills the remote index.
