# Requirements — phase-15-dead-code-and-surface-cleanup

## Context

`Phase 15 — Final Evaluation and Cleanup` still lists `cleanup of dead code` as
one of its deliverables. The repository currently exposes an `mcp/` package
surface in documentation, but the package itself is only an empty placeholder
module. The actual MCP implementation already lives under `core/mcp_*`.

This creates an unnecessary repository surface: readers are told that MCP
integration spans both `mcp/` and `core/mcp_*`, while the versioned `mcp/`
package contains no runtime code, tests, or supported boundary.

## Goal

Close one narrow dead-surface cleanup slice by removing the empty `mcp/`
placeholder package and synchronizing the documented repository surface to the
real MCP implementation boundary.

## In Scope

- Remove the empty versioned `mcp/__init__.py` placeholder package surface.
- Update durable docs that currently present `mcp/` as part of the supported
  repository architecture.
- Update the roadmap so `Phase 15` explicitly records this cleanup slice.

## Out of Scope

- Refactoring the real MCP implementation under `core/mcp_*`.
- Changing MCP contracts, protocol versions, or tool registration behavior.
- Broader cleanup of future-facing seams that still have tests or active
  implementation value.

## Acceptance Criteria

1. The repository no longer contains the versioned placeholder file
   `mcp/__init__.py`.
2. `README.md` no longer lists `mcp/` as a supported repository surface.
3. `docs/architecture.md` no longer claims that MCP integration is split across
   `mcp/` and `core/mcp_*`; it should point to the real `core/mcp_*` boundary.
4. `specs/roadmap.md` records this dated slice and notes that the Phase 15
   dead-code cleanup deliverable is satisfied by removing the empty MCP package
   surface.
5. Focused validation demonstrates that MCP tests still pass after the cleanup.
