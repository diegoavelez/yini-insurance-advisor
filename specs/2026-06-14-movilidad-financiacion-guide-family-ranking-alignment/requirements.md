# Requirements

## Title

Constrain explicit financing-guide retrieval to the financing document family.

## Context

The extraction-readiness remediation for
`instructivo financiacion de polizas v1.pdf` is now complete:

- Docling now retries with full-page OCR when the first conversion produces
  only image placeholders or an insufficient text surface.
- The financing document now persists a usable cleaned-markdown surface and
  semantically meaningful chunks under
  `document_name = Manual Procedimiento Financiacion de polizas individuales`.

Live retrieval after that remediation improved but still shows one remaining
gap:

- financing-document chunks now appear in results;
- however, explicit financing queries still let `PROPUESTA DE VALOR MOVILIDAD`
  chunks about `fraccionamiento y financiación` outrank the financing guide.

This means the extraction problem is closed and the next narrow issue is now
query-family ranking/scope alignment.

## Scope

This slice should:

1. add a narrow operator-curated filter rule for explicit financing-guide
   intent queries;
2. constrain retrieval to the financing guide family when that rule matches;
3. keep broader movilidad guide retrieval unchanged.

This slice should not:

- reopen extraction logic;
- broaden into `suscripción`;
- redesign the shared `product=movilidad` taxonomy;
- introduce broad reranking logic before exhausting the existing filter seam.

## Required Behavior

### 1. Explicit financing-guide scoping

Acceptance criteria:

- explicit financing queries can match a curated `query_filter_rule` that sets
  `document_name = Manual Procedimiento Financiacion de polizas individuales`;
- the rule requires a financing anchor such as `financiación` together with
  guide-intent wording such as `cómo funciona`, `opciones`, `cuotas`, or
  comparable operational phrasing;
- explicit caller-provided `document_name` filters still take precedence.

### 2. Retrieval-family alignment

Acceptance criteria:

- normalized retrieval queries carry the financing-guide `document_name` filter
  when the rule matches;
- Qdrant query filters include that `document_name` constraint;
- local lexical candidates from adjacent mobility guides such as
  `PROPUESTA DE VALOR MOVILIDAD` are excluded by the same rule.

### 3. Backward compatibility

Acceptance criteria:

- current retrieval tests still pass;
- non-financing mobility queries do not inherit the new filter;
- the public retrieval contract remains unchanged.

### 4. Documentation and roadmap

Acceptance criteria:

- the roadmap records the extraction slice as complete;
- the roadmap records this guide-family ranking correction as the remaining
  financing slice.
