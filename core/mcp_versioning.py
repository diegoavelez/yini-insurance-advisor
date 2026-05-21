"""Explicit MCP interface version policy for the current repository."""

from __future__ import annotations

from contracts import (
    MCPInterfaceVersionPolicy,
    MCPVersionChangeRule,
)
from core.mcp_server import MCP_SERVER_PROTOCOL_VERSION


def build_mcp_interface_version_policy() -> MCPInterfaceVersionPolicy:
    """Return the narrow MCP interface version policy for the current surface."""

    return MCPInterfaceVersionPolicy(
        current_version=MCP_SERVER_PROTOCOL_VERSION,
        version_format="date_based",
        version_source="core.mcp_server.MCP_SERVER_PROTOCOL_VERSION",
        rules=[
            MCPVersionChangeRule(
                change_class="internal_only",
                requires_version_bump=False,
                rationale=(
                    "Pure internal implementation changes that do not alter the "
                    "MCP-visible request, response, or tool surface keep the current version."
                ),
            ),
            MCPVersionChangeRule(
                change_class="additive_mcp_surface",
                requires_version_bump=True,
                rationale=(
                    "Any additive MCP-visible change, including new methods, new exposed "
                    "tools, or new response fields, must advance the interface version date."
                ),
            ),
            MCPVersionChangeRule(
                change_class="breaking_mcp_surface",
                requires_version_bump=True,
                rationale=(
                    "Any breaking MCP-visible contract change must advance the interface "
                    "version date before release."
                ),
            ),
        ],
    )
