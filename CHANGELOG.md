# Changelog

## 2026-06-13

- Add a durable category-onboarding playbook that captures the operator workflow for new corpus categories from raw folder taxonomy through ingestion, embeddings, Qdrant indexing, retrieval validation, grounded-answer validation, and narrow corrective-slice escalation based on the implemented `AUTOS` and `BICICLETAS Y PATINETAS` experience.
- Add the `MOVILIDAD/BICICLETAS Y PATINETAS` baseline corpus slice by onboarding the category into ingestion, embeddings, indexing, product/document-type alias normalization, and real retrieval validation under the existing `movilidad` taxonomy.
- Add the follow-on `BICICLETAS Y PATINETAS` corrective retrieval slices by aligning supported-scope admission for bike and scooter queries, normalizing the diagrammatic `pv` corpus into semantic `COBERTURAS Y PLANES`, `GENERALIDADES`, `EXPEDICIÓN REQUISITOS`, and `DEDUCIBLE` chunks, and improving deductible-specific recall/reranking so real grounded answers now cite explicit deductible evidence.
- Add the first AUTOS comparison corrective retrieval slice by introducing narrow operator-curated comparison query expansion terms, focused comparison-intent regression coverage, and roadmap/spec traceability for comparison-oriented AUTOS retrieval misses.
- Add the next AUTOS comparison corrective retrieval slice by expanding the Qdrant candidate pool for matched comparison intents and applying deterministic lexical reranking so comparative evidence can outrank FAQ-heavy semantic hits when both are present.
- Add the next AUTOS comparison corrective ingestion slices by prefixing governing section context into follow-on chunks, greedily aggregating short same-section comparison fragments, and normalizing markdown comparison tables into plan-oriented semantic statements before chunking.
- Add the next AUTOS comparison corrective retrieval slice by introducing deterministic hybrid comparison recall from local chunk artifacts, fusing lexical candidates with semantic Qdrant results under the existing comparison-intent gate, and correcting the hybrid scorer so anchor restatements do not over-favor Plan Básico FAQ evidence.
- Add the next AUTOS metadata corrective slices by inferring missing `product` and `document_type` values from `source_pdf_relative_path` with overlay precedence, persisting those canonical values into processed and chunk artifacts, and extending the curated `guide` aliases so the real `diferenciales planes autos.pdf` corpus now lands in runtime retrieval with `product=auto` and `document_type=guide`.

## 2026-06-12

- Add committed AUTOS document metadata overlays so the current MOVILIDAD/AUTOS corpus keeps stable `document_type` and `product=auto` classification across future local ingestions and deployments.
- Add the next `Phase 16` ingestion-runtime corrective slice by allowing the `docling` backend path to fall back to PDFium only when a per-document Docling conversion exceeds the configured timeout, adding focused regression coverage for timeout fallback and non-timeout failure behavior, and unblocking the remaining AUTOS `diferenciales` PDF without demoting Docling as the primary local converter.
- Add the next `Phase 15` corrective supported-scope slice by aligning deterministic scope admission with ARL/RUI document questions already supported by retrieval, expanding the narrow token set in `core/query_scope.py`, adding focused classifier and UI-query regression coverage, and closing the dated spec bundle plus roadmap traceability for the hosted ARL refusal gap.
- Add the corrective `Phase 18` operator-curated term-equivalence normalization slice by introducing a committed `ops/term-equivalences.json` table for deterministic Spanish query and metadata-filter alias normalization, wiring retrieval-time query/filter canonicalization without changing the backend contract, documenting incremental `data/raw/` accumulation and canonical-value alignment with metadata overlays, and correcting the batch operator flow so ingestion and embeddings default to `overwrite=false` for new-file-only processing.
- Add the next `Phase 18` corrective metadata slice by introducing operator-curated document metadata overlays for `document_type` and `product`, wiring the batch ingestion flow to pass the overlay file explicitly, and documenting that local `batch-index` also creates the Qdrant payload indexes required for the current metadata-filter surface when the client supports payload-index creation.
- Add the next `Phase 18` corrective retrieval-traceability slice by aligning Qdrant collection bootstrap with retrieval-facing `document_type` and `product` filters, adding compatibility coverage for clients without payload-index helpers, and guarding retrieval-facing `document_name` promotion so noisy media/embed headings with URLs fall back to the deterministic PDF stem instead of becoming citation labels.
- Add the corrective `Phase 17` external batch-runtime operator-flow slice by formalizing a configurable `Makefile` surface for external-venv `Docling` warm-up, ingestion, embeddings, and indexing runs, documenting the operator workflow in the README, validating it against temporary local outputs, and keeping heavy local ingestion artifacts out of the commit surface by ignoring generated `data/markdown/` and `data/processed/` contents.
- Add the corrective `Phase 15` local-embedding-runtime remediation by evidencing the repo-local `.venv` import bottleneck, documenting the validated clean-venv workaround that restores practical local embeddings generation, and closing the dated spec bundle plus roadmap traceability after successful embeddings generation and Qdrant indexing on the current four-document corpus.
- Add the corrective `Phase 15` Spanish autos scope-alignment remediation by narrowing supported query-scope vocabulary for benign autos-assistance requests, adding focused regression coverage for the Spanish autos query path, and validating that the real `answer-query` flow now returns a grounded cited answer instead of a false unsupported-scope refusal.
- Refresh focused smoke coverage so the hosted smoke path asserts the current `documentary_basis` contract alongside the existing supported-answer shape without crashing.

