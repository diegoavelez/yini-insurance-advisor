# Requirements

## Title

Complete live Qdrant indexing and end-to-end query validation for the current
`ARL` corpus.

## Context

The current local repository already contains the full narrow `ARL` cohort in
`data/raw`, with matching processed chunk bundles and embedding artifacts.
However, before this slice there was no evidence in
`data/processed/qdrant-indexing-manifest.jsonl` that those `ARL` embedding
artifacts had actually been indexed into the live Qdrant collection.

That made `ARL` the next narrow operational gap: corpus preparation existed,
but live retrieval and grounded-answer behavior were not yet verified through
the deployed vector store.

## Scope

This slice should:

1. index the existing `ARL` embedding artifacts into the live Qdrant
   collection;
2. validate live retrieval for representative `guide`, `faq`, and `policy`
   queries under `product=arl`;
3. validate at least one live grounded-answer query through Groq on the
   indexed `ARL` corpus;
4. record the operational completion and the next observed quality gap in the
   roadmap and validation notes.

This slice should not:

- re-run PDF ingestion for unchanged `ARL` raw files;
- redesign retrieval ranking globally;
- change supported-scope logic, embeddings, or prompt behavior unless live
  validation proves a code defect;
- broaden into a new category before `ARL` is proven operational end to end.

## Required Behavior

### 1. Live Qdrant indexing

Acceptance criteria:

- the `ARL` embedding artifacts are indexed successfully with the existing
  CLI;
- the Qdrant indexing manifest contains successful `ARL` entries for the four
  current source PDFs.

### 2. Live retrieval validation

Acceptance criteria:

- a representative `guide` query over `ARL` returns the expected account-update
  guidance first;
- a representative `faq` query over `ARL` returns the RUI normativity evidence
  in the top retrieval results;
- a representative `policy` query over `ARL` returns the canal-externo
  remuneration policy family.

### 3. Live grounded-answer validation

Acceptance criteria:

- at least one representative `ARL` question succeeds through
  `answer-query`;
- the answer is supported and cites `ARL` source material from the indexed
  corpus.

### 4. Follow-on gap capture

Acceptance criteria:

- the roadmap records this `ARL` operational slice as closed;
- the roadmap names the next narrow `ARL` quality gap exposed by live
  validation.
