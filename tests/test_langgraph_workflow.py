from __future__ import annotations

import logging
import sys
import types

from agents.langgraph_workflow import (
    build_initial_workflow_state,
    build_linear_workflow_graph,
    classify_langgraph_workflow_error,
    classify_planner_route,
    langgraph_linear_workflow,
    run_planned_workflow_steps,
)
from contracts import (
    CitationVerifierToolResult,
    DocumentRetrievalResult,
    DocumentRetrievalToolResult,
    GroundingVerification,
    GroundingVerificationResult,
    RetrievedChunk,
)


def make_chunk(
    *,
    chunk_id: str = "policy-a:v2:0000",
    text: str = "Coverage applies for listed hospitalization emergencies.",
    document_name: str = "Policy A",
    page: int = 4,
    section: str = "Coverage",
    clause_id: str = "1.2",
    score: float = 0.91,
) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=chunk_id,
        text=text,
        document_name=document_name,
        page=page,
        section=section,
        clause_id=clause_id,
        score=score,
    )


def make_comparable_chunks() -> list[RetrievedChunk]:
    return [
        make_chunk(
            chunk_id="policy-a:v2:0000",
            document_name="Policy A",
            text="Coverage applies for listed hospitalization emergencies.",
        ),
        make_chunk(
            chunk_id="policy-b:v2:0001",
            document_name="Policy B",
            text="Coverage applies for listed hospitalization emergencies.",
        ),
    ]


class FakeCompiledGraph:
    def __init__(self, invoker):
        self._invoker = invoker

    def invoke(self, state):
        return self._invoker(state)