## 2026-06-11

- Add the corrective `Phase 15` architecture/repo-surface sync slice by updating `docs/architecture.md` to reflect the roadmap-complete posture through `Phase 19`, replacing stale future-only labels for implemented `agents/`, `mcp/`, `rag/`, and `tests/` surfaces in the top-level repo tree, and closing the dated spec bundle plus roadmap traceability for that documentation-only remediation.
- Add the corrective `Phase 15` README sync slice by extending the top-level status summary and `Current Status` through completed `Phase 19`, updating `Next Milestones` to reflect the roadmap-complete posture instead of stopping at `Phase 15`, and closing the dated spec bundle plus roadmap traceability for that documentation-only remediation.
- Add the fifth `Phase 19` citation-readability slice by surfacing a compact operator-facing evidence summary in the Gradio debug metadata, deduplicating current evidence document names plus curated `document_type` and `product` values, adding focused empty/non-empty UI regression coverage, and closing `Phase 19` in the roadmap and spec bundle.
- Add the fourth `Phase 19` citation-readability slice by propagating curated `document_type` and `product` metadata into citation and documentary-basis response contracts, rendering those fields in the Gradio `Citas` and `Base documental` surfaces with stable Spanish labels, adding focused contract, grounded-answer, and UI regression coverage, and marking the slice complete in the roadmap and spec bundle.

## 2026-06-10

- Add the third `Phase 19` citation-readability slice by introducing a dedicated `Base documental` UI surface, rendering stable `documentary_basis` review fields including optional relative-path traceability, updating the Gradio output shape and focused UI regression coverage, and marking the slice complete in the roadmap and spec bundle.

## 2026-06-09

- Add the second `Phase 19` citation-readability slice by exposing `source_pdf_relative_path` in the Gradio citation renderer with a stable Spanish label, preserving clean fallback behavior when the field is absent, adding focused UI rendering regression coverage, and marking the slice complete in the roadmap and spec bundle.
- Add the first `Phase 19` citation-readability slice by propagating `source_pdf_relative_path` through citation and documentary-basis response contracts, reusing existing retrieval metadata for operator traceability, adding focused grounded-answer and contract regression coverage, and marking the new phase and slice complete in the roadmap and spec bundle.
- Add the fifth `Phase 18` corpus-metadata slice by re-enabling truthful retrieval filtering for curated `document_type` and `product` metadata, mapping both fields into Qdrant query filters, adding focused regression coverage for combined supported filters, and closing the phase in the roadmap and spec bundle.
- Add the fourth `Phase 18` corpus-metadata slice by introducing optional
  operator-curated metadata overlays keyed by stable `source_pdf_id`,
  propagating curated `document_type` and `product` values through ingestion,
  chunking, embedding, indexing, and retrieval seams without breaking
  documents that have no overlay entry.
