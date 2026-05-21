"""Minimal MCP server seam with narrow tool registration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from agents import clause_extraction_tool, document_retrieval_tool
from contracts import (
    MCPInitializeResult,
    MCPPingResult,
    MCPRequestEnvelope,
    MCPResponseEnvelope,
    MCPServerCapabilities,
    MCPServerMetadata,
    MCPToolCallResult,
    MCPToolDescriptor,
    MCPToolListResult,
    RetrievalQuery,
    RetrievedChunk,
)

MCP_SERVER_PROTOCOL_VERSION = "2026-05-21"
MCP_SERVER_NAME = "yini-mcp"
MCP_SERVER_VERSION = "0.1.0"


@dataclass(frozen=True)
class MCPRegisteredTool:
    """One narrow MCP-visible tool registration."""

    descriptor: MCPToolDescriptor
    handler: Callable[[dict[str, Any]], dict[str, Any]]


class MinimalMCPServer:
    """Narrow MCP server boundary for future tool exposure."""

    def __init__(self, *, tools: dict[str, MCPRegisteredTool] | None = None) -> None:
        self._tools = tools or default_mcp_tool_registry()

    def server_metadata(self) -> MCPServerMetadata:
        """Return the current MCP server identity and capability surface."""

        return MCPServerMetadata(
            name=MCP_SERVER_NAME,
            version=MCP_SERVER_VERSION,
            protocol_version=MCP_SERVER_PROTOCOL_VERSION,
            capabilities=MCPServerCapabilities(
                tools_supported=True,
                client_roundtrip_supported=True,
            ),
        )

    def list_tools(self) -> list[MCPToolDescriptor]:
        """Return the narrow MCP-visible tool surface."""

        return [registered_tool.descriptor for registered_tool in self._tools.values()]

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> MCPToolCallResult:
        """Execute one registered tool through the MCP server seam."""

        registered_tool = self._tools[tool_name]
        return MCPToolCallResult(
            tool_name=tool_name,
            payload=registered_tool.handler(arguments),
        )

    def handle_request(self, request: MCPRequestEnvelope) -> MCPResponseEnvelope:
        """Handle one typed MCP request over the current narrow server seam."""

        if request.method == "initialize":
            result = MCPInitializeResult(server=self.server_metadata())
        elif request.method == "ping":
            result = MCPPingResult()
        elif request.method == "list_tools":
            result = MCPToolListResult(tools=self.list_tools())
        else:
            if request.tool_name is None:
                raise ValueError("tool_name is required for call_tool requests.")
            result = self.call_tool(request.tool_name, request.arguments)

        return MCPResponseEnvelope(
            request_id=request.request_id,
            protocol_version=request.protocol_version,
            result=result,
        )


def _document_retrieval_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    retrieval_query = RetrievalQuery.model_validate(arguments)
    tool_result = document_retrieval_tool(retrieval_query)
    return tool_result.model_dump(mode="json")


def _clause_extraction_handler(arguments: dict[str, Any]) -> dict[str, Any]:
    retrieved_chunks = [
        RetrievedChunk.model_validate(item)
        for item in arguments["retrieved_chunks"]
    ]
    tool_result = clause_extraction_tool(retrieved_chunks)
    return tool_result.model_dump(mode="json")


def default_mcp_tool_registry() -> dict[str, MCPRegisteredTool]:
    """Return the narrow initial MCP-visible tool registry."""

    return {
        "document_retrieval": MCPRegisteredTool(
            descriptor=MCPToolDescriptor(
                name="document_retrieval",
                description="Retrieve ranked document chunks for a typed retrieval query.",
                input_schema={
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "top_k": {"type": "integer"},
                        "filters": {"type": "object"},
                    },
                },
            ),
            handler=_document_retrieval_handler,
        ),
        "clause_extraction": MCPRegisteredTool(
            descriptor=MCPToolDescriptor(
                name="clause_extraction",
                description="Extract typed clauses from retrieved evidence chunks.",
                input_schema={
                    "type": "object",
                    "required": ["retrieved_chunks"],
                    "properties": {
                        "retrieved_chunks": {
                            "type": "array",
                            "items": {"type": "object"},
                        }
                    },
                },
            ),
            handler=_clause_extraction_handler,
        ),
    }


def create_minimal_mcp_server() -> MinimalMCPServer:
    """Create the minimal MCP server seam for this repository."""

    return MinimalMCPServer()