def test_langgraph_linear_workflow_returns_typed_success(monkeypatch) -> None:
    import agents.langgraph_workflow as workflow_module

    def fake_retrieval_tool(*_args, **_kwargs):
        return DocumentRetrievalToolResult(
            ok=True,
            result=DocumentRetrievalResult(chunks=make_comparable_chunks()),
        )

    monkeypatch.setattr(workflow_module, "document_retrieval_tool", fake_retrieval_tool)
    compiled_graph = FakeCompiledGraph(
        lambda state: run_planned_workflow_steps(state, request_id="wf-123456789012")
    )

    result = langgraph_linear_workflow(
        "What coverage applies?",
        request_id="wf-123456789012",
        compiled_graph=compiled_graph,
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.response.suggested_answer
    assert result.result.state.final_answer == result.result.response.suggested_answer
    assert result.result.state.trace_summary == [
        "workflow_initialized",
        "planner:grounded_qa",
        "retrieval:2",
        "clause_extraction:2",
        "comparison_completed",
        "policy_analyst_completed",
        "citation_verifier_completed",
        "response_drafter_completed",
        "workflow_completed",
    ]
    assert result.result.state.analyst_summary
    assert result.result.state.documentary_basis
    assert result.result.state.reviewed_citations


def test_langgraph_linear_workflow_returns_valid_insufficient_information(monkeypatch) -> None:
    import agents.langgraph_workflow as workflow_module

    def fake_retrieval_tool(*_args, **_kwargs):
        return DocumentRetrievalToolResult(
            ok=True,
            result=DocumentRetrievalResult(chunks=[]),
        )

    monkeypatch.setattr(workflow_module, "document_retrieval_tool", fake_retrieval_tool)
    compiled_graph = FakeCompiledGraph(lambda state: run_planned_workflow_steps(state))

    result = langgraph_linear_workflow(
        "Compare policy coverage for hospitalization.",
        compiled_graph=compiled_graph,
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.response.confidence == "low"
    assert result.result.state.verification is not None
    assert result.result.state.verification.supported is False
    assert result.result.state.fallback_stage == "compare"
    assert "insufficient_evidence_fallback:compare" in result.result.state.trace_summary


def test_langgraph_linear_workflow_returns_valid_verifier_fallback(monkeypatch) -> None:
    import agents.langgraph_workflow as workflow_module

    def fake_retrieval_tool(*_args, **_kwargs):
        return DocumentRetrievalToolResult(
            ok=True,
            result=DocumentRetrievalResult(chunks=make_comparable_chunks()),
        )

    def fake_citation_verifier_tool(*_args, **_kwargs):
        return CitationVerifierToolResult(
            ok=True,
            result=GroundingVerificationResult(
                verification=GroundingVerification(
                    supported=False,
                    confidence="low",
                    unsupported_claims=["Citations did not support the draft."],
                    missing_citations=[],
                ),
                reviewed_citations=[],
                notes=["Verifier fallback triggered."],
            ),
        )

    monkeypatch.setattr(workflow_module, "document_retrieval_tool", fake_retrieval_tool)
    monkeypatch.setattr(
        workflow_module,
        "citation_verifier_tool",
        fake_citation_verifier_tool,
    )
    compiled_graph = FakeCompiledGraph(
        lambda state: run_planned_workflow_steps(state, request_id="wf-123456789012")
    )

    result = langgraph_linear_workflow(
        "What coverage applies?",
        request_id="wf-123456789012",
        compiled_graph=compiled_graph,
    )

    assert result.ok is True
    assert result.result is not None
    assert result.result.state.fallback_stage == "citation_verifier"
    assert "insufficient_evidence_fallback:citation_verifier" in result.result.state.trace_summary


def test_langgraph_linear_workflow_returns_typed_input_validation_failure() -> None:
    result = langgraph_linear_workflow("", compiled_graph=FakeCompiledGraph(lambda state: state))

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "input_validation_failure"


def test_langgraph_linear_workflow_returns_dependency_failure_without_backend(monkeypatch) -> None:
    import agents.langgraph_workflow as workflow_module

    monkeypatch.setattr(workflow_module, "langgraph_backend_is_available", lambda: False)

    result = langgraph_linear_workflow("What coverage applies?")

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "dependency_failure"


def test_langgraph_linear_workflow_failure_remains_observable(caplog) -> None:
    caplog.set_level(logging.INFO)

    compiled_graph = FakeCompiledGraph(
        lambda _state: (_ for _ in ()).throw(RuntimeError("workflow exploded"))
    )
    result = langgraph_linear_workflow(
        "What coverage applies?",
        request_id="wf-123456789012",
        compiled_graph=compiled_graph,
    )

    assert result.ok is False
    assert result.error is not None
    assert result.error.kind == "workflow_failure"
    failed = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "langgraph_linear_workflow_failed"
    )
    assert failed.request_id == "wf-123456789012"


def test_langgraph_linear_workflow_preserves_state_transition_observability(
    monkeypatch,
    caplog,
) -> None:
    import agents.langgraph_workflow as workflow_module

    caplog.set_level(logging.INFO)

    def fake_retrieval_tool(*_args, **_kwargs):
        return DocumentRetrievalToolResult(
            ok=True,
            result=DocumentRetrievalResult(chunks=make_comparable_chunks()),
        )

    monkeypatch.setattr(workflow_module, "document_retrieval_tool", fake_retrieval_tool)
    compiled_graph = FakeCompiledGraph(
        lambda state: run_planned_workflow_steps(state, request_id="wf-123456789012")
    )

    result = langgraph_linear_workflow(
        "What coverage applies?",
        request_id="wf-123456789012",
        compiled_graph=compiled_graph,
    )

    assert result.ok is True
    transitions = [
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "workflow_state_transition"
    ]
    assert transitions
    assert any(record.workflow_step == "planner" for record in transitions)
    assert any(record.workflow_step == "retrieve" for record in transitions)
    assert any(record.workflow_step == "compare" for record in transitions)
    assert any(record.workflow_step == "policy_analyst" for record in transitions)
    assert any(record.workflow_step == "citation_verifier" for record in transitions)
    assert any(record.workflow_step == "response_drafter" for record in transitions)
    assert all(record.request_id == "wf-123456789012" for record in transitions)
    planner_event = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "") == "planner_route_selected"
    )
    assert planner_event.request_id == "wf-123456789012"
    assert planner_event.route == "grounded_qa"


