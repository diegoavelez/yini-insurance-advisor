# Validation

Executed checks for this slice:

1. `./.venv/bin/python -m pytest tests/test_ingestion.py -q`
2. `./.venv/bin/python -m ruff check rag/ingestion.py tests/test_ingestion.py`
3. `make batch-ingest BATCH_VENV=./.venv BATCH_MARKDOWN_DIR=data/markdown BATCH_PROCESSED_DIR=data/processed BATCH_GLOB='MOVILIDAD/TRANSVERSALES/pv *.pdf' BATCH_OVERWRITE=true`
4. Inspected:
   - `data/processed/movilidad__transversales__pv-portafolio-movilidad-v2.cleaned.md`
   - `data/processed/chunks/movilidad__transversales__pv-portafolio-movilidad-v2.chunks.json`
   - `data/processed/movilidad__transversales__pv-planes-movilidad-v1.cleaned.md`
   - `data/processed/chunks/movilidad__transversales__pv-planes-movilidad-v1.chunks.json`

Observed outcome:

- Focused ingestion tests pass after adding PV-specific normalization and
  grouping coverage.
- `pv portafolio movilidad v2` now drops most standalone slogan headings and
  shows at least `16` merged benefit + `PLANES QUE APLICA` chunks.
- `pv portafolio movilidad v2` chunk count improves from `119` to `90`.
- `pv planes movilidad v1` remains stable at `102` chunks with no PV-slogan
  residue detected in chunk text.
- The slice materially improves chunk readability and pairing, but does not yet
  collapse the remaining heavy concentration of standalone `PLANES QUE APLICA`
  chunks in `pv portafolio movilidad v2` (`35` section-path hits after the
  rebuild).
- Two inline commercial-tail residues remain in applicability-heavy
  `pv portafolio movilidad v2` chunks, so the next narrow follow-up should
  target applicability-block collapse and residual inline-tail cleanup.

Follow-up note:

- The narrow follow-up was later executed as
  `movilidad-pv-applicability-collapse-and-inline-tail-remediation`, reducing
  `pv portafolio movilidad v2` further from `90` to `82` chunks and removing
  the remaining inline slogan residue from persisted chunk artifacts.
