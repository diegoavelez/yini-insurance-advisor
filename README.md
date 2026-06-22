---
title: Yini Insurance Advisor
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Yini

Yini es un asistente interno diseñado para ayudar a asesores senior de seguros
a recuperar, analizar, comparar y resumir información a partir de documentos
oficiales de pólizas y procedimientos de seguros de Sura.

Este repositorio contiene actualmente la `Phase 0` completada de fundación, la
`Phase 1` completa de configuración y contratos compartidos, el pipeline
implementado de ingestión y chunking de `Phase 2` y `Phase 3`, el pipeline
completo de embeddings e indexación de `Phase 4`, la capa MVP de QA completada
de `Phase 5`, la base de observabilidad completada de `Phase 6`, la capa de
tooling reutilizable completada de `Phase 7`, la capa de orquestación de
workflow completada de `Phase 8`, la capa de guardrails completada de
`Phase 9`, la base de evaluación implementada de `Phase 10`, la base de
optimización completada de `Phase 11`, la base MCP completada de `Phase 12`,
el hardening del demo completado de `Phase 13`, el hardening de despliegue
completado de `Phase 14`, el trabajo final de evaluación y cleanup completado
de `Phase 15`, el trabajo completado de remediación del runtime de ingestión
de `Phase 16`, el hardening de compatibilidad de runtime completado de
`Phase 17`, el trabajo completado de metadata de corpus y trazabilidad de
retrieval de `Phase 18`, y el trabajo completado de legibilidad de citas y
trazabilidad para operadores de `Phase 19`.

## Documentos fuente

- `PRD.md` es la fuente de verdad de requerimientos de producto.
- `specs/mission.md` contiene principios del producto y anti-objetivos.
- `specs/tech-stack.md` contiene restricciones del stack y límites
  arquitectónicos.
- `specs/roadmap.md` contiene el orden de implementación y el estado actual de la solución.
- `docs/evaluation-report.md` contiene la línea base actual de evaluación del MVP.
- `docs/mvp-go-live.md` contiene la línea base operativa actual de go-live del MVP.
- `specs/` también contiene especificaciones fechadas de implementación.

## Estado actual

- `Phase 0` hasta `Phase 19` están completas.
- El estado detallado de implementación vive en `specs/roadmap.md`.

## Configuración local

Usa un entorno virtual local para todo el desarrollo.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
cp .env.example .env
```

Si solo necesitas instalar las dependencias de runtime en un entorno que espera
`pip` + `requirements.txt`, puedes usar:

```bash
pip install -r requirements.txt
```

En este repositorio, `pyproject.toml` sigue siendo la fuente de verdad de las
dependencias; `requirements.txt` es un export de compatibilidad para runtime.

Si `python3.11` no está disponible en tu shell, usa cualquier ejecutable de
Python 3.11+ en su lugar. El proyecto no soporta Python 3.10.

## Comandos comunes

```bash
make setup
make lint
make test
make test-release
make app
```

## Línea base final de pruebas del MVP

La compuerta determinística autoritativa previa a release para el MVP actual es:

```bash
make test-release
```

Esta compuerta reutiliza intencionalmente las superficies de pruebas locales ya
commiteadas y evita exigir llamadas live frescas a Groq o Qdrant Cloud.

Superficies protegidas:

- assets de evaluación y cobertura smoke tipo hosted;
- compatibilidad MCP y seams de roundtrip local;
- UI Gradio, observabilidad, scope soportado, guardrails y comportamiento del workflow;
- retrieval, respuesta fundamentada, embeddings, indexación, runtime CLI e ingestión.

No son bloqueantes, pero siguen siendo útiles:

- `make test` para la suite completa de regresión local;
- onboarding dirigido por categoría o validación live de providers cuando el
  corpus o el runtime cambien de forma material;
- corridas externas de batch-ingestion bajo el flujo de operador documentado.

## Reproducción local con Docker

Si quieres reproducir la app localmente con el mismo contenedor base usado para
el despliegue, puedes usar el `Dockerfile` raíz.

Pasos mínimos:

1. Crea tu archivo local de variables:

   ```bash
   cp .env.example .env
   ```

2. Completa en `.env` como mínimo:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`

