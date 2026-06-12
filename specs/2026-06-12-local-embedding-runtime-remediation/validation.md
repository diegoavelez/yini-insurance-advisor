# Validation

## Status

- Planned on `2026-06-12`.
- Completed on `2026-06-12`.

## Required Checks

- Focused validation that the local embeddings runtime can start and that the
  embedding-generation CLI resumes practical progress on the current machine.

## Required Scenarios

- The root cause of the embeddings runtime blockage is evidenced concretely.
- The remediation restores practical local execution for embeddings generation.
- Downstream MVP validation can resume toward indexing and one real query.

## Merge Readiness

This spec is ready when the local embeddings runtime is no longer the blocking
factor for completing the current MVP validation sequence.

## Evidence

- Repo-local `.venv` import path was evidenced as the blocker:
  - `./.venv/bin/python -c "import torch; print(torch.__version__)"` stalled for
    minutes without completing.
  - `faulthandler` sampling showed the import stuck inside repeated Python-file
    loads under `torch.nn.intrinsic/...`, consistent with pathological package
    import I/O rather than an API or model-resolution failure.
- A clean virtualenv outside the synced workspace restored practical runtime:
  - `/private/tmp/yini-fast-venv311/bin/python -c "import torch"` completed in
    about `8.71s`.
  - `/private/tmp/yini-fast-venv311/bin/python -c "import sentence_transformers"`
    completed in about `60.15s`.
- Embeddings generation then succeeded for the current four-document corpus:
  - `/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --manifest-path data/processed/embedding-generation-manifest.jsonl --overwrite true --fail-fast false`
- Downstream indexing also succeeded:
  - `/private/tmp/yini-fast-venv311/bin/python -m rag.ingestion index-embeddings --embedding-dir data/processed/embeddings --manifest-path data/processed/qdrant-indexing-manifest.jsonl`

## Recorded Outcome

- The blocking factor was narrowed to the local Python runtime location, not to
  the Spanish embedding stack itself.
- MVP validation resumed successfully through embeddings generation and Qdrant
  indexing using the clean external virtualenv.
- Follow-up hardening can later decide whether to formalize an external local
  venv path or replace the heavy local embedding runtime, but the immediate
  remediation objective is satisfied.
