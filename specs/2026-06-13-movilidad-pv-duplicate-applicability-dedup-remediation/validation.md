# Validation

Executed checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
3. `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/pv *.pdf' BATCH_OVERWRITE=true`
4. Recounted:
   - exact duplicate chunk groups;
   - standalone `PLANES QUE APLICA` chunk count;
   - merged benefit + applicability chunk count.

Observed outcome:

- Focused ingestion tests pass after adding exact standalone applicability
  deduplication.
- `pv portafolio movilidad v2` improves from:
  - `82` to `78` total chunks;
  - `27` to `23` standalone `PLANES QUE APLICA` chunks;
  - `3` duplicate chunk-text groups / `7` duplicate chunks total
    to `0` duplicate groups / `0` duplicate chunks.
- Merged benefit + applicability chunks remain stable at `16`.
- `pv planes movilidad v1` stays stable at `102` chunks with `0` duplicate
  chunk-text groups introduced by the change.

Conclusion:

- The remaining blocker for `PV` indexing is no longer corpus duplication.
- The next narrow slice should move to embedding/runtime readiness rather than
  more `PV` chunk cleanup.
