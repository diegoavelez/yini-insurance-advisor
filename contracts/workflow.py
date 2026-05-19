"""Workflow execution contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from contracts.responses import AdvisorDraftResponse
from contracts.state import AgentState
from contracts.tools import ToolError

PlannerRoute = Literal["grounded_qa", "unsupported"]


class PlannerDecision(BaseModel):
    """Typed planner routing decision for the LangGraph workflow."""

    route: PlannerRoute
    reason: str


class WorkflowExecutionResult(BaseModel):
    """Typed successful output for the first LangGraph workflow slice."""

    state: AgentState
    response: AdvisorDraftResponse


class LangGraphWorkflowToolResult(BaseModel):
    """Typed success or failure result for the LangGraph workflow wrapper."""

    ok: bool
    result: WorkflowExecutionResult | None = None
    error: ToolError | None = None