3. Construye la imagen:

   ```bash
   docker build -t yini-insurance-advisor .
   ```

4. Ejecuta el contenedor:

   ```bash
   docker run --rm \
     -p 7860:7860 \
     --env-file .env \
     yini-insurance-advisor
   ```

5. Abre la app en tu navegador:

   - `http://localhost:7860`

Notas:

- el contenedor usa `python -m app.ui` como entrypoint;
- el puerto expuesto es `7860`;
- durante el build se instalan dependencias y se hace warm-up de assets de embeddings;
- si faltan credenciales reales de Groq o Qdrant, la UI puede cargar pero no
  responder consultas fundamentadas correctamente.

## Despliegue en Hugging Face Spaces

Este repositorio está configurado actualmente para un Hugging Face Space basado
en Docker.

Superficies autoritativas de despliegue:

- bloque YAML raíz de `README.md`:
  - `sdk: docker`
  - `app_port: 7860`
- `Dockerfile` raíz

Procedimiento mínimo para el operador:

1. Crea un nuevo Hugging Face Space y elige el SDK `Docker`.
2. Haz push de este repositorio al repositorio del Space, preservando el bloque
   YAML raíz de `README.md` y el `Dockerfile` raíz.
3. En la configuración del Space, define los secrets o variables de runtime
   requeridos por el contrato actual de arranque:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
4. Deja que el Space reconstruya automáticamente después del push.
5. Confirma que el Space sirve la app en el puerto `7860`, en línea con
   `app_port` del `README.md` raíz.

Space desplegado actualmente:

- URL de la página:
  `https://huggingface.co/spaces/Diegoavelez/Yini-insurance-advisor`

Notas:

- El runtime del Space usa el `Dockerfile` raíz como artefacto autoritativo de build.
- Cada nuevo commit enviado al repositorio del Space dispara un rebuild y reinicio.
- Esta sección se limita intencionalmente al procedimiento de despliegue; las
  restricciones operativas del demo y las notas de rollback se documentan en
  slices posteriores.

## Notas de rollback de despliegue

Estas notas cubren únicamente la guía mínima de rollback para la ruta actual de
despliegue hosted del demo.

Postura actual de rollback:

- el target hosted sigue siendo un Hugging Face Space configurado con:
  - `sdk: docker`
  - `Dockerfile` raíz
- la unidad práctica de rollback es un estado previo conocido como bueno del repo
- restaurar ese estado conocido como bueno en el repositorio del Space dispara
  un nuevo rebuild del demo hosted

Procedimiento mínimo de rollback:

1. Identifica el último commit conocido como bueno para el repositorio del Space.
2. Restaura o vuelve a hacer push de ese estado del repo al repositorio del Space.
3. Conserva las superficies autoritativas de despliegue en el estado restaurado:
   - bloque YAML raíz de `README.md`
   - `Dockerfile` raíz
4. Confirma que las variables de runtime requeridas siguen configuradas en el Space:
   - `GROQ_API_KEY`
   - `GROQ_MODEL`
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
5. Deja que el Space reconstruya a partir del estado restaurado del repo.

Límite de esta sección:

- esta sección se limita intencionalmente a la guía de rollback
- las expectativas smoke hosted, notas de runtime/dependencias y notas de
  restricciones del demo se documentan en slices separados

## Restricciones de runtime y dependencias del demo

Estas notas cubren únicamente la postura actual de runtime/dependencias del
demo hosted en el Hugging Face Space basado en Docker.

Supuestos actuales de runtime:

- el target hosted sigue siendo un Hugging Face Space configurado con:
  - `sdk: docker`
  - `app_port: 7860`
- el artefacto autoritativo de build es el `Dockerfile` raíz
- el entrypoint autoritativo de la app es:
  - `python -m app.ui`

