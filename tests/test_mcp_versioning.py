from __future__ import annotations

from contracts import MCPInterfaceVersionPolicy
from core.mcp_server import MCP_SERVER_PROTOCOL_VERSION
from core.mcp_versioning import build_mcp_interface_version_policy


def test_build_mcp_interface_version_policy_returns_typed_policy() -> None:
    policy = build_mcp_interface_version_policy()

    assert isinstance(policy, MCPInterfaceVersionPolicy)
    assert policy.current_version == MCP_SERVER_PROTOCOL_VERSION
    assert policy.version_format == "date_based"


def test_build_mcp_interface_version_policy_defines_operational_rules() -> None:
    policy = build_mcp_interface_version_policy()

    rules_by_class = {rule.change_class: rule for rule in policy.rules}

    assert rules_by_class["internal_only"].requires_version_bump is False
    assert rules_by_class["additive_mcp_surface"].requires_version_bump is True
    assert rules_by_class["breaking_mcp_surface"].requires_version_bump is True


def test_build_mcp_interface_version_policy_points_to_current_version_source() -> None:
    policy = build_mcp_interface_version_policy()

    assert policy.version_source == "core.mcp_server.MCP_SERVER_PROTOCOL_VERSION"
