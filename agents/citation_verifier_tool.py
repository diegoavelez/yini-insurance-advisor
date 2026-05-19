"""Independently callable citation verifier tool wrapper."""

from __future__ import annotations

import logging
import re
from collections.abc import Sequence

from contracts import (
    Citation,
    CitationVerifierToolResult,
    GroundingVerification,
    GroundingVerificationResult,
    RetrievedChunk,
    ToolError,
)
from ops.observability import log_timed_event

TOOL_LOGGER = logging.getLogger("yini.tools.citation_verifier")
TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]{4,}")


def classify_citation_verifier_error(exc: Exception) -> ToolError:
    """Map citation verification failures into the typed tool error surface."""

    if isinstance(exc, ValueError):
        return ToolError(kind="input_validation_failure", message=str(exc))
    return ToolError(kind="verification_failure", message=str(exc))


def validate_citation_verifier_input(
    drafted_output: str,
    citations: Sequence[Citation],
    evidence_chunks: Sequence[RetrievedChunk],
) -> None:
    """Validate citation verifier input before processing."""

    if not isinstance(drafted_output, str) or not drafted_output.strip():
        raise ValueError("drafted_output must be a non-empty string.")
    if not isinstance(citations, Sequence):
        raise ValueError("citations must be a sequence of Citation items.")
    if not isinstance(evidence_chunks, Sequence):
        raise ValueError("evidence_chunks must be a sequence of RetrievedChunk items.")
    for citation in citations:
        if not isinstance(citation, Citation):
            raise ValueError("citations must contain only Citation items.")
    for evidence_chunk in evidence_chunks:
        if not isinstance(evidence_chunk, RetrievedChunk):
            raise ValueError("evidence_chunks must contain only RetrievedChunk items.")


def citation_matches_chunk(citation: Citation, chunk: RetrievedChunk) -> bool:
    """Return whether one citation conservatively matches one evidence chunk."""

    if citation.chunk_id is not None and citation.chunk_id == chunk.chunk_id:
        return True
    if citation.document_name != chunk.document_name:
        return False
    if citation.page is not None and citation.page != chunk.page:
        return False
    if citation.section is not None and citation.section != chunk.section:
        return False
    if citation.clause_id is not None and citation.clause_id != chunk.clause_id:
        return False
    return True


def tokenize_for_support(text: str) -> set[str]:
    """Extract a conservative token set for weak support checks."""

    return {token.lower() for token in TOKEN_PATTERN.findall(text)}


def verify_citations_against_evidence(
    drafted_output: str,
    citations: Sequence[Citation],
    evidence_chunks: Sequence[RetrievedChunk],
) -> GroundingVerificationResult:
    """Conservatively assess whether citations support the drafted output."""

    if not citations:
        return GroundingVerificationResult(
            verification=GroundingVerification(
                supported=False,
                confidence="low",
                unsupported_claims=["Drafted output did not include any citations."],
                missing_citations=["No citations were provided for verification."],
            ),
            notes=["Verification could not confirm support because no citations were provided."],
        )

    reviewed_citations: list[Citation] = []
    missing_citations: list[str] = []
    matched_chunks: list[RetrievedChunk] = []

    for citation in citations:
        matching_chunk = next(
            (chunk for chunk in evidence_chunks if citation_matches_chunk(citation, chunk)),
            None,
        )
        if matching_chunk is None:
            missing_citations.append(
                f"Could not match citation for document '{citation.document_name}'."
            )
            continue
        reviewed_citations.append(citation)
        matched_chunks.append(matching_chunk)

    if not reviewed_citations:
        return GroundingVerificationResult(
            verification=GroundingVerification(
                supported=False,
                confidence="low",
                unsupported_claims=["No cited evidence could be matched to the provided evidence."],
                missing_citations=missing_citations,
            ),
            reviewed_citations=[],
            notes=["All provided citations failed traceability checks against the evidence."],
        )

    drafted_tokens = tokenize_for_support(drafted_output)
    evidence_tokens = {
        token
        for chunk in matched_chunks
        for token in tokenize_for_support(chunk.text)
    }
    token_overlap = drafted_tokens & evidence_tokens

    if len(reviewed_citations) != len(citations):
        return GroundingVerificationResult(
            verification=GroundingVerification(
                supported=False,
                confidence="medium",
                unsupported_claims=["Some cited claims could not be fully verified."],
                missing_citations=missing_citations,
            ),
            reviewed_citations=reviewed_citations,
            notes=["Only part of the cited evidence could be matched to the provided chunks."],
        )

    if not token_overlap:
        return GroundingVerificationResult(
            verification=GroundingVerification(
                supported=False,
                confidence="medium",
                unsupported_claims=[
                    "The drafted output is only weakly supported by the cited evidence."
                ],
                missing_citations=[],
            ),
            reviewed_citations=reviewed_citations,
            notes=[
                "Citations were traceable, but lexical overlap between the draft and "
                "evidence was weak."
            ],
        )

    confidence = "high" if all(citation.chunk_id for citation in reviewed_citations) else "medium"
    return GroundingVerificationResult(
        verification=GroundingVerification(
            supported=True,
            confidence=confidence,
            unsupported_claims=[],
            missing_citations=[],
        ),
        reviewed_citations=reviewed_citations,
        notes=[],
    )


def citation_verifier_tool(
    drafted_output: str,
    citations: Sequence[Citation],
    evidence_chunks: Sequence[RetrievedChunk],
    *,
    request_id: str | None = None,
) -> CitationVerifierToolResult:
    """Verify drafted output only against the provided cited evidence."""

    try:
        with log_timed_event(
            TOOL_LOGGER,
            event_type="citation_verifier_tool",
            request_id=request_id,
            start_fields={
                "citation_count": len(citations),
                "evidence_chunk_count": len(evidence_chunks),
            },
            success_fields_factory=(
                lambda _duration_ms: {
                    "supported": verification_result.verification.supported,
                    "confidence": verification_result.verification.confidence,
                    "reviewed_citation_count": len(verification_result.reviewed_citations),
                }
            ),
        ):
            validate_citation_verifier_input(drafted_output, citations, evidence_chunks)
            verification_result = verify_citations_against_evidence(
                drafted_output,
                citations,
                evidence_chunks,
            )
            return CitationVerifierToolResult(ok=True, result=verification_result)
    except Exception as exc:
        return CitationVerifierToolResult(
            ok=False,
            error=classify_citation_verifier_error(exc),
        )
