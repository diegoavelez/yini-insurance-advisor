# Requirements

## Title

Normalize `ARL/RUI` FAQ structure so live retrieval and citations point to the
exact numbered question evidence instead of noisy portal headings.

## Context

The `ARL` corpus is already operationally live in Qdrant, and representative
`ARL/RUI` grounded answers now complete successfully. Live validation exposed a
narrow remaining quality gap in one document:

- `ARL/preguntas frecuentes registro unico de intermediacion - rui.pdf`

The current cleaned markdown preserves noisy portal artifacts such as the Vimeo
recording heading, `MINISTERIODELTRABAJO`, and a large status table. It also
keeps multiple FAQ questions in one mixed preamble block before semantic
headings begin.

As a result:

- retrieval sections are labeled with noisy headings instead of the exact FAQ
  question;
- answer citations and documentary basis can include lateral numbered
  questions unrelated to the operator’s exact normativity query.

## Scope

This slice should:

1. add narrow document-specific normalization for the `ARL/RUI` FAQ;
2. promote each numbered FAQ question into a semantic heading;
3. suppress the noisy portal/table block that interrupts the FAQ flow;
4. improve downstream citation precision through better chunk structure rather
   than broader answer-contract redesign.

This slice should not:

- redesign generic FAQ ingestion for unrelated documents;
- broaden answer-time filtering or LLM prompting globally unless the normalized
  structure is still insufficient;
- remove legitimate ARL/RUI question content from the corpus.

## Required Behavior

### 1. FAQ heading normalization

Acceptance criteria:

- the document normalizes to one stable root heading for the FAQ;
- numbered questions such as `1. ¿Cuál es la normatividad... ?` and
  `2. Teniendo en cuenta...` become semantic markdown headings;
- noisy headings such as the Vimeo recording label and
  `MINISTERIODELTRABAJO` no longer survive as semantic sections.

### 2. Portal-block suppression

Acceptance criteria:

- the temporary portal/status block between the early FAQ questions and the
  later numbered questions is removed from the normalized FAQ surface;
- table rows and portal CTA fragments do not become retrieval chunks or
  citation sections.

### 3. Citation-traceability improvement

Acceptance criteria:

- rebuilding the FAQ chunk bundle yields question-labeled sections for the
  early ARL/RUI normativity content;
- live retrieval for the RUI normativity query returns the exact question
  section first;
- live grounded answers no longer need noisy section labels for their primary
  citations.
