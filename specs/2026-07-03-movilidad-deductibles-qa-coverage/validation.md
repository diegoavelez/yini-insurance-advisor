# Validation

This slice is ready when movilidad deductible questions are covered by a focused
QA fixture and deterministic tests.

## Acceptance checks

- `data/eval/movilidad-deductibles-qa.json` contains autos/vehículos, motos,
  bicicletas/patinetas, utilitarios/pesados, and Muévete Libre deductible cases.
- Focused tests confirm each case normalizes to the intended document family.
- Focused tests confirm expected deductible answer terms exist in the local
  processed chunks for each expected family.
- Existing bicicletas/patinetas deductible behavior remains unchanged.

## Verification commands

- `PYTHONPATH=. ./.venv/bin/pytest tests/test_retrieval.py -q -k 'movilidad_deductibles_qa or deductible or deducible'`
- `make test-release`

## Hosted follow-up

After Qdrant/Space health is restored, run the same fixture questions manually in
the hosted UI and confirm citations/documentary basis stay in the expected
families.
