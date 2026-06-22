# Checklist manual de QA para Hugging Face Spaces

Usa esta tabla para validar manualmente el Space público después de un deploy o rebuild.

## Cómo usarla

1. Abre el Space en Hugging Face.
2. Ejecuta cada pregunta en la UI.
3. Marca `Pass` solo si:
   - la app responde sin error;
   - `Estado de revisión` sigue indicando borrador para revisión del asesor;
   - `Calidad de la respuesta` no cae a un estado inesperado;
   - el bloque principal separa visualmente `Respuesta sugerida` y el acordeón `Citas clave`;
   - `Citas clave` y, cuando aplique, `Base documental` apuntan a la familia documental esperada.
4. Marca `Fail` si hay error, deriva a una familia documental incorrecta o la respuesta no corresponde a la intención.
5. Usa `Notas` para registrar drift de evidencia, citas ruidosas o respuestas incompletas.

## Campos de ejecución

- Fecha de prueba: `_____________`
- Commit / SHA desplegado: `_____________`
- URL del Space: `_____________`
- Operador: `_____________`

## Smoke base del Space

| ID | Tipo | Verificación | Pass | Fail | Notas |
| --- | --- | --- | --- | --- | --- |
| `space-ui-001` | Carga | La app carga correctamente en el navegador. | [ ] | [ ] | |
| `space-ui-002` | Estado | `Estado del servicio` muestra estado listo. | [ ] | [ ] | |
| `space-ui-003` | Layout | La UI muestra un encabezado visible para `Respuesta sugerida`, un acordeón visible de `Citas clave`, además de `Detalles de revisión` y `Diagnóstico técnico`. | [ ] | [ ] | |
| `space-ui-004` | Error | Antes de preguntar, `Estado de error` no muestra fallo activo. | [ ] | [ ] | |

## Preguntas manuales por familia aceptada del MVP

