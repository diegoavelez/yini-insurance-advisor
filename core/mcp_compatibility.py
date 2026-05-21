"""Explicit MCP compatibility boundaries for the current repository surface."""

from __future__ import annotations

from contracts import (
    MCPCompatibilityBoundary,
    MCPCompatibilityExpectation,
)
from core.mcp_server import MCP_SERVER_PROTOCOL_VERSION, create_minimal_mcp_server

CURRENT_MCP_COMPATIBILITY_SURFACE = "current_mcp_server_surface"


def build_mcp_tool_compatibility_boundary() -> MCPCompatibilityBoundary:
    """Return explicit compatibility expectations for the current MCP surface."""

    server = create_minimal_mcp_server()
    tool_names = [tool.name for tool in server.list_tools()]

    return MCPCompatibilityBoundary(
        protocol_version=MCP_SERVER_PROTOCOL_VERSION,
        surface=CURRENT_MCP_COMPATIBILITY_SURFACE,
        methods=["initialize", "ping", "list_tools", "call_tool"],
        tool_names=tool_names,
        expectations=[
            MCPCompatibilityExpectation(
                surface_area="request_methods",
                compatible_changes=[
                    "internal refactors with no MCP-visible request-method change",
                ],
                breaking_changes=[
                    "removing an exposed request method",
                    "renaming an exposed request method",
                ],
            ),
            MCPCompatibilityExpectation(
                surface_area="request_fields",
                compatible_changes=[
                    "adding optional request fields without changing existing field meaning",
                    (
                        "internal validation changes that preserve existing "
                        "request-field names and semantics"
                    ),
                ],
                breaking_changes=[
                    "removing an exposed request field",
                    "renaming an exposed request field",
                    "changing an optional request field to required",
                ],
            ),
            MCPCompatibilityExpectation(
                surface_area="tool_registration",
                compatible_changes=[
                    "preserving an existing tool name, purpose, and input contract",
                ],
                breaking_changes=[
                    "removing an exposed tool",
                    "renaming an exposed tool",
                ],
            ),
            MCPCompatibilityExpectation(
                surface_area="tool_metadata",
                compatible_changes=[
                    "clarifying a tool description without changing the tool purpose",
                    "adding optional metadata details without changing existing metadata meaning",
                ],
                breaking_changes=[
                    "changing the meaning of existing tool metadata fields",
                    "removing an exposed tool-metadata field relied on by clients",
                ],
            ),
            MCPCompatibilityExpectation(
                surface_area="response_shapes",
                compatible_changes=[
                    "internal implementation changes that preserve MCP response fields",
                ],
                breaking_changes=[
                    "removing an exposed response field",
                    "changing the meaning of an exposed response field",
                ],
            ),
        ],
        alignment_note=(
            "These boundaries align with the MCP interface version policy: additive or "
            "breaking MCP-visible surface changes require a version bump."
        ),
    )
