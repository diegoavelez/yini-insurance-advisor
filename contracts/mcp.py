"""Minimal MCP transport and server contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

MCPProtocolVersion = Literal["2026-05-21"]
MCPRequestMethod = Literal["initialize", "ping"]


class MCPServerCapabilities(BaseModel):
    """Minimal server capability advertisement for the MCP seam."""

    tools_supported: bool = False
    client_roundtrip_supported: bool = False


class MCPServerMetadata(BaseModel):
    """Minimal MCP server identity metadata."""

    name: str = Field(min_length=1)
    version: str = Field(min_length=1)
    protocol_version: MCPProtocolVersion
    capabilities: MCPServerCapabilities


class MCPRequestEnvelope(BaseModel):
    """Typed transport request envelope for the minimal MCP seam."""

    request_id: str = Field(min_length=1)
    method: MCPRequestMethod
    protocol_version: MCPProtocolVersion


class MCPInitializeResult(BaseModel):
    """Typed initialize response body for the minimal MCP seam."""

    server: MCPServerMetadata


class MCPPingResult(BaseModel):
    """Typed ping response body for the minimal MCP seam."""

    ok: bool = True


class MCPResponseEnvelope(BaseModel):
    """Typed transport response envelope for the minimal MCP seam."""

    request_id: str = Field(min_length=1)
    protocol_version: MCPProtocolVersion
    result: MCPInitializeResult | MCPPingResult
