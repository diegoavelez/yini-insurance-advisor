"""First LangGraph workflow skeleton over existing reusable tools."""

from __future__ import annotations

import importlib.util
import logging
from typing import Any

from agents.citation_verifier_tool import citation_verifier_tool
from agents.clause_extraction_tool import clause_extraction_tool
from agents.document_retrieval_tool import (
    document_retrieval_tool,
    unwrap_retrieval_tool_result,
)
from agents.policy_comparison_tool import policy_comparison_tool
from agents.response_draft_tool import response_draft_tool
from contracts import (
    AgentState,
    GroundingVerification,
    LangGraphWorkflowToolResult,
    PlannerDecision,
    RetrievalQuery,
    ToolError,
    WorkflowExecutionResult,
)
from core.config import Settings
from ops.observability import log_event, log_timed_event
from rag.ingestion import build_citations_from_chunks, build_documentary_basis

WORKFLOW_LOGGER = logging.getLogger("yini.workflow.langgraph")
SUPPORTED_QUERY_TOKENS = {
    "accident",
    "authorization",
    "benefit",
    "claim",
    "clause",
    "compare",
    "comparison",
    "copay",
    "coverage",
    "covered",
    "deductible",
    "difference",
    "endorsement",
    "exclusion",
    "hospital",
    "insurance",
    "policy",
    "premium",
    "procedure",
    "reimbursement",
    "restriction",
    "versus",
    "vs",
}


def langgraph_backend_is_available() -> bool:
    """Return whether the LangGraph backend is importable."""

    return importlib.util.find_spec("langgraph") is not None


def classify_langgraph_workflow_error(exc: Exception) -> ToolError:
    """Map workflow failures into the typed error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    message = str(exc).lower()
    if "langgraph" in message and ("not installed" in message or "unavailable" in message):
        return ToolError(kind="dependency_failure", message=str(exc))
    return ToolError(kind="workflow_failure", message=str(exc))


def validate_workflow_input(user_query: str) -> None:
    """Validate workflow input before execution."""

    if not isinstance(user_query, str) or not user_query.strip():
        raise ValueError("user_query must be a non-empty string.")


def build_initial_workflow_state(user_query: str) -> AgentState:
    """Build the initial shared workflow state."""

    return AgentState(
        user_query=user_query,
        plan=[
            "planner",
            "retrieve",
            "extract_clauses",
            "compare",
            "draft_initial",
            "verify_citations",
            "draft_final",
        ],
        trace_summary=["workflow_initialized"],
    )


def ensure_agent_state(state: AgentState | dict[str, Any]) -> AgentState:
    """Normalize a LangGraph state payload into the typed shared state."""

    if isinstance(state, AgentState):
        return state
    return AgentState.model_validate(state)


def append_trace(state: AgentState, message: str) -> list[str]:
    """Return the next trace summary list with one appended message."""

    return [*state.trace_summary, message]


def classify_planner_route(user_query: str) -> PlannerDecision:
    """Return a deterministic typed route decision for one user query."""

    normalized_tokens = {
        token.strip(".,:;!?()[]{}'\"").lower()
        for token in user_query.split()
        if token.strip(".,:;!?()[]{}'\"")
    }
    if normalized_tokens & SUPPORTED_QUERY_TOKENS:
        return PlannerDecision(
            route="grounded_qa",
            reason="Query matches supported insurance-document workflow patterns.",
        )
    return PlannerDecision(
        route="unsupported",
        reason="Query does not match supported insurance-document workflow patterns.",
    )


def emit_transition(
    *,
    request_id: str | None,
    step: str,
    status: str,
    **fields: object,
) -> None:
    """Emit one structured workflow transition event."""

    log_event(
        WORKFLOW_LOGGER,
        event_type="workflow_state_transition",
        request_id=request_id,
        workflow_step=step,
        transition_status=status,
        **fields,
    )


def planner_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the narrow planner step and record the route decision."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="planner", status="started")
    decision = classify_planner_route(typed_state.user_query)
    log_event(
        WORKFLOW_LOGGER,
        event_type="planner_route_selected",
        request_id=request_id,
        route=decision.route,
        reason=decision.reason,
    )
    emit_transition(
        request_id=request_id,
        step="planner",
        status="succeeded",
        route=decision.route,
    )
    return {
        "planner_route": decision.route,
        "planner_reason": decision.reason,
        "query_type": decision.route,
        "trace_summary": append_trace(typed_state, f"planner:{decision.route}"),
    }


def unsupported_route_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Return a conservative valid workflow outcome for unsupported routes."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="unsupported_route", status="started")
    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            "The query is outside the workflow's currently supported insurance-document scope."
        ],
        missing_citations=["No workflow evidence was gathered for this unsupported route."],
    )
    tool_result = response_draft_tool(
        typed_state.user_query,
        [],
        [],
        verification=verification,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Unsupported-route drafting failed."
        )
    emit_transition(
        request_id=request_id,
        step="unsupported_route",
        status="succeeded",
        confidence=tool_result.result.confidence,
    )
    return {
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "final_answer": tool_result.result.suggested_answer,
        "verification": verification,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "requires_human_review": True,
        "trace_summary": append_trace(typed_state, "workflow_completed_unsupported"),
    }


def retrieve_step(
    state: AgentState | dict[str, Any],
    *,
    settings: Settings | None,
    client: object | None,
    request_id: str | None,
) -> dict[str, object]:
    """Run the retrieval tool step."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="retrieve", status="started")
    retrieval_query = RetrievalQuery(
        query=typed_state.user_query,
        top_k=(settings.top_k if settings is not None else 5),
    )
    retrieval_tool_result = document_retrieval_tool(
        retrieval_query,
        settings=settings,
        client=client,
        request_id=request_id,
    )
    retrieval_result = unwrap_retrieval_tool_result(retrieval_tool_result)
    emit_transition(
        request_id=request_id,
        step="retrieve",
        status="succeeded",
        result_count=len(retrieval_result.chunks),
    )
    return {
        "retrieved_chunks": retrieval_result.chunks,
        "trace_summary": append_trace(typed_state, f"retrieval:{len(retrieval_result.chunks)}"),
    }


