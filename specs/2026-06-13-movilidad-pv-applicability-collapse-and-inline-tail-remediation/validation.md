# Validation

Executed checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
3. `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/pv *.pdf' BATCH_OVERWRITE=true`
4. Inspected:
   - `data/processed/chunks/movilidad__transversales__pv-portafolio-movilidad-v2.chunks.json`
   - `data/processed/chunks/movilidad__transversales__pv-planes-movilidad-v1.chunks.json`

Observed outcome:

- Focused ingestion tests pass after adding:
  - no-overlap control for pure `PV` applicability chunks;
  - equivalent heading collapse for `Plan que aplica` variants;
  - cleanup of heading-prefixed applicability bodies.
- `pv portafolio movilidad v2` chunk count improves further from `90` to `82`.
- Standalone commercial-slogan residue in `pv portafolio movilidad v2` drops
  from `1` residual hit to `0`.
- Merged benefit + `PLANES QUE APLICA` chunks remain stable at `16`.
- Standalone `PLANES QUE APLICA` section-path hits reduce from `35` to `27`.
- `pv planes movilidad v1` remains stable at `102` chunks with no slogan
  residue introduced by the overlap change.

Residual gap:

- `pv portafolio movilidad v2` still has a relatively heavy concentration of
  standalone `PLANES QUE APLICA` chunks, so the next reasonable follow-up is a
  narrower applicability-density or retrieval-readiness slice rather than more
  generic cleanup.