- Add the third `Phase 18` corpus-metadata slice by guarding unsupported
  `document_type` and `product` retrieval filters explicitly, preserving only
  the metadata filters backed by the current indexed payload contract and
  avoiding silent empty-result behavior for unsupported corpus fields.
- Add the second `Phase 18` corpus-metadata slice by propagating
  `source_pdf_relative_path` through embedding payloads, persisted Qdrant
  payloads, and retrieved chunk mapping, preserving compatibility with older
  payloads that do not yet carry the field.
- Add the first `Phase 18` corpus-metadata slice by documenting the current
  baseline contract for `source_pdf_id`, `source_pdf_relative_path`,
  retrieval-facing `document_name`, and optional `document_version`, while
  correcting the stale README metadata note to match the actual ingestion
  behavior without changing runtime logic.
- Add the fourth `Phase 17` runtime-compatibility slice by synchronizing the
  top-level `README.md` phase-status summary with the already completed
  `Phase 16` ingestion-runtime remediation and `Phase 17` runtime-compatibility
  hardening work, keeping the change narrowly scoped to documentation
  traceability.
- Add the third `Phase 17` runtime-compatibility slice by remediating the
  hosted latency smoke so budget assertions are deterministic in tests via
  injected timing/evaluation seams, preserving the callable default smoke
  payload while removing machine-dependent wall-clock flakiness from
  `tests/test_smoke.py`.
- Add the second `Phase 17` runtime-compatibility slice by aligning the typed
  `Groq` default runtime model to `openai/gpt-oss-120b`, extending hosted
  operator startup-contract notes to include `GROQ_MODEL`, adding focused
  smoke/config regression coverage, and recording the remaining unrelated
  hosted-latency smoke failure as out-of-slice evidence.
- Add the first `Phase 17` runtime-compatibility slice by standardizing the
  tracked Groq model identifier to `openai/gpt-oss-120b`, synchronizing
  `.env.example`, `PRD.md`, and observability test fixtures with the validated
  runtime value, and recording end-to-end `answer-query` evidence for the
  hosted Spanish RAG path.

## 2026-06-08

- Add the remaining `Phase 16` Qdrant remediation work by normalizing
  physical Qdrant point ids to deterministic UUIDs while preserving logical
  `chunk_id` values in payloads, adapting retrieval to the installed
  `qdrant-client` surface via `query_points()`, synchronizing `.env.example`
  with the multilingual embedding default, and temporarily ignoring
  `data/raw/**` during local batch-ingestion tuning.
- Add the final `Phase 16` ingestion-remediation slice by supporting
  recursive PDF discovery under nested raw source folders, deriving
  collision-safe document ids from relative source paths, recording relative
  path traceability in processed/chunk contracts, and validating a real
  Docling-first ingestion run against a nested sample tree without flattening
  or renaming source PDFs.
- Add the first `Phase 16` ingestion-remediation work by documenting the
  Docling startup block, then making local PDF ingestion explicitly
  Docling-first with configurable startup timeout, an asset warm-up command,
  and a controlled PDFium fallback path verified by targeted ingestion tests
  and a real local Docling warm-up/sample run.
- Add the final `Phase 15` closure slice by synchronizing the top-level
  `README.md` and `specs/roadmap.md`, marking `Phase 15` complete, removing
  stale milestone text that still implied `Phase 15` was pending, and adding a
  dated traceability bundle for the final README/roadmap status sync.
- Add the next `Phase 15` Spanish-alignment slice by hardening the Spanish
  demo UI state derivation so support/degraded outcomes no longer depend on
  brittle English backend substrings, while adding regression coverage for
  Spanish limited-evidence wording and marking the new slice complete in the
  roadmap.
- Add the fourth `Phase 15` Spanish-alignment slice by translating the curated
  30-question evaluation fixture set and the linked query-classification
  optimization subset to Spanish, preserving ids and expectation alignment
  while updating local-evaluation, optimization, and hosted-like smoke tests
  to the new Spanish-facing dataset versions.
- Add the third `Phase 15` Spanish-alignment slice by extending deterministic
  supported-scope matching and prompt-injection detection to common Spanish
  insurance and override/reveal phrasing, while preserving the current typed
  refusal contracts, event surfaces, and baseline query-classification path.
