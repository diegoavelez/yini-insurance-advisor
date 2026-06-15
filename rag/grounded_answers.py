from __future__ import annotations

from contracts import (
    AdvisorDraftResponse,
    Citation,
    DocumentaryBasisItem,
    GroundedAnswerResult,
    GroundingVerification,
    RetrievedChunk,
)


def build_grounded_prompt(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
) -> str:
    """Build a deterministic grounded-answer prompt from retrieved evidence."""

    evidence_sections: list[str] = []
    for chunk in retrieved_chunks:
        evidence_sections.append(
            "\n".join(
                [
                    f"Chunk ID: {chunk.chunk_id}",
                    f"Document: {chunk.document_name}",
                    f"Section: {chunk.section or 'Unknown'}",
                    f"Text: {chunk.text}",
                ]
            )
        )

    evidence_block = "\n\n---\n\n".join(evidence_sections)
    return (
        "Answer the advisor's question using only the evidence below.\n"
        "If the evidence is insufficient, say that explicitly and do not invent details.\n\n"
        f"Question: {query}\n\n"
        f"Evidence:\n{evidence_block}"
    )


def build_citations_from_chunks(retrieved_chunks: list[RetrievedChunk]) -> list[Citation]:
    """Derive explicit citations from retrieved evidence."""

    citations: list[Citation] = []
    for chunk in retrieved_chunks:
        citations.append(
            Citation(
                document_name=chunk.document_name,
                source_pdf_relative_path=chunk.source_pdf_relative_path,
                document_type=chunk.document_type,
                product=chunk.product,
                chunk_id=chunk.chunk_id,
                page=chunk.page,
                section=chunk.section,
                clause_id=chunk.clause_id,
                quote=chunk.text[:280],
            )
        )
    return citations


def build_documentary_basis(retrieved_chunks: list[RetrievedChunk]) -> list[DocumentaryBasisItem]:
    """Map retrieved evidence into documentary basis items."""

    return [
        DocumentaryBasisItem(
            document_name=chunk.document_name,
            source_pdf_relative_path=chunk.source_pdf_relative_path,
            document_type=chunk.document_type,
            product=chunk.product,
            page=chunk.page,
            section=chunk.section,
            clause_id=chunk.clause_id,
            note=f"Derived from chunk {chunk.chunk_id}",
        )
        for chunk in retrieved_chunks
    ]


def assess_grounding(
    *,
    retrieved_chunks: list[RetrievedChunk],
    citations: list[Citation],
    min_retrieval_chunks_for_high_confidence: int,
) -> GroundingVerification:
    """Build a simple typed grounding assessment from evidence availability."""

    if not retrieved_chunks:
        return GroundingVerification(
            supported=False,
            confidence="low",
            unsupported_claims=["No retrieval evidence was available."],
            missing_citations=["No citations available because retrieval returned no chunks."],
        )

    if len(retrieved_chunks) >= min_retrieval_chunks_for_high_confidence and citations:
        return GroundingVerification(supported=True, confidence="high")

    return GroundingVerification(
        supported=True,
        confidence="medium",
        missing_citations=(
            [] if citations else ["No citations were derived from retrieved evidence."]
        ),
    )


def build_insufficient_evidence_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    limitation_note: str | None = None,
    advisor_review_notice: str,
    min_retrieval_chunks_for_high_confidence: int,
) -> GroundedAnswerResult:
    """Return a typed limited grounded response for insufficient evidence."""

    citations = build_citations_from_chunks(retrieved_chunks)
    verification = assess_grounding(
        retrieved_chunks=retrieved_chunks,
        citations=citations,
        min_retrieval_chunks_for_high_confidence=min_retrieval_chunks_for_high_confidence,
    )
    limitations = [
        limitation_note or "Retrieved evidence is insufficient for a strong grounded answer."
    ]
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I do not have enough grounded evidence in the retrieved documents to answer "
                "this confidently."
            ),
            documentary_basis=build_documentary_basis(retrieved_chunks),
            citations=citations,
            confidence="low",
            limitations=limitations,
            advisor_review_notice=advisor_review_notice,
        ),
        verification=verification,
    )


def build_unsupported_query_response(
    *,
    query: str,
    advisor_review_notice: str,
) -> GroundedAnswerResult:
    """Return a typed conservative refusal for out-of-scope queries."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            "The query is outside the supported insurance-document scope for this assistant."
        ],
        missing_citations=["No citations are available for an out-of-scope refusal outcome."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot answer that request within the supported insurance-document scope "
                "of this assistant."
            ),
            documentary_basis=[],
            citations=[],
            confidence="low",
            limitations=["This request is outside the supported insurance-document scope."],
            advisor_review_notice=advisor_review_notice,
        ),
        verification=verification,
    )


def build_prompt_injection_refusal_response(
    *,
    query: str,
    advisor_review_notice: str,
) -> GroundedAnswerResult:
    """Return a typed conservative refusal for prompt-injection-like queries."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            (
                "The query included instructions that conflict with the assistant's "
                "grounded-use boundaries."
            )
        ],
        missing_citations=["No citations are available for a prompt-injection refusal outcome."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot follow instructions that attempt to override the assistant's "
                "grounded-use rules or reveal hidden system behavior."
            ),
            documentary_basis=[],
            citations=[],
            confidence="low",
            limitations=[
                (
                    "This request triggered a prompt-injection guardrail and was refused "
                    "conservatively."
                )
            ],
            advisor_review_notice=advisor_review_notice,
        ),
        verification=verification,
    )


def build_missing_citation_guardrail_response(
    *,
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    advisor_review_notice: str,
) -> GroundedAnswerResult:
    """Return a typed guarded outcome for citationless answerable responses."""

    verification = GroundingVerification(
        supported=False,
        confidence="low",
        unsupported_claims=[
            "No traceable citations could be derived from the retrieved evidence."
        ],
        missing_citations=["At least one citation is required for an answerable response."],
    )
    return GroundedAnswerResult(
        query=query,
        response=AdvisorDraftResponse(
            suggested_answer=(
                "I cannot provide a grounded answer because the retrieved evidence did not "
                "produce traceable citations."
            ),
            documentary_basis=build_documentary_basis(retrieved_chunks),
            citations=[],
            confidence="low",
            limitations=[
                (
                    "At least one traceable citation is required before surfacing "
                    "an answerable response."
                )
            ],
            advisor_review_notice=advisor_review_notice,
        ),
        verification=verification,
    )
