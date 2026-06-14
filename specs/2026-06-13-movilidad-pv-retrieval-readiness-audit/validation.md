# Validation

Executed checks for this slice:

1. Structural audit over:
   - `data/processed/chunks/movilidad__transversales__pv-portafolio-movilidad-v2.chunks.json`
   - `data/processed/chunks/movilidad__transversales__pv-planes-movilidad-v1.chunks.json`
2. `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path data/processed/embedding-manifest.jsonl --glob 'movilidad__transversales__pv-*.chunks.json' --overwrite true --fail-fast true`

Observed outcome:

- `pv portafolio movilidad v2` currently persists:
  - `82` total chunks;
  - `27` standalone `PLANES QUE APLICA` chunks (`~32.9%`);
  - `16` merged benefit + applicability chunks;
  - `0` residual slogan hits.
- `pv planes movilidad v1` currently persists:
  - `102` total chunks;
  - `0` standalone applicability chunks;
  - `0` slogan residue.
- Exact duplicate-surface audit still finds `3` duplicate text groups in
  `pv portafolio movilidad v2`, representing `7` duplicate chunks total.
- The duplicate groups are all applicability-heavy `PLANES QUE APLICA` chunks,
  which means the remaining readiness risk is no longer general noise, but
  retrieval dilution from repeated plan-applicability evidence.
- The local embedding-generation attempt does not invalidate the corpus itself,
  but it does fail in this environment because the configured multilingual
  sentence-transformer cannot be resolved from `huggingface.co`.

Decision at audit time:

- `NO-GO` for embeddings/indexing yet.
- Reason 1: `pv portafolio movilidad v2` still had repeated exact duplicate
  applicability chunks that were likely to waste vector budget and dilute top-k
  retrieval.
- Reason 2: local embedding generation was blocked by model-download network
  resolution in this environment, so runtime readiness was not demonstrated.

Follow-up note:

- The corpus-side duplicate issue was later addressed in
  `movilidad-pv-duplicate-applicability-dedup-remediation`, which reduced
  `pv portafolio movilidad v2` to `78` chunks with `0` exact duplicate chunk
  groups. The remaining blocker is now embedding-runtime readiness only.