- Add the second `Phase 15` Spanish-alignment slice by switching the default
  embedding model from the English-only `BAAI/bge-small-en-v1.5` to the
  multilingual `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`,
  preserving the existing `sentence-transformers` provider seam while updating
  embedding-generation and Qdrant-indexing expectations plus the roadmap
  status for the completed retrieval-alignment slice.

## 2026-06-07

- Add the first `Phase 15` Spanish-alignment slice by localizing the public
  Gradio demo UI into Spanish, translating user-visible status/support/debug
  surfaces in the UI layer without changing retrieval behavior, and updating
  the roadmap to document both the completed `Phase 4` accounting gap and the
  new `Phase 15` Spanish-localization slice state.
- Finish the remaining `Phase 14` closure work by recording the deployed
  Hugging Face Space git SHA in the hosted deployment evidence slice, adding a
  dated `readme-phase-status-sync` bundle, and updating the README `Next
  Milestones` section so it points to `Phase 15` instead of stale `Phase 8`
  work.
- Close the remaining `Phase 14` documentation follow-ups by adding the dated
  traceability remediation bundle for the Spaces entrypoint-normalization claim
  and synchronizing the top-level `README.md` phase-status summary so the repo
  status now matches the roadmap-complete state for `Phase 14`.
- Advance the corrective `Phase 14` hosted deployment-evidence slice by
  recording real Hugging Face Spaces startup, readiness, and public
  accessibility evidence, and update the roadmap to reflect that hosted
  deployment validation is now complete while the remaining traceability and
  README-status follow-ups stay open.

## 2026-05-27

- Add the final documented `Phase 14` hosted-smoke expectations slice in
  `README.md`, then reopen `Phase 14` truthfully by recording the remaining
  hosted deployment-evidence, traceability, and README-status gaps surfaced by
  the audit, including a blocked evidence bundle for real Hugging Face Spaces
  deployment validation.
- Add the next `Phase 14` deployment slice with dedicated hosted-deployment
  rollback notes in `README.md`, explicitly documenting the current Spaces
  rollback posture, the minimum operator procedure for restoring a known-good
  repo state, and the required runtime variables that must remain configured
  after rollback, without mixing in hosted smoke expectations.
- Add the next `Phase 14` deployment slice with a dedicated hosted-demo
  supported-scope constraints section in `README.md`, explicitly documenting
  the current supported insurance-document posture, unsupported-scope refusal
  behavior, and the user-visible demo surfaces where unsupported requests are
  surfaced, without mixing in guardrail/refusal or rollback notes.
- Add the next `Phase 14` deployment slice with a dedicated hosted-demo
  guardrail/refusal constraints section in `README.md`, explicitly documenting
  the current prompt-injection refusal posture, conservative citation and
  confidence downgrade behavior, and the user-visible demo surfaces where
  those guarded outcomes appear, without mixing in supported-scope or rollback
  notes.
- Add the next `Phase 14` deployment slice with a dedicated hosted-demo
  runtime/dependency constraints section in `README.md`, explicitly documenting
  the current Hugging Face Spaces Docker posture, required startup variables,
  and evidenced container/runtime constraints without mixing in guardrail or
  rollback notes.
- Add the next `Phase 14` deployment slice with a concise Hugging Face Spaces
  deployment procedure in `README.md`, aligned to the configured `sdk: docker`
  runtime, the authoritative root `Dockerfile`, and the minimum startup
  variables required by the current app contract.
- Add the next `Phase 14` deployment slice that removes the stale
  `deploy/start.sh`, leaving the validated root `Dockerfile` and its direct
  `python -m app.ui` launch path as the only remaining Hugging Face Spaces
  startup surface before any entrypoint normalization work.

## 2026-05-26

- Add the next `Phase 14` deployment slice that removes the stale
  `deploy/Dockerfile`, leaving the validated root `Dockerfile` as the single
  authoritative Hugging Face Spaces Docker launch artifact for the configured
  `sdk: docker` runtime before any start-command normalization work.
