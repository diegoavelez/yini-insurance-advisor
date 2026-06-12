# Requirements

## Feature Summary

This feature defines a corrective runtime slice under
`Phase 15 — Final Evaluation and Cleanup`.

The goal is to restore a practical local embeddings runtime so the current MVP
validation flow can continue through embedding generation, Qdrant indexing, and
one real grounded query against the locally ingested sample corpus.

## In Scope

- Diagnose the current local embeddings-runtime blockage precisely enough to
  avoid speculative dependency churn.
- Apply the smallest safe remediation that restores practical execution of the
  `generate-embeddings` CLI path on the current machine.
- Preserve the existing typed embedding/indexing contracts and downstream CLI
  workflow.
- Record focused evidence for the remediation and the resumed MVP validation
  path.

## Out of Scope

- Broad dependency upgrades unrelated to the identified local runtime blockage.
- Changes to Qdrant retrieval logic, answer-generation contracts, or Gradio UI
  behavior outside the already-found stale smoke fix.
- Hosted deployment changes.

## Acceptance Criteria

- The local embeddings runtime no longer stalls indefinitely during practical
  import/startup on the current machine.
- `generate-embeddings` can run against the current processed sample corpus.
- The remediation is documented as a narrow corrective slice under `Phase 15`.