Contrato actual de variables de arranque:

- `GROQ_API_KEY` debe existir en runtime
- `GROQ_MODEL` debe existir en runtime o resolver al default validado
  `openai/gpt-oss-120b`
- `QDRANT_URL` debe existir en runtime
- `QDRANT_API_KEY` debe existir en runtime

Restricciones actuales de dependencias/runtime:

- el runtime del contenedor debe exponer el puerto `7860`, en línea con la
  configuración de Spaces del `README.md` raíz y el `Dockerfile` raíz
- la imagen actual es pesada en dependencias e incluye paquetes de ML y
  procesamiento documental instalados durante `pip install .`; hay que asumir
  que los tiempos de build y el tamaño de imagen no serán triviales
- la validación local del contenedor usó valores dummy de provider solo para
  checks de startup y readiness; un demo hosted todavía necesita configuración
  real de providers para soportar retrieval live y generación de respuestas

Límite de esta sección:

- esta sección se limita intencionalmente a restricciones de runtime y dependencias
- las notas de guardrails/scope del demo y las notas de rollback se documentan
  en slices posteriores

## Restricciones de guardrails y rechazos del demo

Estas notas cubren únicamente la postura de guardrails/rechazos del demo
hosted para la superficie pública actual dirigida al asesor.

Comportamiento actual de guardrails/rechazos:

- consultas estilo prompt injection se rechazan de forma conservadora antes de
  que corra la ruta normal de respuesta fundamentada
- rutas de generación de respuestas que pierden trazabilidad de citas se
  degradan a un borrador de menor confianza en lugar de presentarse como salida
  fundamentada normal
- la confianza sobreafirmada se degrada antes de mostrar el borrador final en
  la UI del demo

Efecto visible actual para el usuario:

- los caminos conservadores de guardrails siguen orientados a borrador y
  revisión, en lugar de presentarse como respuestas finales completamente fundamentadas
- el demo expone esos resultados mediante:
  - limitaciones
  - resumen de trazabilidad
  - contexto de soporte
  - metadata de depuración
  - mensajería de calidad de respuesta

Límite de esta sección:

- esta sección se limita intencionalmente a restricciones de guardrails/rechazos
- las notas de scope soportado, runtime/dependencias y rollback se documentan
  en secciones separadas

## Restricciones de scope soportado del demo

Estas notas cubren únicamente el límite actual de scope soportado del demo
hosted para la superficie pública actual dirigida al asesor.

Postura actual de scope soportado:

- el demo está pensado para preguntas fundamentadas sobre documentos soportados
  de pólizas y procedimientos de seguros en la superficie actual del asesor
- solicitudes fuera de ese scope soportado de documentos de seguros se
  rechazan antes de correr la ruta normal de respuesta fundamentada
- las solicitudes no soportadas se exponen como respuestas orientadas a
  borrador y baja confianza, no como respuestas fundamentadas normales

Efecto visible actual para el usuario:

- los resultados de scope no soportado aparecen mediante:
  - limitaciones
  - resumen de trazabilidad
  - contexto de soporte
  - metadata de depuración
  - mensajería de calidad de respuesta
- las solicitudes no soportadas no continúan hacia la ruta normal de
  generación de respuesta fundamentada

Límite de esta sección:

- esta sección se limita intencionalmente a restricciones de scope soportado
- las notas de runtime/dependencias, guardrails/rechazos y rollback se
  documentan en slices separados

## Expectativas smoke hosted y notas para operadores

Estas notas cubren únicamente las expectativas smoke mínimas del demo
desplegado y los checks estrechos que debe ejecutar el operador después de un
deploy o rebuild.

Expectativas smoke hosted actuales:

- el Space debe servir la app en el puerto `7860`
- la UI pública debe renderizar las superficies actuales del demo, incluyendo:
  - `Estado del servicio`
  - `Respuesta sugerida`
  - acordeón `Citas clave`
  - `Estado de revisión`
  - `Confianza`
  - `Calidad de la respuesta`
  - `Estado de error`
