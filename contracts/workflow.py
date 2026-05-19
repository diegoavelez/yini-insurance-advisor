"""Workflow execution contracts."""

from __future__ import annotations

from pydantic import BaseModel

from contracts.responses import AdvisorDraftResponse
from contracts.state import AgentState
from contracts.tools import ToolError


class WorkflowExecutionResult(BaseModel):
    """Typed successful output for the first LangGraph workflow slice."""

    state: AgentState
    response: AdvisorDraftResponse


class LangGraphWorkflowToolResult(BaseModel):
    """Typed success or failure result for the LangGraph workflow wrapper."""

    ok: bool
    result: WorkflowExecutionResult | None = None
    error: ToolError | None = None