- Add the next `Phase 14` deployment slice with a minimal Hugging Face Spaces
  runtime configuration in the root `README.md`, explicitly targeting the
  Docker SDK and `app_port: 7860` to match the current containerized Gradio
  app path before any launch-artifact or hosted-smoke work.
- Add the next `Phase 14` deployment slice with one successful local container
  readiness validation against the running app surface, explicit capture of the
  startup and readiness probe commands, and confirmation that the containerized
  Gradio surface responds with `HTTP 200` before any hosted deployment work.

## 2026-05-25

- Add the next `Phase 14` deployment slice with one successful local container
  startup from the validated image, explicit capture of the startup command and
  required runtime env surface, and confirmation that the current app
  entrypoint can launch without immediate failure before readiness probing.
- Add the next `Phase 14` deployment slice with one successful local Docker
  image build for the current runtime skeleton, explicit capture of the build
  command, and validation that dependency installation and app packaging
  complete from current repo state without drifting into container startup or
  readiness checks.
- Add the first `Phase 14` deployment slice with a root Docker runtime
  skeleton, explicit dependency installation from `pyproject.toml`, explicit
  Gradio bind/port runtime wiring, and the current app entrypoint without
  drifting into container smoke validation or hosted deployment work.

## 2026-05-22

- Add the corrective `Phase 13` demo-hardening slice that sanitizes explicit
  public trace summaries, preserves safe concise trace labels, redacts unsafe
  internal trace items, and falls back to the derived review-oriented trace
  when explicit trace data is not safe to show.
- Add the final `Phase 13` demo-hardening slice with a narrow `Answer Quality`
  surface, explicit degraded messaging for lower-confidence and limited-evidence
  drafts, and local validation that closes the remaining demo UI hardening work.

## 2026-05-21

- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  readiness surface, explicit degraded messaging for runtime/dependency
  readiness failures, and local validation without drifting into
  answer-quality degradation work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  error-state surface, explicit distinction between input-validation and
  runtime-processing failures, and local validation without drifting into
  degraded-service messaging work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  loading-state surface, explicit in-flight and ready feedback through the
  current Gradio UI handler, and local validation without drifting into
  error-state redesign or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow operator-facing
  debug-metadata surface, compact request/runtime/retrieval metadata tied to
  the current UI seams, and local validation without drifting into
  loading/error-state or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  support-context surface, concise request-follow-up guidance tied to the
  current request-correlation seams, and local validation without drifting
  into broader debug-metadata or degraded-service work.
- Add the next `Phase 13` demo-hardening slice with a narrow user-visible
  trace-summary surface, concise review-oriented trace rendering across
  success/refusal UI paths, and local validation without drifting into broader
  debug-context or degraded-service messaging work.
- Add the first `Phase 13` demo-hardening slice with a grouped Gradio `Blocks`
  layout, clearer review-oriented output organization for answer/citations/
  confidence/limitations/status, and local validation without drifting into
  trace-summary or degraded-service messaging work.
- Add the corrective `Phase 12` MCP slice that closes the remaining
  compatibility-boundary gap by making request-field and MCP-visible
  tool-metadata compatibility expectations explicit, aligning the implemented
  MCP seam with the final phase requirements.
- Add the final `Phase 12` MCP slice with explicit tool-compatibility
  boundaries for the current MCP-visible surface, operational forward/backward
  compatibility expectations aligned to the interface version policy, and local
  validation that closes the remaining MCP integration work.
- Add the next `Phase 12` MCP slice with an explicit interface version policy,
  date-based version naming, operational bump rules for additive and breaking
  MCP-surface changes, and local validation without drifting into detailed
  compatibility-boundary work.
- Add the next `Phase 12` MCP slice with a narrow local client seam, end-to-end
  initialize/list/call roundtrip over the current registered MCP tool surface,
  and local validation without drifting into interface versioning work.
- Add the next `Phase 12` MCP slice with initial server-side tool
  registration and exposure for `document_retrieval` and `clause_extraction`,
  explicit MCP-visible tool metadata, and local validation without drifting
  into MCP client integration.
- Add the first `Phase 12` MCP slice with a minimal server seam, explicit
  typed transport request/response contracts, initialize/ping-only handling,
  and local validation without drifting into tool execution wiring.

