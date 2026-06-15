# MVP Acceptance Matrix

## Purpose

This matrix defines the operational acceptance pass for the categories already
onboarded into the current corpus. It is intentionally execution-oriented: the
goal is to prove the current MVP works on the real category set before opening
new category waves or resuming non-blocking coupling refactors.

## Acceptance Status Scale

- `pending` — not executed yet
- `pass` — retrieval and grounded answer both meet expectations
- `fragile-pass` — works, but with known retrieval/citation limitations
- `fail` — retrieval or grounded answer does not meet the target evidence gate

## Shared Gates

Each row is accepted only when all of the following are true:

1. the retrieval query returns the intended category/document family;
2. the grounded answer stays inside the intended evidence family;
3. citations or documentary basis reference the intended document surface;
4. any weakness is written down explicitly as a limitation.

## Execution Order

Run the matrix in this order so the highest-value and already-hardened product
surfaces are proven first:

1. `ARL`
2. `MOVILIDAD/AUTOS`
3. `EPS/PAC`
4. `MOVILIDAD/SOAT`
5. `MOVILIDAD/MUEVETE LIBRE`
6. `MOVILIDAD/MOTOS`
7. `MOVILIDAD/BICICLETAS Y PATINETAS`
8. `MOVILIDAD/VIAJES`
9. `MOVILIDAD/UTILITARIO Y PESADOS`
10. `MOVILIDAD/TRANSVERSALES` / `choque simple`
11. `MOVILIDAD/PV`
12. `MOVILIDAD/FINANCIACION`
13. `MOVILIDAD/SUSCRIPCION`

## Matrix

