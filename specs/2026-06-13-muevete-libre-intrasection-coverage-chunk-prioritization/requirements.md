# Requirements

## Title

Prefer descriptive `Muévete Libre` coverage chunks over operational reminders
within the same coverage section.

## Context

The previous coverage-breadth slice improved horizontal evidence selection
across distinct sections such as `1.1`, `1.2`, `2.1`, `3.1`, and `4.1`.

Runtime validation still shows a narrower vertical issue inside some repeated
sections, especially `4.1. Cobertura`: the retrieval result may keep the
section breadth but still choose the operational reminder chunk
(`Recuerda que para activar...`) instead of the more descriptive chunk that
actually explains what the coverage pays for.

The next narrow slice should fix that local ordering issue without changing the
public retrieval contract.

## Scope

This slice should:

- keep retrieval contracts unchanged;
- add a deterministic descriptive-vs-operational preference within duplicated
  explicit coverage sections;
- remain scoped to coverage-intent queries and explicit coverage sections.

This slice should not:

- add model-based summarization;
- redesign chunking;
- hardcode one document id or one exact section id.

## Acceptance Criteria

### 1. Intra-section descriptive preference

- When two explicit coverage chunks belong to the same section, the chunk that
  actually describes the coverage should outrank a chunk that mainly contains
  operational reminders or activation instructions.

### 2. Backward compatibility

- Existing coverage-breadth and coverage-intent retrieval behavior remains
  intact.
- Focused retrieval tests pass.
