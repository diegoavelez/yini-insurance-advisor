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
from core.query_scope import classify_query_scope
from ops.observability import log_event, log_timed_event
from rag.ingestion import build_citations_from_chunks, build_documentary_basis

WORKFLOW_LOGGER = logging.getLogger("yini.workflow.langgraph")
MAX_WORKFLOW_RETRY_ATTEMPTS = 2
RETRYABLE_WORKFLOW_STEPS = {"retrieve", "citation_verifier"}


class WorkflowStepError(RuntimeError):
    """Internal typed workflow-step failure."""

    def __init__(
        self,
        stage: str,
        message: str,
        *,
        retryable: bool,
        failure_kind: str,
    ) -> None:
        super().__init__(message)
        self.stage = stage
        self.retryable = retryable
        self.failure_kind = failure_kind


class WorkflowRetryExhaustedError(RuntimeError):
    """Internal terminal failure after bounded retry exhaustion."""

    def __init__(self, stage: str, last_error: WorkflowStepError) -> None:
        super().__init__(str(last_error))
        self.stage = stage
        self.last_error = last_error


def langgraph_backend_is_available() -> bool:
    """Return whether the LangGraph backend is importable."""

    return importlib.util.find_spec("langgraph") is not None


def classify_langgraph_workflow_error(exc: Exception) -> ToolError:
    """Map workflow failures into the typed error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    if isinstance(exc, WorkflowRetryExhaustedError):
        return ToolError(
            kind="retry_exhausted_failure",
            message=f"{exc.stage} exhausted bounded retry attempts: {exc.last_error}",
        )
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
            "policy_analyst",
            "citation_verifier",
            "response_drafter",
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

    scope_decision = classify_query_scope(user_query)
    if scope_decision.scope == "supported":
        return PlannerDecision(
            route="grounded_qa",
            reason=scope_decision.reason,
        )
    return PlannerDecision(
        route="unsupported",
        reason=scope_decision.reason,
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


def emit_fallback_selected(
    *,
    request_id: str | None,
    fallback_stage: str,
    fallback_reason: str,
) -> None:
    """Emit one structured insufficient-evidence fallback event."""

    log_event(
        WORKFLOW_LOGGER,
        event_type="workflow_insufficient_evidence_fallback_selected",
        request_id=request_id,
        fallback_stage=fallback_stage,
        fallback_reason=fallback_reason,
    )


def emit_retry_attempt(
    *,
    request_id: str | None,
    workflow_step: str,
    attempt_number: int,
    max_attempts: int,
    error_message: str,
) -> None:
    """Emit one structured retry-attempt event."""

    log_event(
        WORKFLOW_LOGGER,
        event_type="workflow_retry_attempt",
        request_id=request_id,
        workflow_step=workflow_step,
        attempt_number=attempt_number,
        max_attempts=max_attempts,
        error_message=error_message,
    )


def emit_retry_exhausted(
    *,
    request_id: str | None,
    workflow_step: str,
    attempts_used: int,
    error_message: str,
) -> None:
    """Emit one structured retry-exhausted event."""

    log_event(
        WORKFLOW_LOGGER,
        event_type="workflow_retry_exhausted",
        request_id=request_id,
        workflow_step=workflow_step,
        attempts_used=attempts_used,
        error_message=error_message,
    )


def classify_retryable_failure_kind(error_kind: str) -> bool:
    """Return whether one tool failure kind is eligible for bounded retry."""

    return error_kind in {"dependency_failure", "backend_failure"}


def execute_workflow_step_with_retry(
    state: AgentState,
    *,
    step_name: str,
    step_runner: Any,
    request_id: str | None,
) -> AgentState:
    """Execute one workflow step with bounded retry when the boundary allows it."""

    current_state = state.model_copy(deep=True)
    max_attempts = (
        MAX_WORKFLOW_RETRY_ATTEMPTS if step_name in RETRYABLE_WORKFLOW_STEPS else 1
    )
    attempt_number = 1
    while True:
        try:
            return current_state.model_copy(
                update=step_runner(current_state),
                deep=True,
            )
        except WorkflowStepError as exc:
            if not exc.retryable or attempt_number >= max_attempts:
                if exc.retryable and step_name in RETRYABLE_WORKFLOW_STEPS:
                    emit_retry_exhausted(
                        request_id=request_id,
                        workflow_step=step_name,
                        attempts_used=attempt_number,
                        error_message=str(exc),
                    )
                    raise WorkflowRetryExhaustedError(step_name, exc) from exc
                raise
            emit_retry_attempt(
                request_id=request_id,
                workflow_step=step_name,
                attempt_number=attempt_number,
                max_attempts=max_attempts,
                error_message=str(exc),
            )
            current_state = current_state.model_copy(
                update={
                    "retry_attempts": [
                        *current_state.retry_attempts,
                        f"{step_name}:attempt_{attempt_number}",
                    ],
                    "trace_summary": append_trace(
                        current_state,
                        f"retry:{step_name}:{attempt_number}",
                    ),
                },
                deep=True,
            )
            attempt_number += 1


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


def determine_post_compare_route(state: AgentState | dict[str, Any]) -> str:
    """Return the next route after comparison."""

    typed_state = ensure_agent_state(state)
    if typed_state.comparison_result is None:
        return "insufficient_evidence_fallback"
    if not typed_state.comparison_result.sufficient_information:
        return "insufficient_evidence_fallback"
    return "policy_analyst"


def determine_post_verifier_route(state: AgentState | dict[str, Any]) -> str:
    """Return the next route after citation verification."""

    typed_state = ensure_agent_state(state)
    if typed_state.verification is None:
        return "insufficient_evidence_fallback"
    if not typed_state.verification.supported:
        return "insufficient_evidence_fallback"
    return "response_drafter"


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
    try:
        retrieval_result = unwrap_retrieval_tool_result(retrieval_tool_result)
    except Exception as exc:
        error_kind = (
            retrieval_tool_result.error.kind
            if retrieval_tool_result.error is not None
            else "backend_failure"
        )
        raise WorkflowStepError(
            "retrieve",
            str(exc),
            retryable=classify_retryable_failure_kind(error_kind),
            failure_kind=error_kind,
        ) from exc
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
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "extraction_failure"
        )
        raise WorkflowStepError(
            "extract_clauses",
            (
                tool_result.error.message
                if tool_result.error
                else "Clause extraction failed."
            ),
            retryable=False,
            failure_kind=error_kind,
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
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "comparison_failure"
        )
        raise WorkflowStepError(
            "compare",
            (
                tool_result.error.message
                if tool_result.error
                else "Policy comparison failed."
            ),
            retryable=False,
            failure_kind=error_kind,
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


def build_analyst_summary(state: AgentState) -> str:
    """Build one compact analyst-stage summary from comparison output."""

    if state.comparison_result is None:
        return "No policy comparison result was available."
    if state.comparison_result.comparison_points:
        return " ".join(
            comparison_point.finding
            for comparison_point in state.comparison_result.comparison_points
        )
    if state.comparison_result.notes:
        return " ".join(state.comparison_result.notes)
    return "Policy analyst pass did not produce a comparison finding."


def policy_analyst_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the explicit analyst pass over comparison and preliminary drafting."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="policy_analyst", status="started")
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
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "drafting_failure"
        )
        raise WorkflowStepError(
            "policy_analyst",
            (
                tool_result.error.message
                if tool_result.error
                else "Policy analyst drafting failed."
            ),
            retryable=False,
            failure_kind=error_kind,
        )
    analyst_summary = build_analyst_summary(typed_state)
    emit_transition(
        request_id=request_id,
        step="policy_analyst",
        status="succeeded",
        confidence=tool_result.result.confidence,
        sufficient_information=(
            typed_state.comparison_result.sufficient_information
            if typed_state.comparison_result is not None
            else False
        ),
    )
    return {
        "documentary_basis": documentary_basis,
        "analyst_summary": analyst_summary,
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "trace_summary": append_trace(typed_state, "policy_analyst_completed"),
    }


def verify_citations_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the citation verification tool step."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="citation_verifier", status="started")
    tool_result = citation_verifier_tool(
        typed_state.draft_answer or "",
        typed_state.citations,
        typed_state.retrieved_chunks,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "verification_failure"
        )
        raise WorkflowStepError(
            "citation_verifier",
            (
                tool_result.error.message
                if tool_result.error
                else "Citation verification failed."
            ),
            retryable=classify_retryable_failure_kind(error_kind),
            failure_kind=error_kind,
        )
    emit_transition(
        request_id=request_id,
        step="citation_verifier",
        status="succeeded",
        supported=tool_result.result.verification.supported,
        confidence=tool_result.result.verification.confidence,
    )
    return {
        "verification": tool_result.result.verification,
        "reviewed_citations": tool_result.result.reviewed_citations,
        "verifier_notes": tool_result.result.notes,
        "trace_summary": append_trace(typed_state, "citation_verifier_completed"),
    }


def response_drafter_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Run the explicit final drafting pass with verification input."""

    typed_state = ensure_agent_state(state)
    emit_transition(request_id=request_id, step="response_drafter", status="started")
    documentary_basis = typed_state.documentary_basis or build_documentary_basis(
        typed_state.retrieved_chunks
    )
    tool_result = response_draft_tool(
        typed_state.user_query,
        documentary_basis,
        typed_state.citations,
        verification=typed_state.verification,
        comparison_result=typed_state.comparison_result,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "drafting_failure"
        )
        raise WorkflowStepError(
            "response_drafter",
            (
                tool_result.error.message
                if tool_result.error
                else "Final drafting failed."
            ),
            retryable=False,
            failure_kind=error_kind,
        )
    emit_transition(
        request_id=request_id,
        step="response_drafter",
        status="succeeded",
        confidence=tool_result.result.confidence,
        limitation_count=len(tool_result.result.limitations),
    )
    return {
        "documentary_basis": documentary_basis,
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "final_answer": tool_result.result.suggested_answer,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "requires_human_review": True,
        "trace_summary": append_trace(typed_state, "response_drafter_completed"),
    }


