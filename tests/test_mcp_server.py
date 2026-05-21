from __future__ import annotations

from pydantic import ValidationError

from contracts import (
    MCPInitializeResult,
    MCPPingResult,
    MCPRequestEnvelope,
    MCPResponseEnvelope,
    MCPServerMetadata,
)
from core.mcp_server import (
    MCP_SERVER_NAME,
    MCP_SERVER_PROTOCOL_VERSION,
    create_minimal_mcp_server,
)


def test_mcp_request_envelope_rejects_unknown_method() -> None:
    try:
        MCPRequestEnvelope(
            request_id="req-1",
            method="list_tools",
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
    assert metadata.capabilities.tools_supported is False


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