def test_insufficient_evidence_fallback_emits_observable_event(monkeypatch, caplog) -> None:
    import agents.langgraph_workflow as workflow_module

    caplog.set_level(logging.INFO)

    def fake_retrieval_tool(*_args, **_kwargs):
        return DocumentRetrievalToolResult(
            ok=True,
            result=DocumentRetrievalResult(chunks=[]),
        )

    monkeypatch.setattr(workflow_module, "document_retrieval_tool", fake_retrieval_tool)
    compiled_graph = FakeCompiledGraph(
        lambda state: run_planned_workflow_steps(state, request_id="wf-123456789012")
    )

    result = langgraph_linear_workflow(
        "Compare policy coverage for hospitalization.",
        request_id="wf-123456789012",
        compiled_graph=compiled_graph,
    )

    assert result.ok is True
    fallback_event = next(
        record
        for record in caplog.records
        if getattr(record, "event_type", "")
        == "workflow_insufficient_evidence_fallback_selected"
    )
    assert fallback_event.request_id == "wf-123456789012"
    assert fallback_event.fallback_stage == "compare"


def test_build_linear_workflow_graph_wires_langgraph_stategraph(monkeypatch) -> None:
    import agents.langgraph_workflow as workflow_module

    captured: dict[str, object] = {}

    class FakeCompiledGraph:
        def invoke(self, state):
            return state

    class FakeStateGraph:
        def __init__(self, _state_type):
            captured["graph"] = self
            self.nodes = {}
            self.edges = []
            self.conditional_edges = []
            self.entry_point = None

        def add_node(self, name, fn):
            self.nodes[name] = fn

        def set_entry_point(self, name):
            self.entry_point = name

        def add_edge(self, left, right):
            self.edges.append((left, right))

        def add_conditional_edges(self, node, route_fn, mapping):
            self.conditional_edges.append((node, route_fn, mapping))

        def compile(self):
            return FakeCompiledGraph()

    fake_graph_module = types.ModuleType("langgraph.graph")
    fake_graph_module.StateGraph = FakeStateGraph
    fake_graph_module.END = "END"

    monkeypatch.setattr(workflow_module, "langgraph_backend_is_available", lambda: True)
    monkeypatch.setitem(sys.modules, "langgraph.graph", fake_graph_module)

    compiled = build_linear_workflow_graph(request_id="wf-123456789012")

    assert hasattr(compiled, "invoke")
    graph = captured["graph"]
    assert graph.entry_point == "planner"
    assert graph.conditional_edges
    node, _route_fn, mapping = graph.conditional_edges[0]
    assert node == "planner"
    assert mapping["grounded_qa"] == "retrieve"
    assert mapping["unsupported"] == "unsupported_route"
    assert ("extract_clauses", "compare") in graph.edges
    assert len(graph.conditional_edges) == 3
    compare_node, _compare_route_fn, compare_mapping = graph.conditional_edges[1]
    assert compare_node == "compare"
    assert compare_mapping["policy_analyst"] == "policy_analyst"
    assert compare_mapping["insufficient_evidence_fallback"] == "insufficient_evidence_fallback"
    assert ("policy_analyst", "citation_verifier") in graph.edges
    verifier_node, _verifier_route_fn, verifier_mapping = graph.conditional_edges[2]
    assert verifier_node == "citation_verifier"
    assert verifier_mapping["response_drafter"] == "response_drafter"
    assert verifier_mapping["insufficient_evidence_fallback"] == "insufficient_evidence_fallback"


def test_build_initial_workflow_state_sets_linear_plan() -> None:
    state = build_initial_workflow_state("What coverage applies?")

    assert state.plan == [
        "planner",
        "retrieve",
        "extract_clauses",
        "compare",
        "policy_analyst",
        "citation_verifier",
        "response_drafter",
    ]
    assert state.trace_summary == ["workflow_initialized"]


def test_classify_planner_route_returns_supported_route_for_insurance_query() -> None:
    decision = classify_planner_route("Compare policy coverage for hospitalization.")

    assert decision.route == "grounded_qa"
    assert decision.reason


def test_classify_planner_route_returns_unsupported_route_for_out_of_scope_query() -> None:
    decision = classify_planner_route("What is the weather in Bogota?")

    assert decision.route == "unsupported"
    assert decision.reason


def test_classify_langgraph_workflow_error_distinguishes_runtime_failure() -> None:
    error = classify_langgraph_workflow_error(RuntimeError("workflow failed"))

    assert error.kind == "workflow_failure"
