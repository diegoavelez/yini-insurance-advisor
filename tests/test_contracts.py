from __future__ import annotations

import pytest
from pydantic import ValidationError

from contracts import (
    AdvisorDraftResponse,
    AgentState,
    Citation,
    Clause,
    ClauseExtractionResult,
    ComparisonItem,
    DocumentaryBasisItem,
    DocumentFilters,
    DocumentRetrievalResult,
    GroundingVerification,
    GroundingVerificationResult,
    PolicyComparisonResult,
    RetrievalQuery,
    RetrievedChunk,
)


def test_retrieved_chunk_contract_is_valid() -> None:
    chunk = RetrievedChunk(
        chunk_id="chunk-1",
        text="Policy coverage text.",
        document_name="policy-a",
        page=4,
        section="Coverage",
        clause_id="1.2",
        score=0.91,
    )

    assert chunk.document_name == "policy-a"
    assert chunk.page == 4


def test_invalid_clause_category_fails() -> None:
    with pytest.raises(ValidationError):
        Clause(
            category="benefit",
            summary="Invalid category",
            document_name="policy-a",
        )


def test_valid_clause_category_is_accepted() -> None:
    clause = Clause(
        category="coverage",
        summary="Hospitalization is covered.",
        document_name="policy-a",
        page=2,
        section="Benefits",
        clause_id="2.1",
    )

    assert clause.category == "coverage"
    assert clause.page == 2


def test_document_filters_accept_optional_metadata() -> None:
    filters = DocumentFilters(
        document_type="policy",
        product="health",
        document_name="policy-a",
        version="2026-01",
    )

    assert filters.product == "health"
    assert filters.version == "2026-01"


def test_retrieval_query_top_k_bounds_are_enforced() -> None:
    with pytest.raises(ValidationError):
        RetrievalQuery(query="coverage", top_k=0)


def test_document_retrieval_result_wraps_chunks() -> None:
    result = DocumentRetrievalResult(
        chunks=[
            RetrievedChunk(
                chunk_id="chunk-1",
                text="Policy coverage text.",
                document_name="policy-a",
                page=4,
                section="Coverage",
                clause_id="1.2",
                score=0.91,
            )
        ]
    )

    assert result.chunks[0].chunk_id == "chunk-1"


def test_clause_extraction_result_wraps_clauses() -> None:
    result = ClauseExtractionResult(
        clauses=[
            Clause(
                category="restriction",
                summary="Applies only to approved clinics.",
                document_name="policy-a",
                section="Restrictions",
            )
        ]
    )

    assert result.clauses[0].category == "restriction"


def test_policy_comparison_can_represent_insufficient_information() -> None:
    comparison = PolicyComparisonResult(
        sufficient_information=False,
        notes=["Not enough evidence to compare the two policies."],
    )

    assert comparison.sufficient_information is False
    assert comparison.notes


def test_policy_comparison_supports_typed_citations() -> None:
    comparison = PolicyComparisonResult(
        comparison_points=[
            ComparisonItem(
                criterion="hospitalization coverage",
                finding="Policy A covers private room upgrades; Policy B does not.",
                source_documents=["policy-a", "policy-b"],
                citations=[
                    Citation(document_name="policy-a", page=4, section="Coverage", clause_id="1.2"),
                    Citation(
                        document_name="policy-b",
                        page=7,
                        section="Exclusions",
                        clause_id="3.4",
                    ),
                ],
            )
        ]
    )

    assert comparison.comparison_points[0].citations[0].document_name == "policy-a"


def test_advisor_response_contract_matches_prd_shape() -> None:
    response = AdvisorDraftResponse(
        suggested_answer="Coverage applies with listed exclusions.",
        documentary_basis=[
            DocumentaryBasisItem(
                document_name="policy-a",
                page=4,
                section="Coverage",
                clause_id="1.2",
            )
        ],
        citations=[Citation(document_name="policy-a", page=4, section="Coverage", clause_id="1.2")],
        confidence="high",
        limitations=["Does not include claim adjudication guidance."],
        advisor_review_notice="This response is a draft for advisor review.",
    )

    assert response.confidence == "high"
    assert response.citations[0].document_name == "policy-a"


def test_invalid_confidence_fails_in_grounding_verification() -> None:
    with pytest.raises(ValidationError):
        GroundingVerification(supported=True, confidence="certain")


def test_grounding_verification_result_wraps_verification() -> None:
    result = GroundingVerificationResult(
        verification=GroundingVerification(
            supported=True,
            confidence="high",
        )
    )

    assert result.verification.confidence == "high"


def test_citation_preserves_traceability_fields() -> None:
    citation = Citation(
        document_name="policy-a",
        page=4,
        section="Coverage",
        clause_id="1.2",
        quote="Hospitalization expenses are covered.",
    )

    assert citation.page == 4
    assert citation.section == "Coverage"
    assert citation.clause_id == "1.2"


def test_agent_state_is_typed_and_constructible() -> None:
    chunk = RetrievedChunk(
        chunk_id="chunk-1",
        text="Policy coverage text.",
        document_name="policy-a",
        page=4,
        section="Coverage",
        clause_id="1.2",
        score=0.91,
    )
    clause = Clause(
        category="coverage",
        summary="Coverage applies for the listed event.",
        document_name="policy-a",
        page=4,
        section="Coverage",
        clause_id="1.2",
        supporting_chunk_ids=["chunk-1"],
    )
    comparison = PolicyComparisonResult(
        comparison_points=[
            ComparisonItem(
                criterion="hospitalization coverage",
                finding="Policy A covers the event.",
                source_documents=["policy-a"],
                citations=[
                    Citation(
                        document_name="policy-a",
                        page=4,
                        section="Coverage",
                        clause_id="1.2",
                    )
                ],
            )
        ]
    )

    state = AgentState(
        user_query="Does this policy cover hospitalization?",
        query_type="coverage_lookup",
        plan=["retrieve", "analyze", "format"],
        retrieved_chunks=[chunk],
        extracted_clauses=[clause],
        comparison_result=comparison,
        draft_answer="Coverage appears applicable.",
        citations=[Citation(document_name="policy-a", page=4, section="Coverage", clause_id="1.2")],
        verification=GroundingVerification(supported=True, confidence="medium"),
        final_answer="Coverage appears applicable.",
        confidence="medium",
        trace_summary=["intent detected", "retrieval completed"],
    )

    assert state.retrieved_chunks[0].chunk_id == "chunk-1"
    assert state.extracted_clauses[0].category == "coverage"
    assert state.comparison_result is not None
    assert state.draft_answer == "Coverage appears applicable."


def test_agent_state_invalid_confidence_fails() -> None:
    with pytest.raises(ValidationError):
        AgentState(user_query="question", confidence="certain")
