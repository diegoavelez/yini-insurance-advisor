# Requirements

## Title

Remediate title and duplicated-heading structure for the `como tomar fotos`
`choque simple` guide.

## Context

After the `choque simple` cohort was ingested and indexed, live retrieval
started surfacing the intended photo-evidence guide. However, the document
still carries a noisy promoted title and repeated section headings inside chunk
text, which degrades citation readability and chunk clarity.

## Scope

This slice should:

- reject the noisy promotional heading as `document_name`;
- keep deterministic fallback naming intact;
- remove duplicated leading headings when section-path prefixing already
  contributes the same structural context.

This slice should not:

- redesign generic title extraction for all documents;
- rework the whole chunking strategy;
- introduce new retrieval heuristics.

## Acceptance Criteria

### 1. Title readability

- The photo guide no longer promotes the noisy heading
  `estas recomendaciones...` as `document_name`.

### 2. Chunk readability

- Chunk text no longer starts with duplicated copies of the same section
  heading when prefix context is already present.

### 3. Backward compatibility

- Focused ingestion tests pass.
