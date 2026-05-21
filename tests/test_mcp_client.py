from __future__ import annotations

from contracts import MCPInitializeResult, MCPToolCallResult
from core.mcp_client import create_local_mcp_client
from core.mcp_server import create_minimal_mcp_server


def test_local_mcp_client_initializes_against_server() -> None:
    client = create_local_mcp_client(create_minimal_mcp_server())

    result = client.initialize()

    assert isinstance(result, MCPInitializeResult)
    assert result.server.capabilities.tools_supported is True
    assert result.server.capabilities.client_roundtrip_supported is True


def test_local_mcp_client_lists_registered_tools() -> None:
    client = create_local_mcp_client(create_minimal_mcp_server())

    tools = client.list_tools()

    assert [tool.name for tool in tools] == ["document_retrieval", "clause_extraction"]


def test_local_mcp_client_calls_registered_tool_end_to_end() -> None:
    client = create_local_mcp_client(create_minimal_mcp_server())

    result = client.call_tool(
        "clause_extraction",
        {
            "retrieved_chunks": [
                {
                    "chunk_id": "chunk-1",
                    "text": "Coverage applies when prior authorization is required.",
                    "document_name": "policy-a",
                    "page": 2,
                    "section": "Coverage",
                    "clause_id": "2.1",
                    "score": 0.9,
                }
            ]
        },
    )

    assert isinstance(result, MCPToolCallResult)
    assert result.tool_name == "clause_extraction"
    assert result.payload["ok"] is True
    assert result.payload["result"]["clauses"][0]["category"] == "requirement"
