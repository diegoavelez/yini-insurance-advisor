from __future__ import annotations

from pydantic import ValidationError

from contracts import (
    MCPInitializeResult,
    MCPPingResult,
    MCPRequestEnvelope,
    MCPResponseEnvelope,
    MCPServerMetadata,
    MCPToolCallResult,
    MCPToolDescriptor,
    MCPToolListResult,
)
from core.mcp_server import (
    MCP_SERVER_NAME,
    MCP_SERVER_PROTOCOL_VERSION,
    MCPRegisteredTool,
    MinimalMCPServer,
    create_minimal_mcp_server,
)


def test_mcp_request_envelope_rejects_unknown_method() -> None:
    try:
        MCPRequestEnvelope(
            request_id="req-1",
            method="unknown_method",
            protocol_version=MCP_SERVER_PROTOCOL_VERSION,
        )
    except ValidationError:
        return

    raise AssertionError("Expected ValidationError for unknown MCP method.")


def test_minimal_mcp_server_exposes_typed_metadata() -> None:
    server = create_minimal_mcp_server()

    metadata = server.server_metadata()

    assert isinstance(metadata, MCPServerMetadata)
    assert metadata.name == MCP_SERVER_NAME
    assert metadata.protocol_version == MCP_SERVER_PROTOCOL_VERSION
    assert metadata.capabilities.tools_supported is True


def test_minimal_mcp_server_handles_initialize_request() -> None:
    server = create_minimal_mcp_server()
    request = MCPRequestEnvelope(
        request_id="req-1",
        method="initialize",
        protocol_version=MCP_SERVER_PROTOCOL_VERSION,
    )

    response = server.handle_request(request)

    assert isinstance(response, MCPResponseEnvelope)
    assert response.request_id == "req-1"
    assert isinstance(response.result, MCPInitializeResult)
    assert response.result.server.name == MCP_SERVER_NAME


def test_minimal_mcp_server_handles_ping_request() -> None:
    server = create_minimal_mcp_server()
    request = MCPRequestEnvelope(
        request_id="req-2",
        method="ping",
        protocol_version=MCP_SERVER_PROTOCOL_VERSION,
    )

    response = server.handle_request(request)

    assert isinstance(response.result, MCPPingResult)
    assert response.result.ok is True


def test_minimal_mcp_server_lists_registered_tools() -> None:
    server = create_minimal_mcp_server()
    request = MCPRequestEnvelope(
        request_id="req-3",
        method="list_tools",
        protocol_version=MCP_SERVER_PROTOCOL_VERSION,
    )

    response = server.handle_request(request)

    assert isinstance(response.result, MCPToolListResult)
    tool_names = [tool.name for tool in response.result.tools]
    assert tool_names == ["document_retrieval", "clause_extraction"]


def test_minimal_mcp_server_can_call_registered_tool_through_server_seam() -> None:
    server = MinimalMCPServer(
        tools={
            "stub_tool": MCPRegisteredTool(
                descriptor=MCPToolDescriptor(
                    name="stub_tool",
                    description="Stub MCP-visible tool.",
                    input_schema={"type": "object"},
                ),
                handler=lambda arguments: {"echo": arguments["value"]},
            )
        }
    )
    request = MCPRequestEnvelope(
        request_id="req-4",
        method="call_tool",
        protocol_version=MCP_SERVER_PROTOCOL_VERSION,
        tool_name="stub_tool",
        arguments={"value": "ok"},
    )

    response = server.handle_request(request)

    assert isinstance(response.result, MCPToolCallResult)
    assert response.result.tool_name == "stub_tool"
    assert response.result.payload == {"echo": "ok"}
