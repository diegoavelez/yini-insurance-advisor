# Requirements

## Title

Improve hosted Spaces readability for wide answer tables without shrinking the font.

## Context

During the hosted manual MVP QA pass on 2026-06-20, the SOAT 2026 tariff response rendered a wide Markdown table whose numeric values wrapped awkwardly inside narrow cells, visually cutting trailing zeros and making the tariff grid difficult to read.

The answer content was correct; the issue is purely presentational in the public Gradio UI. The narrowest corrective action is to add scoped table styling for the answer surface so wide tables scroll horizontally instead of compressing cell contents.

## Scope

This slice should:

1. Add scoped Gradio styling for wide Markdown tables in the answer surface.
2. Preserve the current font size.
3. Keep the fix limited to the public UI layer.
4. Add focused UI layout regression coverage for the new styling surface.

This slice should not:

- change retrieval, grounding, or answer content;
- rewrite Markdown tables into another component type;
- globally restyle all markdown in unrelated surfaces;
- shrink fonts to force the table to fit.

## Required Behavior

### 1. Wide answer tables remain readable

Acceptance criteria:

- wide tables in `Respuesta sugerida` can scroll horizontally within the answer surface;
- table cells no longer wrap numeric values in a way that visually truncates amounts;
- the current default font size is preserved.

### 2. Scope stays narrow

Acceptance criteria:

- the styling is scoped to the public Gradio answer/documentary surfaces that may contain wide tables;
- textbox-based status panels remain unchanged;
- no backend contract changes are required.

### 3. Regression safety

Acceptance criteria:

- focused UI tests assert the CSS surface is wired into the Gradio app build;
- focused UI tests assert the answer markdown component carries the expected styling class.
