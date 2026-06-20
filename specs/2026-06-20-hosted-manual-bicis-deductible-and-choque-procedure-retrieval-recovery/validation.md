# Validation

This slice is ready when the hosted manual MVP regressions for bicicletas/patinetas deductible and choque simple procedure are deterministically routed back into their intended document families.

## Acceptance checks

- A committed spec bundle exists for `hosted-manual-bicis-deductible-and-choque-procedure-retrieval-recovery`.
- The term-equivalence file contains a deterministic bicicletas/patinetas deductible `document_name` rule.
- The term-equivalence file contains a deterministic choque simple procedure `document_name` rule.
- Focused tests confirm both hosted-style queries normalize to the intended families without caller filters.
- Existing repository tests for bicicletas/patinetas coverage and choque simple photo intent still pass.
- Roadmap and acceptance-matrix notes disclose the hosted manual regression and this corrective slice.

## Verification commands

- `PYTHONPATH=. ./.venv/bin/pytest tests/test_retrieval.py -q -k 'repository_bicicletas_patinetas_deductible_hosted or repository_choque_simple_procedure_hosted or bicicletas_patinetas_coverage or choque_simple_photo'`
