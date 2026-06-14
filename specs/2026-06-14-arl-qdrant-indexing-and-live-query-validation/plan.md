# Plan

## Objective

Close the remaining operational gap between prepared `ARL` artifacts and live
Qdrant-backed retrieval/answer validation.

## Affected Files

- `specs/roadmap.md`
- `specs/2026-06-14-arl-qdrant-indexing-and-live-query-validation/requirements.md`
- `specs/2026-06-14-arl-qdrant-indexing-and-live-query-validation/plan.md`
- `specs/2026-06-14-arl-qdrant-indexing-and-live-query-validation/validation.md`
- runtime artifact: `data/processed/qdrant-indexing-manifest.jsonl`

## Assumptions

- the current `ARL` chunks and embeddings already reflect the intended corpus;
- environment credentials for Qdrant Cloud and Groq are already configured;
- the main gap is operational proof, not missing baseline code.

## Risks

- live indexing may reveal a collection-schema or payload-index mismatch;
- live retrieval may expose a new ranking or traceability issue that is out of
  scope for this operational slice;
- manifest evidence may exist only as runtime state if the artifact is ignored
  from version control.

## Steps

1. Confirm the current `ARL` embeddings exist but are absent from the Qdrant
   indexing manifest.
2. Index the `ARL` embedding cohort into the live Qdrant collection.
3. Validate representative live `guide`, `faq`, and `policy` retrieval flows.
4. Validate one representative live grounded answer through Groq.
5. Record completion evidence and the next narrow `ARL` corrective slice.

## Verification Strategy

- inspect the Qdrant indexing manifest for successful `ARL` entries;
- run focused live `retrieve-chunks` commands for `guide`, `faq`, and
  `policy`;
- run one focused live `answer-query` command for the `ARL/RUI` path.
