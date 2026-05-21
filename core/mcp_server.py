"""Minimal MCP server seam without tool execution wiring."""

from __future__ import annotations

from contracts import (
    MCPInitializeResult,
    MCPPingResult,
    MCPRequestEnvelope,
    MCPResponseEnvelope,
    MCPServerCapabilities,
    MCPServerMetadata,
)

MCP_SERVER_PROTOCOL_VERSION = "2026-05-21"
MCP_SERVER_NAME = "yini-mcp"
MCP_SERVER_VERSION = "0.1.0"


class MinimalMCPServer:
    """Narrow MCP server boundary for future tool exposure."""

    def server_metadata(self) -> MCPServerMetadata:
        """Return the current MCP server identity and capability surface."""

        return MCPServerMetadata(
            name=MCP_SERVER_NAME,
            version=MCP_SERVER_VERSION,
            protocol_version=MCP_SERVER_PROTOCOL_VERSION,
            capabilities=MCPServerCapabilities(
                tools_supported=False,
                client_roundtrip_supported=False,
            ),
        )

    def handle_request(self, request: MCPRequestEnvelope) -> MCPResponseEnvelope:
        """Handle one typed MCP request without executing repository tools."""

        if request.method == "initialize":
            result = MCPInitializeResult(server=self.server_metadata())
        else:
            result = MCPPingResult()

        return MCPResponseEnvelope(
            request_id=request.request_id,
            protocol_version=request.protocol_version,
            result=result,
        )


def create_minimal_mcp_server() -> MinimalMCPServer:
    """Create the minimal MCP server seam for this repository."""

    return MinimalMCPServer()
