# Validation

## Required Checks

- `ruff check .`
- `pytest`

## Required Test Scenarios

### Retrieval and Document Contracts

- A retrieved chunk can be created with the PRD-required metadata fields.
- Retrieval request filters accept optional document metadata.
- Invalid retrieval input values fail loudly when constrained.

### Clause and Comparison Contracts

- Valid clause categories are accepted.
- Invalid clause categories are rejected.
- Policy comparison contracts can represent both populated comparisons and
  insufficient-information cases.

### Response Contracts

- Citation models preserve document/page/section/clause traceability.
- Confidence values are restricted to `high`, `medium`, or `low`.
- Advisor response contracts can represent the PRD structured response shape.

### Workflow State

- The workflow state can be constructed with retrieval, clause, citation, and
  response data.
- Invalid confidence values fail.
- The state keeps list-like fields typed rather than raw dictionaries.

## Merge Readiness

The feature is ready to merge when the shared contract surface exists, matches
the PRD vocabulary, and is covered by tests for key valid and invalid cases.
