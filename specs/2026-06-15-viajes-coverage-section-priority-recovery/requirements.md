# Requirements

## Title

Recover coverage-section priority for VIAJES coverage smokes.

## Context

The MVP acceptance row for `MOVILIDAD/VIAJES` is still pending. Live smokes already disambiguate correctly into the national and international clausulado families, so no family-routing fix is needed. The remaining issue is narrower: explicit `¿Qué cubre ...?` queries rank exclusion and operational sections above the available `SECCIÓN I QUÉ CUBRE ESTE SEGURO` chunks.

## Scope

This slice should:

1. Add one viajes-specific coverage expansion rule that boosts the real `QUÉ CUBRE` sections for both national and international policy queries.
2. Preserve the existing national/international document-family routing.
3. Add focused regressions for repository-loaded equivalences and retrieval query expansion.
4. Update roadmap and the acceptance matrix when the row passes.

This slice should not:

- re-chunk VIAJES documents;
- redesign the answer generator;
- broaden to generic luggage-only or assistance-only retrieval logic.

## Required Behavior

### 1. Coverage recall enrichment

Acceptance criteria:

- explicit VIAJES coverage queries append coverage-oriented recall terms such as `SECCIÓN I QUÉ CUBRE ESTE SEGURO`, `hurto de documentos`, `equipaje protegido`, and `cancelación e interrupción de viaje`;
- existing `document_name` routing for `viaje nacional` and `viaje internacional` remains unchanged.

### 2. Retrieval and answer alignment

Acceptance criteria:

- live retrieval for `¿Qué cubre el seguro de viaje nacional?` stays inside `clausulado viaje nacional v1.pdf` and surfaces a `SECCIÓN I QUÉ CUBRE ESTE SEGURO` chunk in the top results;
- live grounded answering for `¿Qué cubre el seguro de viaje internacional?` stays inside `clausulado viaje internacional v1.pdf` and cites `SECCIÓN I QUÉ CUBRE ESTE SEGURO` evidence.

### 3. Regression safety

Acceptance criteria:

- focused tests cover the viajes coverage expansion rule;
- existing viajes national/international document-name normalization tests still pass.