## 2026-05-20

- Add the corrective `Phase 11` optimization slice that remediates
  query-classification measurable-improvement semantics by making the current
  optimization-subset evaluation surface explicit, reporting when improvement
  is not actually validated, and removing overstated optimization claims from
  the roadmap.
- Add the final corrective `Phase 11` optimization slice with hosted-like
  query-classification latency-budget validation over the product-facing
  classification path, explicit distinction from the local comparison seam, and
  local validation that truthfully closes the remaining `Phase 11` gap.
- Add the final `Phase 11` optimization slice with typed
  query-classification latency-budget validation, explicit within-budget /
  over-budget reporting over the current optimized predictor and latency
  comparison seam, and local validation that closes the remaining `Phase 11`
  work.
- Add the next `Phase 11` optimization slice with a typed
  query-classification quality-improvement validation seam, explicit improved /
  flat / regressed reporting over the current optimized predictor and baseline,
  and local validation without drifting into latency-budget validation.
- Add the next `Phase 11` optimization slice with a real optimized
  query-classification callable, subset-backed predictor wiring, compatibility
  with the existing quality/latency/cost comparison seams, and local
  validation without yet claiming measurable improvement.
- Add the final `Phase 11` optimization slice with a measurable
  query-classification cost-comparison seam, typed baseline-versus-optimized
  external-call and estimated-cost reporting over the current optimization
  subset, and local validation that closes the remaining `Phase 11` work.
- Add the next `Phase 11` optimization slice with a measurable
  query-classification latency-comparison seam, typed baseline-versus-optimized
  latency reporting over the current optimization subset, and local validation
  without drifting into cost comparison work.
- Add the next `Phase 11` optimization slice with a measurable
  query-classification quality-comparison seam, typed overall and per-category
  reporting, deterministic baseline-versus-optimized evaluation over the
  current optimization subset, and local validation without drifting into
  latency or cost comparison work.
- Add the next `Phase 11` optimization slice with a narrow query-classification
  optimization dataset subset, typed optimization-example contracts, explicit
  linkage to the 30-question evaluation and golden-behavior assets, and local
  validation without drifting into before/after comparison work.
- Add the next `Phase 11` optimization slice with a minimal DSPy
  query-classification module skeleton, explicit typed optimization I/O
  contracts, lazy DSPy runtime loading, and local validation without drifting
  into optimization dataset or before/after comparison work.
- Add the first `Phase 11` optimization slice by selecting `query
  classification` as the initial DSPy target, defining explicit baseline
  quality, latency, and zero-external-call cost surfaces, and documenting the
  decision without drifting into module implementation.
- Add the next `Phase 10` evaluation slice with a hosted-like latency smoke
  over the local evaluation runner, a deterministic latency assertion surface,
  and local validation without drifting into citation regression smoke work.
- Add the next `Phase 10` evaluation slice with hosted-like startup and
  health/readiness smoke coverage over the current app/runtime seams, keeping
  the checks deterministic and scoped away from latency and citation
  regressions.

## 2026-05-19

- Add the next `Phase 10` evaluation slice with a deterministic local
  evaluation runner over the curated assets, typed run-level and per-question
  outputs, stable `question_id` linkage, and local validation without drifting
  into hosted regression smoke work.
- Add the next `Phase 10` evaluation slice with typed local evaluation
  run-result contracts, deterministic per-question result linkage, and schema
  validation for run-level and per-question outputs without drifting into
  runner execution.
- Add the next `Phase 10` evaluation slice with a typed citation-expectation
  dataset for the curated 30-question set, deterministic question linkage,
  explicit distinction between grounded, no-citation, and guardrail citation
  cases, and local alignment validation without drifting into runner work.
- Add the next `Phase 10` evaluation slice with a typed retrieval-expectation
  dataset for the curated 30-question set, deterministic question linkage,
  explicit distinction between grounded, no-retrieval, and guardrail retrieval
  cases, and local alignment validation without drifting into citation
  expectations or runner work.
- Add the next `Phase 10` evaluation slice with a typed golden behavior
  dataset for the 30-question curated set, deterministic question-to-outcome
  linkage, explicit refusal and guardrail expectations, and local alignment
  validation without drifting into retrieval/citation evidence annotations or
  runner work.