def extract_clauses_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the clause extraction tool step."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="extract_clauses", status="started")
    tool_result = clause_extraction_tool(
        typed_state.retrieved_chunks,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Clause extraction failed."
        )
    emit_transition(
        request_id=request_id,
        step="extract_clauses",
        status="succeeded",
        result_count=len(tool_result.result.clauses),
    )
    return {
        "extracted_clauses": tool_result.result.clauses,
        "trace_summary": append_trace(
            typed_state,
            f"clause_extraction:{len(tool_result.result.clauses)}",
        ),
    }


def compare_policies_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the policy comparison tool step."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="compare", status="started")
    tool_result = policy_comparison_tool(
        typed_state.extracted_clauses,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Policy comparison failed."
        )
    emit_transition(
        request_id=request_id,
        step="compare",
        status="succeeded",
        sufficient_information=tool_result.result.sufficient_information,
    )
    return {
        "comparison_result": tool_result.result,
        "trace_summary": append_trace(typed_state, "comparison_completed"),
    }


def draft_initial_response_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the initial drafting step without verification input."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="draft_initial", status="started")
    documentary_basis = build_documentary_basis(typed_state.retrieved_chunks)
    citations = build_citations_from_chunks(typed_state.retrieved_chunks)
    tool_result = response_draft_tool(
        typed_state.user_query,
        documentary_basis,
        citations,
        comparison_result=typed_state.comparison_result,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Initial drafting failed."
        )
    emit_transition(
        request_id=request_id,
        step="draft_initial",
        status="succeeded",
        confidence=tool_result.result.confidence,
    )
    return {
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "trace_summary": append_trace(typed_state, "initial_draft_completed"),
    }


def verify_citations_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the citation verification tool step."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="verify_citations", status="started")
    tool_result = citation_verifier_tool(
        typed_state.draft_answer or "",
        typed_state.citations,
        typed_state.retrieved_chunks,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Citation verification failed."
        )
    emit_transition(
        request_id=request_id,
        step="verify_citations",
        status="succeeded",
        supported=tool_result.result.verification.supported,
        confidence=tool_result.result.verification.confidence,
    )
    return {
        "verification": tool_result.result.verification,
        "trace_summary": append_trace(typed_state, "citation_verification_completed"),
    }