| ID | Familia | Tipo | Pregunta | Evidencia esperada | Criterio de pass | Pass | Fail | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `mvp-arl-r1` | `ARL` | Retrieval | `¿Cómo consulto la liquidación de comisiones de ARL?` | `instructivos consulta de comisiones arl sura v2.pdf` | La respuesta y/o citas apuntan a la guía de consulta de comisiones ARL. | [ ] | [ ] | |
| `mvp-arl-a1` | `ARL` | Answer | `¿Cuál es la normatividad que rige el RUI?` | `preguntas frecuentes registro unico de intermediacion - rui.pdf` | La respuesta cita el FAQ de RUI y responde la normatividad sin deriva a otra familia. | [ ] | [ ] | |
| `mvp-autos-r1` | `MOVILIDAD/AUTOS` | Retrieval | `¿Qué diferencia hay entre los planes de autos?` | `diferenciales planes autos.pdf` | Las citas clave reflejan el comparativo de planes de autos. | [ ] | [ ] | |
| `mvp-autos-a1` | `MOVILIDAD/AUTOS` | Answer | `¿Qué cubre el plan autos básico PT?` | `generalidades plan autos basico pt v2.pdf` | La respuesta resume coberturas del plan básico PT y cita esa familia. | [ ] | [ ] | |
| `mvp-pac-r1` | `EPS/PAC` | Retrieval | `¿Cómo actualizo el correo para factura Global Web?` | `instructivo actualizacion correo para factura global web v2.pdf` | La respuesta remite al instructivo correcto de Global Web. | [ ] | [ ] | |
| `mvp-pac-a1` | `EPS/PAC` | Answer | `¿Qué condiciones de asegurabilidad tiene PAC 60 Más?` | `politicas asegurabilidad pac 60 mas.pdf` | La respuesta usa la política de asegurabilidad de PAC 60 Más, no otra familia PAC. | [ ] | [ ] | |
| `mvp-soat-r1` | `MOVILIDAD/SOAT` | Retrieval | `¿Qué cubre el SOAT?` | `clausulado soat.pdf` | La respuesta cita el clausulado SOAT para coberturas. | [ ] | [ ] | |
| `mvp-soat-a1` | `MOVILIDAD/SOAT` | Answer | `¿Cuáles son las tarifas SOAT 2026?` | `tarifas soat 2026.pdf` | La respuesta cita la tarifa 2026 y no deriva al clausulado. | [ ] | [ ] | |
| `mvp-muevete-r1` | `MOVILIDAD/MUEVETE LIBRE` | Retrieval | `¿Qué cubre Muévete Libre?` | `clausulado muevete libre v2.pdf` | La evidencia principal viene del clausulado Muévete Libre. | [ ] | [ ] | |
| `mvp-muevete-a1` | `MOVILIDAD/MUEVETE LIBRE` | Answer | `¿Qué cubre Muévete Libre?` | `clausulado muevete libre v2.pdf` | La respuesta mantiene la misma familia documental y resume coberturas. | [ ] | [ ] | |
| `mvp-motos-r1` | `MOVILIDAD/MOTOS` | Retrieval | `¿Qué diferencia hay entre los planes de motos?` | `comparativo motos.pdf` | Las citas clave reflejan el comparativo de motos. | [ ] | [ ] | |
| `mvp-motos-a1` | `MOVILIDAD/MOTOS` | Answer | `¿Qué cubre el plan de motos?` | `clausulado-plan motos.pdf` | La respuesta cita el clausulado del plan de motos. | [ ] | [ ] | |
| `mvp-bicis-r1` | `MOVILIDAD/BICICLETAS Y PATINETAS` | Retrieval | `¿Cuál es el deducible del seguro de bicicletas y patinetas?` | `pv bicis y patinetas v2.pdf` | La respuesta y las citas aterrizan en el documento PV de bicis y patinetas. | [ ] | [ ] | |
| `mvp-bicis-a1` | `MOVILIDAD/BICICLETAS Y PATINETAS` | Answer | `¿Qué cubre el seguro para bicicletas y patinetas?` | `clausulado-bicis y patinetas.pdf` | La respuesta cita el clausulado y no deriva a suscripción general. | [ ] | [ ] | |
| `mvp-viajes-r1` | `MOVILIDAD/VIAJES` | Retrieval | `¿Qué cubre el seguro de viaje nacional?` | `clausulado viaje nacional v1.pdf` | Las citas clave deben reflejar viaje nacional. | [ ] | [ ] | |
| `mvp-viajes-a1` | `MOVILIDAD/VIAJES` | Answer | `¿Qué cubre el seguro de viaje internacional?` | `clausulado viaje internacional v1.pdf` | La respuesta debe citar la familia internacional, no la nacional. | [ ] | [ ] | |
| `mvp-utilitarios-r1` | `MOVILIDAD/UTILITARIO Y PESADOS` | Retrieval | `¿Qué beneficios tiene el seguro de utilitarios y pesados?` | `ayudaventas utilitarios y pesados v2.pdf` | La evidencia principal viene del ayudaventas. | [ ] | [ ] | |
| `mvp-utilitarios-a1` | `MOVILIDAD/UTILITARIO Y PESADOS` | Answer | `¿Qué cubre el plan de utilitarios y pesados?` | `clausulado-plan utilitarios y pesados.pdf` | La respuesta cita el clausulado dedicado, no suscripción movilidad. | [ ] | [ ] | |
| `mvp-choque-r1` | `MOVILIDAD/TRANSVERSALES/choque simple` | Retrieval | `¿Cómo debo tomar fotos en un choque simple?` | `como tomar fotos choque simple v2.pdf` | La respuesta remite a la guía de fotos, no a pólizas de otra categoría. | [ ] | [ ] | |
| `mvp-choque-a1` | `MOVILIDAD/TRANSVERSALES/choque simple` | Answer | `¿Cuál es el procedimiento de atención del choque simple?` | `proceso atencion choque simple v2.pdf` y `circular choque simple.pdf` | La respuesta debe mantenerse en la familia de choque simple y citar el procedimiento/circular. | [ ] | [ ] | |
| `mvp-pv-r1` | `MOVILIDAD/PV` | Retrieval | `¿Qué beneficios incluye la propuesta de valor de movilidad?` | `pv planes movilidad v1.pdf` y `pv portafolio movilidad v2.pdf` | La evidencia se mantiene en la familia PV de movilidad. | [ ] | [ ] | |
| `mvp-pv-a1` | `MOVILIDAD/PV` | Answer | `¿Qué beneficios incluye la propuesta de valor de movilidad?` | `pv planes movilidad v1.pdf` y `pv portafolio movilidad v2.pdf` | La respuesta resume beneficios y cita la familia PV sin deriva lateral. | [ ] | [ ] | |
| `mvp-financiacion-r1` | `MOVILIDAD/FINANCIACION` | Retrieval | `¿Cómo funciona la financiación de pólizas individuales?` | `instructivo financiacion de polizas v1.pdf` | La evidencia principal viene del instructivo de financiación. | [ ] | [ ] | |
| `mvp-financiacion-a1` | `MOVILIDAD/FINANCIACION` | Answer | `¿Cómo funciona la financiación de pólizas individuales?` | `instructivo financiacion de polizas v1.pdf` | La respuesta se mantiene en la misma familia y explica el flujo. | [ ] | [ ] | |
| `mvp-suscripcion-r1` | `MOVILIDAD/SUSCRIPCION` | Retrieval | `¿Cómo funciona la facturación por asegurado en movilidad?` | `politicas de suscripcion de movilidad.pdf` | La respuesta debe citar la política de suscripción de movilidad. | [ ] | [ ] | |
| `mvp-suscripcion-a1` | `MOVILIDAD/SUSCRIPCION` | Answer | `¿Qué políticas de suscripción aplican para movilidad?` | `politicas de suscripcion de movilidad.pdf` | La respuesta debe mantenerse en la familia de suscripción y responder de forma general. | [ ] | [ ] | |

## Resumen final

- Total `Pass`: `_____`
- Total `Fail`: `_____`
- Bloqueadores encontrados: `_____________________________________________`
- Acción siguiente recomendada: `_____________________________________________`
