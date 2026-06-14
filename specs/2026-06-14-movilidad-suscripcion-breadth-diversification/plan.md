# Plan

## Objective

Reduce duplicate subsection concentration in broad suscripción retrieval while
keeping contentful evidence first.

## Affected Files

- `rag/ingestion.py`
- `tests/test_retrieval.py`
- `specs/roadmap.md`
- `specs/2026-06-14-movilidad-suscripcion-heading-stub-evidence-prioritization/validation.md`
- `specs/2026-06-14-movilidad-suscripcion-breadth-diversification/requirements.md`
- `specs/2026-06-14-movilidad-suscripcion-breadth-diversification/plan.md`
- `specs/2026-06-14-movilidad-suscripcion-breadth-diversification/validation.md`

## Assumptions

- broad suscripción queries now reach enough useful candidate chunks;
- the remaining issue is result concentration, not family leakage or heading
  stubs;
- a narrow deterministic diversification rule should be sufficient.

## Risks

- over-diversifying and hiding the best supporting chunk for a strong section;
- applying breadth logic too broadly outside the suscripción family;
- regressing specific subsection queries that legitimately need repeated local
  evidence.

## Steps

1. Capture the repeated-subsection live pattern.
2. Add the smallest suscripción-specific breadth rule.
3. Add focused regression coverage.
4. Re-run the live suscripción broad query.

## Verification Strategy

- run focused retrieval tests;
- run Ruff on touched files;
- re-run at least one live broad suscripción retrieval query.