def finalize_response_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the final drafting step with verification input."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="draft_final", status="started")
    documentary_basis = build_documentary_basis(typed_state.retrieved_chunks)
    tool_result = response_draft_tool(
        typed_state.user_query,
        documentary_basis,
        typed_state.citations,
        verification=typed_state.verification,
        comparison_result=typed_state.comparison_result,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        raise RuntimeError(
            tool_result.error.message
            if tool_result.error
            else "Final drafting failed."
        )
    emit_transition(
        request_id=request_id,
        step="draft_final",
        status="succeeded",
        confidence=tool_result.result.confidence,
        limitation_count=len(tool_result.result.limitations),
    )
    return {
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "final_answer": tool_result.result.suggested_answer,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "requires_human_review": True,
        "trace_summary": append_trace(typed_state, "workflow_completed"),
    }


def run_linear_workflow_steps(
    state: AgentState,
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
) -> AgentState:
    """Execute the fixed linear workflow path over existing tools."""

    current_state = state.model_copy(deep=True)
    for step_runner in (
        lambda s: retrieve_step(s, settings=settings, client=client, request_id=request_id),
        lambda s: extract_clauses_step(s, request_id=request_id),
        lambda s: compare_policies_step(s, request_id=request_id),
        lambda s: draft_initial_response_step(s, request_id=request_id),
        lambda s: verify_citations_step(s, request_id=request_id),
        lambda s: finalize_response_step(s, request_id=request_id),
    ):
        current_state = current_state.model_copy(
            update=step_runner(current_state),
            deep=True,
        )
    return current_state


def run_planned_workflow_steps(
    state: AgentState,
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
) -> AgentState:
    """Execute the planner step and then the selected narrow route."""

    current_state = state.model_copy(deep=True)
    current_state = current_state.model_copy(
        update=planner_step(current_state, request_id=request_id),
        deep=True,
    )
    if current_state.planner_route == "unsupported":
        return current_state.model_copy(
            update=unsupported_route_step(current_state, request_id=request_id),
            deep=True,
        )
    return run_linear_workflow_steps(
        current_state,
        settings=settings,
        client=client,
        request_id=request_id,
    )


def build_linear_workflow_graph(
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
) -> object:
    """Compile the first LangGraph workflow over the existing tool seams."""

    if not langgraph_backend_is_available():
        raise RuntimeError("LangGraph backend is not installed or unavailable.")

    from langgraph.graph import END, StateGraph

    workflow = StateGraph(AgentState)
    workflow.add_node(
        "planner",
        lambda state: planner_step(state, request_id=request_id),
    )
    workflow.add_node(
        "retrieve",
        lambda state: retrieve_step(
            state,
            settings=settings,
            client=client,
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "extract_clauses",
        lambda state: extract_clauses_step(state, request_id=request_id),
    )
    workflow.add_node(
        "compare",
        lambda state: compare_policies_step(state, request_id=request_id),
    )
    workflow.add_node(
        "draft_initial",
        lambda state: draft_initial_response_step(state, request_id=request_id),
    )
    workflow.add_node(
        "verify_citations",
        lambda state: verify_citations_step(state, request_id=request_id),
    )
    workflow.add_node(
        "draft_final",
        lambda state: finalize_response_step(state, request_id=request_id),
    )
    workflow.add_node(
        "unsupported_route",
        lambda state: unsupported_route_step(state, request_id=request_id),
    )
    workflow.set_entry_point("planner")
    workflow.add_conditional_edges(
        "planner",
        lambda state: ensure_agent_state(state).planner_route or "unsupported",
        {
            "grounded_qa": "retrieve",
            "unsupported": "unsupported_route",
        },
    )
    workflow.add_edge("retrieve", "extract_clauses")
    workflow.add_edge("extract_clauses", "compare")
    workflow.add_edge("compare", "draft_initial")
    workflow.add_edge("draft_initial", "verify_citations")
    workflow.add_edge("verify_citations", "draft_final")
    workflow.add_edge("draft_final", END)
    workflow.add_edge("unsupported_route", END)
    return workflow.compile()


def langgraph_linear_workflow(
    user_query: str,
    *,
    settings: Settings | None = None,
    client: object | None = None,
    request_id: str | None = None,
    compiled_graph: object | None = None,
) -> LangGraphWorkflowToolResult:
    """Execute the first linear LangGraph workflow over existing tools."""

    try:
        with log_timed_event(
            WORKFLOW_LOGGER,
            event_type="langgraph_linear_workflow",
            request_id=request_id,
            start_fields={"has_compiled_graph": compiled_graph is not None},
            success_fields_factory=lambda _duration_ms: {
                "confidence": final_state.confidence,
                "trace_count": len(final_state.trace_summary),
            },
        ):
            validate_workflow_input(user_query)
            initial_state = build_initial_workflow_state(user_query)
            graph = compiled_graph or build_linear_workflow_graph(
                settings=settings,
                client=client,
                request_id=request_id,
            )
            final_state_payload = graph.invoke(initial_state)
            final_state = ensure_agent_state(final_state_payload)
            if final_state.draft_response is None:
                raise RuntimeError("Workflow completed without a final draft response.")
            return LangGraphWorkflowToolResult(
                ok=True,
                result=WorkflowExecutionResult(
                    state=final_state,
                    response=final_state.draft_response,
                ),
            )
    except Exception as exc:
        return LangGraphWorkflowToolResult(
            ok=False,
            error=classify_langgraph_workflow_error(exc),
        )
