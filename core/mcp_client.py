"""Local MCP client seam for repository roundtrip validation."""

from __future__ import annotations

from typing import Any

from contracts import (
    MCPInitializeResult,
    MCPRequestEnvelope,
    MCPResponseEnvelope,
    MCPToolCallResult,
    MCPToolDescriptor,
    MCPToolListResult,
)
from core.mcp_server import MCP_SERVER_PROTOCOL_VERSION, MinimalMCPServer


class LocalMCPClient:
    """Narrow local MCP client over the in-process server seam."""

    def __init__(self, server: MinimalMCPServer) -> None:
        self._server = server
        self._request_counter = 0

    def _next_request_id(self) -> str:
        self._request_counter += 1
        return f"mcp-client-{self._request_counter}"

    def _send(self, **payload: Any) -> MCPResponseEnvelope:
        request = MCPRequestEnvelope(
            request_id=self._next_request_id(),
            protocol_version=MCP_SERVER_PROTOCOL_VERSION,
            **payload,
        )
        return self._server.handle_request(request)

    def initialize(self) -> MCPInitializeResult:
        """Initialize against the local MCP server seam."""

        response = self._send(method="initialize")
        assert isinstance(response.result, MCPInitializeResult)
        return response.result

    def list_tools(self) -> list[MCPToolDescriptor]:
        """List the current MCP-visible tool surface."""

        response = self._send(method="list_tools")
        assert isinstance(response.result, MCPToolListResult)
        return response.result.tools

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> MCPToolCallResult:
        """Call one MCP-visible tool over the local client/server seam."""

        response = self._send(
            method="call_tool",
            tool_name=tool_name,
            arguments=arguments,
        )
        assert isinstance(response.result, MCPToolCallResult)
        return response.result


def create_local_mcp_client(server: MinimalMCPServer) -> LocalMCPClient:
    """Create the narrow local MCP client seam for this repository."""

    return LocalMCPClient(server)
