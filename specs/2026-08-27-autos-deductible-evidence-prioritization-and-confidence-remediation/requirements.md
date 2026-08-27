# Requirements

## Title

Autos deductible evidence prioritization and confidence remediation.

## Status and Authority

- Work type: narrow corrective slice in `retrieval/ranking/answering`.
- Planning and specification: authorized.
- Implementation, local verification of an implementation, commit, push,
  provider-backed execution, and deployment: not authorized by this spec.

## Context

The accepted `movilidad-deductibles-qa-coverage` slice routes general autos
deductible questions to `SEGURO DE AUTOS` and proves that expected terms exist
in the local corpus. After Qdrant restoration and Hugging Face publication, a
hosted smoke test confirmed that citations remain inside that document family
and that the answer can define and explain the deductible.

The smoke test also exposed a narrower failure family that the previous slice
did not accept or test end to end:

- the bounded candidate pool may contain direct deductible evidence without
  placing it first;
- hybrid score fusion can update scores while preserving pre-fusion insertion
  order;
- the answer path can receive lateral evidence before the direct deductible
  section;
- confidence can be reported as `high` from chunk count and citation presence
  without proving that direct evidence supports the autos deductible intent.

This is a correction to the accepted autos deductible behavior, tracked as a
new slice for traceability. It is not a new product feature or roadmap phase.

## Objective

For general autos deductible questions, make direct deductible evidence lead
retrieval, answer input, and citations, and prevent `high` confidence when that
direct support is absent.

## Scope

This slice should:

1. Use a bounded candidate pool large enough to compare direct and lateral
   `SEGURO DE AUTOS` evidence for general autos deductible intents.
2. Make hybrid score fusion return deterministic score order, with a stable
   tie-break that preserves original candidate order.
3. Prefer chunks whose section metadata and content directly define, explain,
   or calculate the deductible over chunks that merely mention a deductible.
4. Preserve the normalized `SEGURO DE AUTOS` family boundary established by
   the prior slice.
5. Ensure answer-facing evidence and citation order preserve the same direct
   evidence priority.
6. Keep confidence at `medium` or below, with an explicit evidence limitation,
   when an otherwise answerable general autos deductible response lacks direct
   deductible support.
7. Add deterministic tests at the retrieval and grounded-answer public seams.

## Non-goals

This slice should not:

- re-embed or reindex Qdrant;
- change the Qdrant collection schema, payload indexes, or embedding model;
- add new insurance categories or broaden supported scope;
- redesign general retrieval, prompts, citations, or confidence semantics;
- change confidence behavior for unrelated intents or product families;
- change public response contracts;
- publish to `origin` or `hf`, deploy, or run provider-backed checks without a
  later explicit authority.

## Required Behavior

### 1. Bounded autos deductible candidate comparison

For a general autos/vehiculos deductible query normalized to
`document_name=SEGURO DE AUTOS`, retrieval must inspect more than the requested
`top_k` when needed to compare direct deductible evidence with lateral mentions.
The expansion must remain bounded by the repository's existing candidate-pool
limits.

### 2. Deterministic fused ordering

After semantic and local lexical candidates are fused, candidates must be
ordered by their fused score before downstream selection. Equal fused scores
must retain a deterministic original-order tie-break.

### 3. Direct evidence priority

For the target intent, a chunk that explicitly defines the deductible or
explains its calculation must outrank same-family chunks that only mention that
a deductible applies. The direct chunk must appear in the final retrieval
`top_k` and before lateral support when both are available.

### 4. Answer and citation alignment

The evidence supplied to answer generation and the resulting citations must
lead with direct autos deductible support. Lateral same-family chunks may remain
only when they add material support and do not displace the direct evidence.

### 5. Evidence-aware confidence

For the target intent, `high` confidence requires all existing grounding
conditions plus at least one selected chunk that directly supports the
deductible definition or calculation. If direct support is absent, the response
must not report `high` confidence and must disclose the evidence limitation.

### 6. Compatibility

- Autos Basico PT and autos assistance deductible routing remain unchanged.
- Motos, bicicletas/patinetas, utilitarios/pesados, and Muevete Libre deductible
  routing remains unchanged.
- Non-deductible retrieval ordering and unrelated confidence behavior remain
  unchanged unless the generic fused-order invariant applies.
- Public contracts remain unchanged.

## Acceptance Criteria

- A deterministic retrieval test proves fused candidates are score-ordered and
  ties are stable.
- A deterministic end-to-end retrieval test for a representative general autos
  deductible query returns direct `SEGURO DE AUTOS` evidence before lateral
  same-family evidence.
- The direct evidence remains present when the requested `top_k` is smaller
  than the bounded candidate pool.
- A grounded-answer test proves that answer input, documentary basis, and
  citations lead with direct deductible evidence.
- A grounded-answer test proves that lateral-only autos deductible evidence
  cannot produce `high` confidence and surfaces a limitation.
- Existing movilidad deductible routing and focused retrieval tests pass.
- The repository release gate passes, subject to already documented baseline
  exceptions.

