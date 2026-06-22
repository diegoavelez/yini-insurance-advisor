# Requirements

## Title

Improve the hosted Spaces review layout by moving `Citas clave` into a compact accordion and strengthening wide-table usability without shrinking the font.

## Context

After the hosted MVP validation pass, the public Gradio UI still had two narrow usability issues:

- `Citas clave` remained visually heavy in the primary answer surface, even though operators usually need the draft answer first and the evidence list second.
- wide tables such as SOAT tariff responses still depended on an initially subtle horizontal scrollbar, making first-time scanning harder in the hosted Space.

The backend answer contract is already sufficient. The remaining work is a presentation-only refinement inside the public Gradio layer.

## Scope

This slice should:

1. Move `Citas clave` into its own collapsed accordion directly below the draft answer.
2. Preserve a clearly labeled evidence surface so operators can still validate document families quickly.
3. Improve wide-table usability in the answer/evidence markdown surfaces without reducing font size.
4. Add focused UI regression coverage and roadmap traceability for the new layout.

This slice should not:

- change retrieval, grounding, or response contracts;
- redesign the broader app architecture;
- replace Markdown rendering with a custom table component;
- expand into unrelated visual polish work.

## Required Behavior

### 1. Compact evidence layout

Acceptance criteria:

- `Respuesta sugerida` remains the primary visible answer surface;
- `Citas clave` is exposed through a visible accordion label rather than a permanently expanded block;
- the accordion defaults to closed;
- the evidence content remains available with the same backend-provided Markdown output.

### 2. Better wide-table affordance

Acceptance criteria:

- the answer surface shows an explicit horizontal-scroll affordance before the user inspects a wide table;
- wide tables in the answer, citations, and documentary-basis surfaces reserve stable scrollbar space where supported;
- the first table column remains readable while the user scrolls horizontally;
- the current font size remains unchanged.

### 3. Narrow UI-only scope

Acceptance criteria:

- the change remains inside `app/ui.py`, documentation, and focused UI tests;
- status/review cards keep their existing behavior;
- no backend or contract files need to change.

