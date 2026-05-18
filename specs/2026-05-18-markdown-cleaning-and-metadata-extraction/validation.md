# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Scenarios

- The ingestion CLI still serves as the only execution path for this stage.
- A successful run writes:
  - raw Markdown output;
  - cleaned Markdown output;
  - processed metadata output;
  - a manifest record.
- Cleaned Markdown output path follows the deterministic
  `data/processed/<source_pdf_id>.cleaned.md` rule.
- Cleaning behavior is deterministic and does not rewrite semantic content.
- Fallback metadata behavior is explicit when richer extraction is unavailable.
- Cleaning failures are recorded as failed manifest entries with error messages.
- Successful cleaning does not require non-essential metadata extraction.
- Re-runs preserve deterministic paths and respect overwrite behavior.

## Merge Readiness

This spec is ready when the next `Phase 2` slice is decision-complete for:

- conservative Markdown cleaning;
- minimal metadata extraction;
- deterministic processed artifact generation;
- explicit failure handling;

without drifting into semantic chunking or retrieval implementation.
