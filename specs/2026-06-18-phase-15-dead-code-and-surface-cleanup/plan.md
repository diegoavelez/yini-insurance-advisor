# Plan — phase-15-dead-code-and-surface-cleanup

## Objective

Remove one clearly dead repository surface without broadening into speculative
cleanup.

## Affected Files

- `mcp/__init__.py`
- `README.md`
- `docs/architecture.md`
- `specs/roadmap.md`

## Assumptions

- No runtime or test code imports the empty `mcp` package directly.
- The real MCP boundary is already implemented and tested in `core/mcp_*`.

## Risks

- A stale documentation or tooling reference could still point at `mcp/`.
- The cleanup could drift into a broader MCP refactor if not kept narrow.

## Execution Steps

1. Remove the empty `mcp/__init__.py` placeholder.
2. Update repository-surface docs to point only to `core/mcp_*`.
3. Record the dated cleanup slice in `specs/roadmap.md`.
4. Run focused MCP validation and import/reference searches.

## Verification Strategy

- Search the repo for `mcp/` repository-surface references.
- Run focused MCP tests covering the real implementation seams.
