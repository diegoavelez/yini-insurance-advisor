# Requirements

## Title

Movilidad deductible QA coverage.

## Context

The user reported difficulty extracting deductible values. The prior automated
coverage focused on bicicletas/patinetas, but deductible questions are common
across movilidad, especially autos/vehículos and motos.

## Scope

This slice should:

1. Add a focused QA fixture for movilidad deductible questions.
2. Add deterministic tests that verify intended document-family routing and
   expected deductible evidence terms.
3. Add narrow term-equivalence routing only for deductible intents with explicit
   product/category signals.
4. Preserve the existing bicicletas/patinetas deductible path.

This slice should not:

- add a broad `movilidad + deducible` catch-all;
- require live Qdrant or hosted Space access for local acceptance;
- change public APIs or response contracts.

## Required Behavior

- Autos/vehículos deductible questions route to `SEGURO DE AUTOS` unless they
  explicitly target Autos Básico PT or small-event assistances.
- Autos Básico PT deductible questions keep routing to
  `Plan Autos Básico Pérdidas Totales`.
- Autos assistance deductible questions route to `SEGURO DE AUTOS`, where the
  concrete assistance deductible values are available.
- Motos general deductible questions route to `PLAN MOTOS SURA`.
- Motos small-event deductible questions route to the motos small-events guide.
- Bicicletas/patinetas deductible questions keep routing to
  `pv bicis y patinetas v2`.
- Utilitarios/pesados and Muévete Libre deductible questions route to their
  corresponding policy families.