- Add the next `Phase 10` evaluation slice by completing the curated local
  question set to the 30-question roadmap target, preserving stable ids,
  balanced category coverage, and deterministic schema validation without
  drifting into golden outputs or runner work.
- Add the next `Phase 10` evaluation slice by expanding the local curated
  question set from the initial seed to a broader balanced dataset with stable
  ids, explicit expected-behavior metadata, and schema validation coverage
  across normal QA and current guardrail categories.
- Add the first `Phase 10` evaluation slice with typed evaluation-question
  schemas, a versioned local curated question set covering normal QA and
  guardrail-oriented prompts, and deterministic dataset validation coverage.
- Add the final `Phase 9` guardrail slice with a narrow local summary surface
  for guardrail/refusal events, typed event records, distinguishable guardrail
  classes, and preserved request-correlation context without drifting into
  broader analytics work.
- Add the next `Phase 9` guardrail slice with deterministic abuse-case
  regression scenarios over implemented guardrails, explicit assertions of the
  expected refusal or downgrade outcomes, and benign supported control coverage
  without drifting into telemetry-summary work.
- Add the next `Phase 9` guardrail slice with deterministic prompt-injection
  signal detection, conservative typed refusal behavior at the workflow and UI
  boundary, and correlated guardrail observability without drifting into
  abuse-case-suite work.
- Add the next `Phase 9` guardrail slice with explicit confidence-consistency
  enforcement, conservative typed downgrade behavior for overstated confidence,
  and correlated guardrail observability without drifting into prompt-injection
  or abuse-case work.
- Add the next `Phase 9` guardrail slice with mandatory citation presence for
  answerable responses, conservative typed downgrade behavior when citations
  are missing, and correlated guardrail observability without drifting into
  broader confidence-policy work.
- Add the first `Phase 9` guardrail slice with deterministic unsupported-query
  scope classification, conservative typed refusal outcomes at the workflow and
  UI boundary, and correlated refusal observability without drifting into
  prompt-injection or citation-confidence policy work.
- Close the remaining `Phase 8` validation gap with an end-to-end
  unsupported-route workflow test, confirming conservative non-error behavior
  for out-of-scope queries and fully closing the documented planner slice
  verification.
- Add the next `Phase 8` workflow slice with explicit insufficient-evidence
  fallback edges after comparison and citation verification, conservative
  typed fallback outcomes, fallback traceability in shared state, and
  observability for fallback selection events.
- Add the next `Phase 7` tooling slice with an independently callable
  `citation_verifier_tool`, conservative verification over drafted output and
  cited evidence only, explicit weak/unsupported non-error outcomes, and typed
  success/failure observability coverage.
- Add the final `Phase 7` tooling slice with an independently callable
  `response_draft_tool`, typed advisor-facing draft output from upstream
  evidence only, explicit insufficient-information handling, and preserved
  observability for reusable drafting.
- Add the first `Phase 8` workflow slice with LangGraph wiring, shared workflow
  state, one linear end-to-end tool path, typed workflow success/failure
  output, and observable state transition tracing.
- Add the next `Phase 8` workflow slice with a typed planner step, explicit
  route selection over existing workflow paths, conservative unsupported-route
  handling, and observable planner decision events.
- Add the next `Phase 8` workflow slice with explicit analyst, verifier, and
  drafter stages, clearer stage outputs in shared workflow state, and tighter
  graph-stage boundaries over the existing tool seams.

## 2026-05-18

- Implement the `docling-ingestion-skeleton` Phase 2 slice with an admin-only
  CLI entrypoint, deterministic output paths, append-only manifest logging, and
  typed processed-document contracts.
- Add Docling as a project dependency and rebuild the repo’s local `.venv` on
  Python `3.11` to align the actual environment with the documented tech stack.
- Update `README.md` to reflect completed `Phase 0`, completed `Phase 1`, and
  the first implemented `Phase 2` ingestion slice.
- Tighten spec alignment with explicit CLI usage docs and added tests for
  append-only manifest reruns and invalid ingestion status values.
