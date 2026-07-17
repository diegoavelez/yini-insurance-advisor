# Plan

Objective: create deterministic QA coverage for movilidad deductible extraction,
prioritizing autos/vehículos and motos while preserving existing accepted
families.

Affected files:

- `ops/term-equivalences.json`
- `data/eval/movilidad-deductibles-qa.json`
- `tests/test_retrieval.py`
- `specs/2026-07-03-movilidad-deductibles-qa-coverage/`

Assumptions:

- `vehículos` means autos unless another movilidad category is named.
- Categories without explicit deductible evidence must not invent values.
- Local deterministic tests are the acceptance gate because the current live CLI
  path can fail when Qdrant/Space is unavailable.

Risks:

- Overbroad routing could send unrelated movilidad deductible questions to autos.
- Autos small-events value questions must route to the clausulado evidence
  because the ayudaventas only states broad/preferential deductible language.

Verification strategy:

- Validate the QA fixture parses and every case normalizes to expected filters.
- Validate the expected document chunks contain the expected deductible terms.
- Run focused deductible retrieval tests and the release gate if routing changed.
