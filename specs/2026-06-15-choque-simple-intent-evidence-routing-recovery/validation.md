# Validation

This slice is ready when choque simple photo intent lands in the photo guide and procedure intent prioritizes the operational procedure/circular family.

## Acceptance Checks

- A committed spec bundle exists for `choque-simple-intent-evidence-routing-recovery`.
- Photo-intent queries normalize to `¿Cómo tomar fotos y videos?`.
- Procedure-intent queries append operational recall anchors.
- Live photo retrieval ranks `como tomar fotos choque simple v2.pdf` first.
- Live procedure answering cites `proceso atencion choque simple v2.pdf` and/or `circular choque simple.pdf` rather than anchoring on the photo guide.

## Verification Commands

- `./.venv/bin/python -m pytest tests/test_retrieval.py -q -k 'choque_simple_photo or choque_simple_procedure'`
- `./.venv/bin/python -m ruff check tests/test_retrieval.py rag/evidence_selection.py --ignore E501`
- `./.venv/bin/python -m rag.ingestion retrieve-chunks --query '¿Cómo debo tomar fotos en un choque simple?' --product movilidad --top-k 5`
- `./.venv/bin/python -m rag.ingestion answer-query --query '¿Cuál es el procedimiento de atención del choque simple?' --product movilidad --top-k 5`