- Add the `markdown-cleaning-and-metadata-extraction` Phase 2 slice with
  conservative Markdown cleaning, deterministic cleaned artifacts, minimal
  metadata extraction, and failure handling for post-conversion processing.
- Add the first `Phase 3` slice for deterministic chunk contracts and local
  chunk persistence, including explicit chunk configuration, stable chunk ids,
  propagated traceability metadata, and persisted per-document chunk bundles.
- Add the `semantic-boundary-aware-chunk-refinement` Phase 3 slice with
  heading-aware and clause-safe chunk boundaries, explicit `v2` chunk schema
  versioning, richer `section_path` metadata, and failure-path validation for
  refined chunk generation.
- Add the first `Phase 4` slice for local embedding generation, including
  typed embedding artifacts, config-driven `sentence-transformers` usage,
  canonical local persistence under `data/processed/embeddings`, and explicit
  failed-manifest behavior for malformed chunk artifacts.
- Add the second `Phase 4` slice for Qdrant indexing, including collection
  bootstrap and compatibility checks, deterministic point mapping from local
  embedding artifacts, idempotent upserts, retry/backoff behavior, and explicit
  indexing manifest coverage for permanent failures and multi-artifact
  continuation.
- Add the first `Phase 5` slice for retrieval, including query embedding reuse,
  Qdrant search, typed `RetrievedChunk` mapping, preserved traceability
  metadata from indexed payloads, explicit empty-result behavior, and retrieval
  failure coverage for malformed payloads.
- Add the second `Phase 5` slice for grounded answer generation, including
  deterministic prompt construction from retrieved evidence, Groq-backed draft
  answers, citation mapping with stable `chunk_id` traceability, and explicit
  low-confidence handling for empty or weak retrieval evidence.
- Add the remaining `Phase 5` MVP UI slice with a thin Gradio app over the
  grounded QA backend, explicit user-visible insufficiency and runtime error
  states, startup/request smoke coverage, and local usage documentation.
- Add the first `Phase 6` observability slice with startup diagnostics,
  request correlation ids, structured retrieval and grounded-answer execution
  events, correlated CLI/UI failure logging, and validation that execution
  events do not leak secrets.
- Add the remaining `Phase 6` observability slice with health/readiness checks,
  optional Phoenix activation, explicit Phoenix failure policy, startup smoke
  visibility for hosted app readiness, and correlated latency traces for the
  grounded QA path.
- Add the first `Phase 7` tooling slice with an independently callable
  `document_retrieval_tool`, typed tool failure contracts, empty-result
  success handling, preserved request correlation, and explicit tool failure
  observability coverage.
- Add the next `Phase 7` tooling slice with an independently callable
  `clause_extraction_tool`, conservative typed clause categorization over
  retrieved evidence only, traceable supporting chunk ids, and explicit
  success/failure observability coverage.
- Add the next `Phase 7` tooling slice with an independently callable
  `policy_comparison_tool`, conservative structured comparison points over
  typed evidence only, explicit insufficient-information handling, and typed
  success/failure observability coverage.

## 2026-05-17

- `chore: phase 0 foundation scaffold`
- `docs: add settings env validation spec`
- `docs: align roadmap with deployment posture`
- `feat: implement settings env validation`
- `docs: add changelog maintenance skill`
- `merge: settings-env-validation into main`
- Add the `shared-contracts-foundation` Phase 1 spec slice for retrieval, response, tool, and workflow-state contracts.
- Add typed shared contract models for documents, tools, responses, and agent state aligned with the PRD vocabulary.
- Expand contract validation coverage for typed filters, clause categories, comparisons, citations, wrapper results, and workflow state construction.
- Add deployment mode flags to the typed settings contract to close the last identified Phase 1 gap.
- Add the `deployment-mode-flags` spec slice and document allowed `APP_ENV` behavior for public MVP demo vs internal production.
- Add the `docling-ingestion-skeleton` Phase 2 kickoff spec with a CLI-first ingestion contract, deterministic storage rules, rerun policy, and processed-document contract expectations.
- Tighten roadmap and existing specs with credential activation timing, contract stability expectations, and a clearer MVP boundary.
