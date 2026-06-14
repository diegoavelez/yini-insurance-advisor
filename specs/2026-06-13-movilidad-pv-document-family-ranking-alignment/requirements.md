# Requirements

## Title

Constrain movilidad PV benefit-intent retrieval to the PV document family.

## Context

The previous PV ranking-alignment slice added curated benefit-intent expansion
for `propuesta de valor movilidad`, which improved recall but still allowed
adjacent `MOVILIDAD/TRANSVERSALES` guides to enter the top results when they
shared strong lexical anchors such as `grúa de amplio alcance`.

Live validation showed that the query `qué beneficios incluye la propuesta de
valor de movilidad` still retrieved `ayudaventas utilitarios y pesados v2`
ahead of some PV chunks, even though the operator intent is explicitly about
the `PROPUESTA DE VALOR MOVILIDAD` document family.

The next narrow corrective slice should use the existing operator-curated query
filter seam to restrict this intent to the PV document family without changing
retrieval contracts or Qdrant payloads.

## Scope

This slice should:

1. Add an operator-curated query filter rule for explicit PV benefit-intent
   queries.
2. Constrain both semantic retrieval and local lexical recall to
   `document_name = PROPUESTA DE VALOR MOVILIDAD` when that rule matches.
3. Keep broader mobility retrieval behavior unchanged.

This slice should not:

- add new retrieval fields or payload schema;
- introduce hardcoded document-id checks in Python code;
- redesign the reranker;
- change non-PV mobility queries.

## Required Behavior

### 1. Operator-curated document-family scoping

When a query explicitly targets the movilidad value proposition and asks for
its benefits, retrieval should default to the PV document family.

Acceptance criteria:

- the query matches a curated `query_filter_rule` that sets
  `document_name = PROPUESTA DE VALOR MOVILIDAD`;
- the rule only applies when the query contains both the PV-family anchor and
  benefit-intent wording;
- explicit caller-provided `document_name` filters still take precedence.

### 2. Retrieval-family alignment

The existing retrieval pipeline should reuse the new filter for both Qdrant and
local lexical candidates.

Acceptance criteria:

- normalized retrieval queries carry the PV `document_name` filter when the
  rule matches;
- Qdrant query filters include that `document_name` constraint;
- local lexical candidates from adjacent mobility guides are excluded by the
  same rule.

### 3. Backward compatibility

Existing retrieval behavior outside this narrow scenario should remain stable.

Acceptance criteria:

- current retrieval tests still pass;
- non-PV mobility queries do not inherit the PV document-name filter;
- the public retrieval contracts remain unchanged.

### 4. Documentation and roadmap

The roadmap should record that this is a document-family scoping correction on
top of the previous PV ranking slice.

Acceptance criteria:

- the new slice is listed in the roadmap;
- the implementation note describes it as a narrow PV family constraint.
