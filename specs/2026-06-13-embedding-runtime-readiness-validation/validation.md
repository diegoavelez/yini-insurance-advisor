# Validation

Executed checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_embedding_generation.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_embedding_generation.py`
3. `./.venv/bin/python -m rag.ingestion generate-embeddings --chunk-dir data/processed/chunks --embedding-dir data/processed/embeddings --manifest-path /tmp/pv-embedding-readiness-manifest.jsonl --glob 'movilidad__transversales__pv-*.chunks.json' --overwrite false --fail-fast true`
4. Attempted: `./.venv/bin/python -m rag.ingestion warmup-embedding-assets`

Observed outcome:

- The CLI now exposes `warmup-embedding-assets`.
- Embedding generation now prefers offline cached assets by default and fails
  immediately with an actionable message when the model is not cached locally.
- In this environment, the offline readiness check fails fast as expected for
  `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, with an
  instruction to run `python -m rag.ingestion warmup-embedding-assets` or
  pre-populate the Hugging Face cache.
- A live networked warm-up attempt could not be validated inside this harness
  because escalated network approval for public model download was rejected by
  environment policy.

Conclusion:

- The runtime seam is now correct and explicit.
- The remaining step is operational rather than code-level: run the warm-up
  command on a machine/session allowed to download the model once, then execute
  embeddings and indexing.
