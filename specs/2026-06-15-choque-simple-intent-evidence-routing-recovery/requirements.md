# Requirements

## Title

Recover intent-specific evidence routing for `choque simple` smokes.

## Context

The MVP acceptance row for `MOVILIDAD/TRANSVERSALES / choque simple` remains pending. Live validation shows two distinct but related gaps:

1. The photo-taking smoke query `¿Cómo debo tomar fotos en un choque simple?` ranks Ley 2251 / circular evidence above the dedicated guide `como tomar fotos choque simple v2.pdf`.
2. The grounded-answer smoke query `¿Cuál es el procedimiento de atención del choque simple?` mixes the photo guide into its primary evidence instead of prioritizing the operational procedure family (`proceso atencion choque simple v2.pdf`) and the ministerial circular.

## Scope

This slice should:

1. Add one deterministic document-family routing rule for explicit photo-taking intent.
2. Add one procedure-intent expansion rule so retrieval can recall the operational procedure family.
3. Prioritize `proceso atencion` / `circular choque simple` evidence for procedure-intent citation and retrieval ranking.
4. Update roadmap and the acceptance matrix after live validation.

This slice should not:

- re-ingest or re-chunk choque simple documents;
- change unrelated movilidad retrieval behavior;
- broaden into generic legal-normativity routing outside the choque simple intent pair.

## Required Behavior

### 1. Photo-intent routing

Acceptance criteria:

- `¿Cómo debo tomar fotos en un choque simple?` normalizes to the dedicated photo guide family `¿Cómo tomar fotos y videos?`;
- live retrieval for that query ranks `como tomar fotos choque simple v2.pdf` first.

### 2. Procedure-intent prioritization

Acceptance criteria:

- procedure-intent queries append operational recall terms such as `EN EVENTOS DE CHOQUES`, `Para recordar`, `INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE`, `retirar los vehículos`, and `centros de conciliación`;
- retrieval/answering for `¿Cuál es el procedimiento de atención del choque simple?` prioritizes `proceso atencion choque simple v2.pdf` and/or `circular choque simple.pdf` over the photo guide.

### 3. Regression safety

Acceptance criteria:

- focused tests cover the photo-family normalization rule;
- focused tests cover procedure-intent prioritization;
- existing choque simple retrieval tests still pass.
