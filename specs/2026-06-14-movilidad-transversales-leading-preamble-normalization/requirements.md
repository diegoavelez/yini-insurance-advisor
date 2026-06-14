# Requirements

## Title

Normalize leading preambles for `MOVILIDAD/TRANSVERSALES` choque-simple process guides.

## Context

The current `MOVILIDAD/TRANSVERSALES` cohort is fully ingested and indexed, but
two process guides still show a narrow ingestion-quality defect:

- `proceso atencion choque simple v2.pdf` emits one leading chunk with
  `section = None` from noisy preamble text such as `Normatividad vigente`;
- `proceso recobro choque simple v2.pdf` emits one leading chunk with
  `section = None` because meaningful introductory text appears before the first
  explicit heading.

This is now a narrow preamble-normalization problem for two already onboarded
guides, not a coverage or indexing gap for the broader `TRANSVERSALES` corpus.

## Scope

This slice should:

1. preserve current ingestion success for all `MOVILIDAD/TRANSVERSALES` files;
2. normalize the leading preamble of the two affected choque-simple process
   guides into stable semantic root headings;
3. eliminate meaningless leading chunks with no section for those two guides.

This slice should not:

- reopen ranking or retrieval alignment for already stabilized transversal
  slices;
- redesign generic document-name inference or heading normalization globally;
- alter unrelated `TRANSVERSALES` artifacts that already have stable sections.

## Required Behavior

### 1. Leading preamble normalization

Acceptance criteria:

- `proceso atencion choque simple v2` no longer surfaces the noisy preamble as
  a standalone leading chunk;
- `proceso recobro choque simple v2` promotes a stable root heading so the
  opening advisory text belongs to a named section.

### 2. Chunk quality recovery

Acceptance criteria:

- the first chunk for each affected guide has a meaningful `section` and
  `section_path`;
- no leading chunk with `section = None` remains for those two guides.

### 3. Traceability

Acceptance criteria:

- the roadmap records this slice as the next active transversal hardening gap;
- the dated validation file records the current preamble-chunk baseline and the
  intended completion checks.