def insufficient_evidence_fallback_step(
    state: AgentState | dict[str, Any],
    *,
    request_id: str | None,
) -> dict[str, object]:
    """Return a conservative non-error workflow outcome for insufficient evidence."""

    typed_state = ensure_agent_state(state)
    fallback_stage = "compare"
    fallback_reason = "Comparison evidence is insufficient for a strong workflow conclusion."
    verification = typed_state.verification

    if typed_state.verification is not None and not typed_state.verification.supported:
        fallback_stage = "citation_verifier"
        fallback_reason = (
            "Citation verification did not confirm enough evidence for a strong workflow result."
        )
    elif (
        typed_state.comparison_result is None
        or not typed_state.comparison_result.sufficient_information
    ):
        verification = GroundingVerification(
            supported=False,
            confidence="low",
            unsupported_claims=[fallback_reason],
            missing_citations=(
                []
                if typed_state.citations
                else ["No citations were available for fallback support."]
            ),
        )

    emit_transition(
        request_id=request_id,
        step="insufficient_evidence_fallback",
        status="started",
        fallback_stage=fallback_stage,
    )
    emit_fallback_selected(
        request_id=request_id,
        fallback_stage=fallback_stage,
        fallback_reason=fallback_reason,
    )
    documentary_basis = typed_state.documentary_basis or build_documentary_basis(
        typed_state.retrieved_chunks
    )
    citations = typed_state.citations or build_citations_from_chunks(typed_state.retrieved_chunks)
    tool_result = response_draft_tool(
        typed_state.user_query,
        documentary_basis,
        citations,
        verification=verification,
        comparison_result=typed_state.comparison_result,
        request_id=request_id,
    )
    if not tool_result.ok or tool_result.result is None:
        error_kind = (
            tool_result.error.kind if tool_result.error is not None else "drafting_failure"
        )
        raise WorkflowStepError(
            "insufficient_evidence_fallback",
            (
                tool_result.error.message
                if tool_result.error
                else "Insufficient-evidence fallback drafting failed."
            ),
            retryable=False,
            failure_kind=error_kind,
        )
    emit_transition(
        request_id=request_id,
        step="insufficient_evidence_fallback",
        status="succeeded",
        confidence=tool_result.result.confidence,
        fallback_stage=fallback_stage,
    )
    return {
        "documentary_basis": documentary_basis,
        "draft_response": tool_result.result,
        "draft_answer": tool_result.result.suggested_answer,
        "final_answer": tool_result.result.suggested_answer,
        "verification": verification,
        "citations": tool_result.result.citations,
        "confidence": tool_result.result.confidence,
        "requires_human_review": True,
        "fallback_stage": fallback_stage,
        "fallback_reason": fallback_reason,
        "trace_summary": append_trace(
            typed_state,
            f"insufficient_evidence_fallback:{fallback_stage}",
        ),
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
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="retrieve",
        step_runner=lambda s: retrieve_step(
            s,
            settings=settings,
            client=client,
            request_id=request_id,
        ),
        request_id=request_id,
    )
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="extract_clauses",
        step_runner=lambda s: extract_clauses_step(s, request_id=request_id),
        request_id=request_id,
    )
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="compare",
        step_runner=lambda s: compare_policies_step(s, request_id=request_id),
        request_id=request_id,
    )
    if determine_post_compare_route(current_state) == "insufficient_evidence_fallback":
        current_state = current_state.model_copy(
            update=insufficient_evidence_fallback_step(
                current_state,
                request_id=request_id,
            ),
            deep=True,
        )
        return current_state.model_copy(
            update={"trace_summary": append_trace(current_state, "workflow_completed")},
            deep=True,
        )
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="policy_analyst",
        step_runner=lambda s: policy_analyst_step(s, request_id=request_id),
        request_id=request_id,
    )
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="citation_verifier",
        step_runner=lambda s: verify_citations_step(s, request_id=request_id),
        request_id=request_id,
    )
    if determine_post_verifier_route(current_state) == "insufficient_evidence_fallback":
        current_state = current_state.model_copy(
            update=insufficient_evidence_fallback_step(
                current_state,
                request_id=request_id,
            ),
            deep=True,
        )
        return current_state.model_copy(
            update={"trace_summary": append_trace(current_state, "workflow_completed")},
            deep=True,
        )
    current_state = execute_workflow_step_with_retry(
        current_state,
        step_name="response_drafter",
        step_runner=lambda s: response_drafter_step(s, request_id=request_id),
        request_id=request_id,
    )
    return current_state.model_copy(
        update={"trace_summary": append_trace(current_state, "workflow_completed")},
        deep=True,
    )


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
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="retrieve",
            step_runner=lambda s: retrieve_step(
                s,
                settings=settings,
                client=client,
                request_id=request_id,
            ),
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "extract_clauses",
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="extract_clauses",
            step_runner=lambda s: extract_clauses_step(s, request_id=request_id),
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "compare",
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="compare",
            step_runner=lambda s: compare_policies_step(s, request_id=request_id),
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "policy_analyst",
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="policy_analyst",
            step_runner=lambda s: policy_analyst_step(s, request_id=request_id),
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "insufficient_evidence_fallback",
        lambda state: insufficient_evidence_fallback_step(state, request_id=request_id),
    )
    workflow.add_node(
        "citation_verifier",
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="citation_verifier",
            step_runner=lambda s: verify_citations_step(s, request_id=request_id),
            request_id=request_id,
        ),
    )
    workflow.add_node(
        "response_drafter",
        lambda state: execute_workflow_step_with_retry(
            ensure_agent_state(state),
            step_name="response_drafter",
            step_runner=lambda s: response_drafter_step(s, request_id=request_id),
            request_id=request_id,
        ),
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
    workflow.add_conditional_edges(
        "compare",
        determine_post_compare_route,
        {
            "policy_analyst": "policy_analyst",
            "insufficient_evidence_fallback": "insufficient_evidence_fallback",
        },
    )
    workflow.add_edge("policy_analyst", "citation_verifier")
    workflow.add_conditional_edges(
        "citation_verifier",
        determine_post_verifier_route,
        {
            "response_drafter": "response_drafter",
            "insufficient_evidence_fallback": "insufficient_evidence_fallback",
        },
    )
    workflow.add_edge("response_drafter", END)
    workflow.add_edge("insufficient_evidence_fallback", END)
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