- se espera que la superficie hosted de readiness reporte:
  - `Estado del servicio — Listo para generar borradores fundamentados.`
- una consulta benigna y dentro de scope debe mantener:
  - `Calidad de la respuesta — Calidad estándar del borrador.`
  - `No hay errores activos.`
  - `Se requiere revisión del asesor antes del uso externo.`

Checks mínimos del operador después de deploy/rebuild:

1. Abre el Space hosted y confirma que la app carga correctamente.
2. Confirma que la página renderiza las secciones actuales del demo, en especial:
   - `Estado del servicio`
   - `Respuesta sugerida`
   - acordeón `Citas clave`
   - `Estado de revisión`
   - `Diagnóstico técnico`
3. Confirma que la superficie de readiness reporta el estado listo y no un
   mensaje degradado de runtime.
4. Envía una consulta benigna y dentro de scope sobre documentos de seguros y confirma:
   - la respuesta se devuelve como borrador;
   - `Citas clave` apunta a la familia documental esperada;
   - no se muestra ningún estado de error activo;
   - la calidad de la respuesta permanece en el estado estándar del borrador.

Límite de esta sección:

- esta sección se limita intencionalmente a expectativas smoke hosted y checks
  del operador
- la guía de rollback, las notas de runtime/dependencias y las notas de
  restricciones del demo se documentan en slices separados

## UI Gradio del MVP

El entrypoint actual de la app es una capa delgada de Gradio sobre el backend
de QA fundamentado.

Comando canónico:

```bash
python -m app.ui
```

La UI expone:

- entrada de pregunta del asesor
- botones de acceso rápido para tipos comunes de consulta
- respuesta fundamentada sugerida
- acordeón compacto `Citas clave` bajo la superficie de respuesta
- panel de revisión con `Estado de revisión`, `Confianza`, `Calidad de la respuesta`
- `Base documental y evidencia extendida`
- diagnósticos técnicos y de soporte dentro de acordeones colapsados

Comportamiento visible para el usuario ante fallos:

- una entrada vacía devuelve un mensaje explícito pidiendo que se ingrese una pregunta
- evidencia insuficiente permanece como una respuesta tipada de baja confianza
- fallos de retrieval o generación aparecen como errores explícitos de la UI
  sin exponer texto crudo de excepciones de backend en las superficies públicas

## CLI de ingestión

El primer slice implementado de `Phase 2` es un job offline de ingestión solo
para administradores.

Comando canónico:

```bash
python -m rag.ingestion ingest-pdfs \
  --input-dir data/raw \
  --markdown-dir data/markdown \
  --processed-dir data/processed \
  --manifest-path data/processed/ingestion-manifest.jsonl \
  --glob "*.pdf" \
  --overwrite false \
  --fail-fast false
```

Flags requeridos:

- `--input-dir`
- `--markdown-dir`
- `--processed-dir`
- `--manifest-path`

Flags opcionales:

- `--glob` por defecto es `*.pdf`
- `--overwrite` por defecto es `false`
- `--fail-fast` por defecto es `false`
- `--metadata-overlay-path` permite metadata curada por operador asociada a un
  `source_pdf_id` estable

Nota sobre corpus incremental:

- `data/raw/` puede acumular PDFs previamente ingestados;
- con `--overwrite false`, la ingestión omite documentos cuyos artefactos
  determinísticos ya existen y procesa únicamente PDFs fuente nuevos;
- si un PDF existente se reemplaza in-place y debe reprocesarse, el rerun debe
  usar `--overwrite true`.

Límite actual del corpus MVP:

- la ingestión es intencionalmente solo para PDF;
- los formularios `.docx` están fuera de scope para el MVP, no se onboardean
  al corpus RAG y no se devuelven como evidencia de respuesta ni como artefactos
  de respuesta.

El comando sale con código distinto de cero cuando:

- Docling no es importable en el runtime local
- el directorio de entrada no existe
- no se encuentran archivos PDF coincidentes
- una conversión falla con `--fail-fast=true`

