# Requirements

## Title

Recover the hosted manual MVP queries for bicicletas/patinetas deductible and choque simple procedure.

## Context

The hosted manual Hugging Face Spaces QA pass on 2026-06-20 exposed two regressions against the committed MVP acceptance surface:

- `¿Cuál es el deducible del seguro de bicicletas y patinetas?` drifted away from the intended `pv bicis y patinetas v2.pdf` guide family and surfaced unrelated movilidad families.
- `¿Cuál es el procedimiento de atención del choque simple?` over-relied on the photo guide path and failed to anchor on the procedural guide family.

The repository-level retrieval tests already demonstrate that these behaviors can pass when local chunk artifacts are available for hybrid recall. The hosted Space does not rely on versioned `data/processed/chunks` artifacts, so the public UI path needs stronger deterministic routing through the existing operator-curated query-filter seam.

## Scope

This slice should:

1. Add one deterministic `document_name` routing rule for explicit bicicletas/patinetas deductible intent.
2. Add one deterministic `document_name` routing rule for explicit choque simple procedure intent.
3. Add focused repository-loaded regression coverage for both hosted-style queries without caller-supplied filters.
4. Update roadmap and acceptance-matrix traceability to record the hosted manual regression and the corrective slice.

This slice should not:

- redesign chunking for bicicletas/patinetas or choque simple;
- require versioning local chunk artifacts into the repository;
- broaden to generic movilidad deductible or generic movilidad procedure questions;
- change already-passing photo-intent or bicicletas/patinetas coverage routing.

## Required Behavior

### 1. Bicicletas/patinetas deductible routing

Acceptance criteria:

- a query that explicitly asks `¿Cuál es el deducible del seguro de bicicletas y patinetas?` normalizes to `product=movilidad`, `document_type=guide`, and `document_name = pv bicis y patinetas v2`;
- the existing bicicletas/patinetas coverage rule remains unchanged;
- unrelated movilidad deductible queries do not receive this document-family filter.

### 2. Choque simple procedure routing

Acceptance criteria:

- a query that explicitly asks for the choque simple handling procedure normalizes to `product=movilidad`, `document_type=guide`, and `document_name = EN EVENTOS DE CHOQUES`;
- the existing photo/video choque simple rule remains unchanged;
- broad choque simple photo queries continue to resolve to `¿Cómo tomar fotos y videos?`.

### 3. Hosted manual acceptance alignment

Acceptance criteria:

- focused tests cover repository-loaded term-equivalence normalization for both queries without caller filters;
- the documented acceptance-matrix/manual-checklist interpretation can again expect those two hosted questions to stay inside their intended families after redeploy;
- no unrelated accepted MVP family changes are required.