| Category / family | Retrieval smoke query | Grounded-answer smoke query | Expected primary evidence | Priority | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `ARL` | `¿Cómo consulto la liquidación de comisiones de ARL?` | `¿Cuál es la normatividad que rige el RUI?` | `instructivos consulta de comisiones arl sura v2.pdf`; `preguntas frecuentes registro unico de intermediacion - rui.pdf` | P1 | `pass` | 2026-06-15 live retrieval ranked the commissions guide first; grounded answer returned only the RUI FAQ family with `confidence=high` and the expected normativity section. |
| `MOVILIDAD/AUTOS` | `¿Qué diferencia hay entre los planes de autos?` | `¿Qué cubre el plan autos básico PT?` | `diferenciales planes autos.pdf`; `generalidades plan autos basico pt v2.pdf`; `clausulado seguro de autos.pdf` | P1 | `pass` | 2026-06-15 after `autos-basico-pt-evidence-family-alignment` and `autos-comparison-primary-guide-ranking-recovery`, live retrieval ranks `diferenciales planes autos.pdf` first for the broad comparison smoke query, while the explicit `autos básico PT` answer stays inside `generalidades plan autos basico pt v2.pdf` and surfaces the `Coberturas principales` rows (`Daños a terceros`, `Pérdida total daños`, `Pérdida total hurto`). |
| `EPS/PAC` | `¿Cómo actualizo el correo para factura Global Web?` | `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` | `instructivo actualizacion correo para factura global web v2.pdf`; `politicas asegurabilidad pac 60 mas.pdf` | P1 | `pass` | 2026-06-15 guide retrieval passed for `Global Web`; after `eps-pac-asegurabilidad-policy-family-recovery` and `eps-pac-asegurabilidad-section-priority-recovery`, the policy retrieval and grounded answer for asegurabilidad stay inside `politicas asegurabilidad pac 60 mas.pdf` and now lead with `EDADES Y REQUISITOS...` plus `GRUPOS ASEGURABLES`, rather than operational sections such as `CONGELACIONES` or `REACTIVACIÓN`. |
| `MOVILIDAD/SOAT` | `¿Qué cubre el SOAT?` | `¿Cuáles son las tarifas SOAT 2026?` | `clausulado soat.pdf`; `tarifas soat 2026.pdf` | P1 | `pass` | 2026-06-15 coverage retrieval stayed in the `clausulado soat.pdf` family; after `soat-tariff-table-label-recovery`, live tariff retrieval and answering now stay inside `tarifas soat 2026.pdf` and preserve usable vehicle-category labels instead of raw numeric-only fragments. |
| `MOVILIDAD/MUEVETE LIBRE` | `¿Qué cubre Muévete Libre?` | `¿Qué cubre Muévete Libre?` | `clausulado muevete libre v2.pdf` | P1 | `pass` | 2026-06-15 retrieval and grounded answer both stayed in the normalized `clausulado muevete libre v2.pdf` hierarchy and cited the expected coverage sections `1.2`, `2.1`, `4.1`, `5.1`, and `6.1`. |
| `MOVILIDAD/MOTOS` | `¿Qué diferencia hay entre los planes de motos?` | `¿Qué cubre el plan de motos?` | `comparativo motos.pdf`; `clausulado-plan motos.pdf` | P2 | `pass` | 2026-06-15 live retrieval ranked `comparativo motos.pdf` first for the broad comparison smoke query, and the grounded answer for `¿Qué cubre el plan de motos?` stayed inside `clausulado-plan motos.pdf` with direct `PLAN MOTOS SURA` citations. |
| `MOVILIDAD/BICICLETAS Y PATINETAS` | `¿Cuál es el deducible del seguro de bicicletas y patinetas?` | `¿Qué cubre el seguro para bicicletas y patinetas?` | `pv bicis y patinetas v2.pdf`; `clausulado-bicis y patinetas.pdf` | P2 | `pass` | 2026-06-15 after `bicicletas-patinetas-coverage-policy-family-recovery`, the explicit coverage smoke query stays inside `clausulado-bicis y patinetas.pdf`, while the deductible smoke query again ranks `pv bicis y patinetas v2.pdf` first after narrowing the coverage-only routing rule to avoid injecting the policy family into guide intent. |
| `MOVILIDAD/VIAJES` | `¿Qué cubre el seguro de viaje nacional?` | `¿Qué cubre el seguro de viaje internacional?` | `clausulado viaje nacional v1.pdf`; `clausulado viaje internacional v1.pdf` | P2 | `pass` | 2026-06-15 after `viajes-coverage-section-priority-recovery`, both smokes stay inside their correct clausulado families and now prioritize `SECCIÓN I QUÉ CUBRE ESTE SEGURO` evidence, so national vs international disambiguation and coverage-section recall both pass. |
| `MOVILIDAD/UTILITARIO Y PESADOS` | `¿Qué beneficios tiene el seguro de utilitarios y pesados?` | `¿Qué cubre el plan de utilitarios y pesados?` | `ayudaventas utilitarios y pesados v2.pdf`; `clausulado-plan utilitarios y pesados.pdf` | P2 | `pass` | 2026-06-15 after `utilitarios-pesados-policy-family-recovery`, the guide smoke stays in `ayudaventas utilitarios y pesados v2.pdf` and the policy smoke now cites `SEGURO DE AUTOS PLAN UTILITARIOS Y PESADOS` from `clausulado-plan utilitarios y pesados.pdf` instead of the transversal suscripción policy family. |
| `MOVILIDAD/TRANSVERSALES` / `choque simple` | `¿Cómo debo tomar fotos en un choque simple?` | `¿Cuál es el procedimiento de atención del choque simple?` | `como tomar fotos choque simple v2.pdf`; `proceso atencion choque simple v2.pdf`; `circular choque simple.pdf` | P3 | `pass` | 2026-06-15 after `choque-simple-intent-evidence-routing-recovery`, photo intent now ranks `como tomar fotos choque simple v2.pdf` first, while procedure intent is anchored on `proceso atencion choque simple v2.pdf` with circular support instead of over-relying on the photo guide. |
| `MOVILIDAD/PV` | `¿Qué beneficios incluye la propuesta de valor de movilidad?` | `¿Qué beneficios incluye la propuesta de valor de movilidad?` | `pv planes movilidad v1.pdf`; `pv portafolio movilidad v2.pdf` | P3 | `pass` | 2026-06-15 live retrieval ranked only `PROPUESTA DE VALOR MOVILIDAD` chunks from `pv planes movilidad v1.pdf` plus `pv portafolio movilidad v2.pdf`, and the grounded answer stayed inside that PV family with `confidence=high` while surfacing diverse benefit sections instead of collapsing into repeated applicability text. |
| `MOVILIDAD/FINANCIACION` | `¿Cómo funciona la financiación de pólizas individuales?` | `¿Cómo funciona la financiación de pólizas individuales?` | `instructivo financiacion de polizas v1.pdf` | P3 | `pass` | 2026-06-15 after `movilidad-financiacion-heading-stub-priority-recovery`, live retrieval now ranks the contentful `Paso a paso` chunk first instead of the `Procedimientos:` stub, and the grounded answer stays inside `instructivo financiacion de polizas v1.pdf` with `confidence=high`. Lower-ranked chunks still contain minor OCR compaction, but no longer block MVP acceptance. |
| `MOVILIDAD/SUSCRIPCION` | `¿Cómo funciona la facturación por asegurado en movilidad?` | `¿Qué políticas de suscripción aplican para movilidad?` | `politicas de suscripcion de movilidad.pdf` | P3 | `pass` | 2026-06-15 live retrieval ranked `14.6.2. Facturación (cobro) agrupada con devolución por asegurado` first from `politicas de suscripcion de movilidad.pdf`, and the grounded answer for broader suscripción policies stayed fully inside that same policy family with `confidence=high`. |

## Command Pattern

For each row, run both commands and record the result in the matrix:

```bash
./.venv/bin/python -m rag.ingestion retrieve-chunks \
  --query "<retrieval query>" \
  --top-k 8
```

```bash
./.venv/bin/python -m rag.ingestion answer-query \
  --query "<grounded-answer query>" \
  --top-k 8
```

Use category-specific `--product` and `--document-type` filters only when they
are already part of the validated retrieval contract for that category and help
reduce ambiguity during acceptance.

## Recording Rules

For each executed row, record:

- retrieval result summary;
- whether the intended document family ranked first or near-first;
- grounded-answer confidence;
- citation/documentary-basis document names;
- limitation notes if the row is `fragile-pass` or `fail`.

Do not mark a family as accepted only because ingestion artifacts already exist.