## Runtime batch local externo

En este repositorio, el runtime de la aplicación y el runtime local de
batch-ingestion son responsabilidades intencionalmente separadas.

Usa `.venv` para:

- `make app`
- `make test`
- desarrollo normal del repositorio

Usa un virtualenv local externo para:

- warm-up de assets de `Docling`
- ingestión de PDFs
- generación de embeddings
- indexación en Qdrant

El paso de indexación también es responsable de crear los payload indexes de
Qdrant requeridos por los filtros de metadata de retrieval actualmente
soportados cuando la superficie del cliente expone creación de payload indexes.

Para el procedimiento completo de operador que permite onboardear una nueva
categoría desde PDFs raw hasta validación de retrieval y respuesta fundamentada,
ver:

- `docs/category-onboarding-playbook.md`

Motivo:

- en la workstation actual, el `.venv` local del repositorio sigue siendo un
  mal ajuste para imports batch pesados como `torch`;
- un virtualenv limpio fuera del workspace sincronizado ya fue validado como
  la ruta práctica para Docling y embeddings.

El repositorio expone ahora targets batch mínimos a través de `Makefile`.
Son configurables y no requieren commitear rutas específicas de una máquina.

Variables importantes:

- `BATCH_VENV` ruta del virtualenv externo
- `BATCH_INPUT_DIR` árbol de PDFs raw, por defecto `data/raw`
- `BATCH_MARKDOWN_DIR` ruta local de salida markdown
- `BATCH_PROCESSED_DIR` ruta local de salida processed
- `BATCH_METADATA_OVERLAY_PATH` archivo de metadata overlay, por defecto
  `ops/document-metadata-overlays.json`
- `BATCH_SAMPLE_PDF` PDF de muestra usado para warm-up de Docling
- `BATCH_OVERWRITE` por defecto `false` para corridas batch locales incrementales

Ejemplo:

```bash
make batch-warmup \
  BATCH_VENV=/private/tmp/yini-fast-venv311

make batch-ingest \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_MARKDOWN_DIR=/tmp/yini-batch-check/markdown \
  BATCH_PROCESSED_DIR=/tmp/yini-batch-check/processed \
  BATCH_METADATA_OVERLAY_PATH=ops/document-metadata-overlays.json

make batch-embeddings \
  BATCH_VENV=/private/tmp/yini-fast-venv311 \
  BATCH_PROCESSED_DIR=/tmp/yini-batch-check/processed
```

Notas operativas:

- el flujo batch por defecto es incremental:
  - documentos previamente procesados se omiten durante la ingestión;
  - artefactos de embeddings previamente generados se omiten durante la generación;
  - define `BATCH_OVERWRITE=true` solo cuando intencionalmente quieras regenerar;
- mantén `BATCH_METADATA_OVERLAY_PATH` apuntando al archivo overlay previsto
  cuando deba aplicarse metadata curada `document_type` / `product` durante la ingestión;
- mantén `data/markdown/` y `data/processed/` solo en local salvo que exista
  una razón explícita de reproducibilidad para snapshotearlos en otro sitio;
- prefiere directorios temporales de salida para corridas locales de validación;
- el comportamiento de despliegue y runtime hosted sigue dependiendo de Qdrant,
  no de artefactos locales de ingestión commiteados.

## Línea base de metadata del corpus

El contrato actual de identidad y metadata del corpus es intencionalmente
estrecho y determinístico.

Campos actuales a nivel documento:

- `source_pdf_id` es la clave estable de identidad del corpus usada a través
  de metadata procesada, artefactos de chunks, artefactos de embeddings,
  manifests de indexación y payloads de retrieval
- `source_pdf_relative_path` preserva trazabilidad hacia el árbol anidado de
  fuentes raw bajo `data/raw`
