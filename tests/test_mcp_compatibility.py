from __future__ import annotations

from contracts import MCPCompatibilityBoundary
from core.mcp_compatibility import (
    CURRENT_MCP_COMPATIBILITY_SURFACE,
    build_mcp_tool_compatibility_boundary,
)
from core.mcp_server import MCP_SERVER_PROTOCOL_VERSION


def test_build_mcp_tool_compatibility_boundary_returns_typed_boundary() -> None:
    boundary = build_mcp_tool_compatibility_boundary()

    assert isinstance(boundary, MCPCompatibilityBoundary)
    assert boundary.protocol_version == MCP_SERVER_PROTOCOL_VERSION
    assert boundary.surface == CURRENT_MCP_COMPATIBILITY_SURFACE


def test_build_mcp_tool_compatibility_boundary_tracks_current_surface() -> None:
    boundary = build_mcp_tool_compatibility_boundary()

    assert boundary.methods == ["initialize", "ping", "list_tools", "call_tool"]
    assert boundary.tool_names == ["document_retrieval", "clause_extraction"]


def test_build_mcp_tool_compatibility_boundary_defines_breaking_changes() -> None:
    boundary = build_mcp_tool_compatibility_boundary()

    expectations = {item.surface_area: item for item in boundary.expectations}
    assert "removing an exposed tool" in expectations["tool_registration"].breaking_changes
    assert "removing an exposed request method" in expectations["request_methods"].breaking_changes
    assert "renaming an exposed request field" in expectations["request_fields"].breaking_changes
    assert (
        "changing the meaning of existing tool metadata fields"
        in expectations["tool_metadata"].breaking_changes
    )
    assert "version policy" in boundary.alignment_note.lower()