- `document_name` es una etiqueta display orientada a retrieval:
  - usa como fallback el stem del PDF fuente;
  - se actualiza al primer heading Markdown cuando se extrae de forma segura
    durante la ingestión;
  - rechaza etiquetas obviamente ruidosas de media/embed con URLs y en esos
    casos vuelve al stem determinístico del PDF;
  - los registros persistidos siguen cayendo a `source_pdf_id` si no hay una
    etiqueta display disponible
- `document_version` es opcional:
  - permanece sin definir cuando no se detecta un token de versión de forma segura;
  - se puebla solo a partir de pattern matching conservador sobre texto temprano del documento

Responsabilidades actuales del repositorio:

- preservar naming determinístico de artefactos a partir de `source_pdf_id`
- preservar trazabilidad raw-to-processed mediante `source_pdf_relative_path`
- transportar `document_name` y el `document_version` opcional a través de los
  seams de chunks, embeddings, indexación, retrieval y citas

## Equivalencias de términos curadas por operador

El repositorio incluye ahora una única tabla mantenida por operadores en:

- `ops/term-equivalences.json`

Propósito:

- normalizar aliases comunes de consulta en español hacia términos canónicos de retrieval;
- anexar bundles estrechos, curados por operador y orientados a comparación
  cuando una regla curada hace match;
- normalizar aliases de filtros `document_type` y `product` hacia valores canónicos;
- mantener explícita y editable la reconciliación de términos a medida que el corpus crece.

Regla importante para el operador:

- mantén los valores canónicos de `ops/term-equivalences.json` alineados con
  los valores canónicos usados en cualquier archivo de metadata overlay, para
  que los filtros de retrieval sigan haciendo match con los payloads indexados
  de forma veraz.

Scope actual:

- la expansión de aliases de consulta es determinística y solo de retrieval;
- las reglas de expansión pueden anexar pequeños bundles de comparación curados por operador;
- los bundles de comparación que hagan match pueden disparar reranking
  determinístico y estrecho sobre un pool más grande de candidatos;
- el mapeo de aliases de filtros de metadata es determinístico y se limita a
  `document_type` y `product`;
- el repositorio no intenta inferencia automática de taxonomía.

Guía para operadores:

- usa reglas de expansión de consulta solo para misses repetidos de retrieval
  con vocabulario estable del operador;
- mantén los términos canónicos anexados alineados con labels reales de
  documentos, overlays u otros nombres orientados a retrieval ya presentes en el corpus;
- trata estas reglas como hints estrechos de retrieval, no como controles
  garantizados de ranking ni como gestión automática de taxonomía.

Limitaciones actuales:

- la superficie práctica de identidad del corpus sigue dependiendo
  principalmente de `source_pdf_id`
- la calidad de `document_name` depende de la calidad del nombre de archivo o
  de la presencia de un heading temprano en el Markdown extraído
- `document_version` es best-effort y puede seguir ausente en muchos documentos reales
- todavía no existen normalización rica de metadata ni clasificación automática
- los metadata overlays curados por operador ya existen como un seam opcional
  en tiempo de ingestión, pero siguen dependiendo de mantenimiento manual deliberado

## Estructura del repositorio

```text
app/        Entry point de la aplicación Gradio MVP
agents/     Agentes LangGraph y superficies de orquestación
contracts/  Contratos tipados compartidos entre ingestión, retrieval y respuestas
core/       Settings, logging y seams MCP
data/       Datos raw, markdown, processed y eval
docs/       Documentación durable de soporte
ops/        Módulos de guardrails y observabilidad
rag/        Pipeline de ingestión y retrieval
specs/      Constitución y especificaciones de implementación
tests/      Smoke tests y cobertura de regresión
```

## Próximos hitos

`Phase 0` hasta `Phase 19` están completas en:

- `/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/specs/roadmap.md`

El siguiente trabajo de implementación debe arrancar desde un nuevo spec
bundle fechado si se aprueba scope adicional, probablemente alrededor de:

- expansión del scope de producto más allá del límite actual del demo
- nuevas decisiones de arquitectura o despliegue
- hardening operativo post-demo
