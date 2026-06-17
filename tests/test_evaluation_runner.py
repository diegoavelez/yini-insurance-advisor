from __future__ import annotations

from pathlib import Path

from contracts import (
    AdvisorDraftResponse,
    DocumentRetrievalResult,
    GroundedAnswerResult,
    GroundingVerification,
    RetrievalQuery,
    RetrievedChunk,
)
from core.evaluation_runner import run_mvp_acceptance_smoke


def test_run_mvp_acceptance_smoke_reports_matched_case(tmp_path: Path) -> None:
    smoke_dataset_path = tmp_path / "mvp-acceptance-smokes.json"
    smoke_dataset_path.write_text(
        """
{
  "version": "test-v1",
  "cases": [
    {
      "case_id": "case-001",
      "category_family": "MOVILIDAD/FINANCIACION",
      "retrieval_query": "¿Cómo funciona la financiación de pólizas individuales?",
      "grounded_answer_query": "¿Cómo funciona la financiación de pólizas individuales?",
      "filters": {
        "product": "movilidad",
        "document_type": "guide"
      },
      "expected_retrieval_evidence": ["instructivo financiacion de polizas v1.pdf"],
      "expected_answer_evidence": ["instructivo financiacion de polizas v1.pdf"]
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    def retrieve_chunks_fn(_query: RetrievalQuery) -> DocumentRetrievalResult:
        return DocumentRetrievalResult(
            chunks=[
                RetrievedChunk(
                    chunk_id="fin:v2:0004",
                    source_pdf_id="movilidad__transversales__instructivo-financiacion-de-polizas-v1",
                    source_pdf_relative_path=(
                        "MOVILIDAD/TRANSVERSALES/instructivo financiacion de polizas v1.pdf"
                    ),
                    chunk_schema_version="v2",
                    chunk_index=4,
                    text="Paso a paso de financiación.",
                    document_name="Manual Procedimiento Financiacion de polizas individuales",
                    document_type="guide",
                    product="movilidad",
                    section="Paso a paso",
                    section_path=[
                        "Manual Procedimiento Financiacion de polizas individuales",
                        "Paso a paso",
                    ],
                    score=0.91,
                )
            ]
        )

    def answer_query_fn(_query: RetrievalQuery) -> GroundedAnswerResult:
        return GroundedAnswerResult(
            query="¿Cómo funciona la financiación de pólizas individuales?",
            response=AdvisorDraftResponse(
                suggested_answer="La financiación usa la modalidad anual financiada.",
                documentary_basis=[
                    {
                        "document_name": "Manual Procedimiento Financiacion de polizas individuales",
                        "source_pdf_relative_path": (
                            "MOVILIDAD/TRANSVERSALES/instructivo financiacion de polizas v1.pdf"
                        ),
                        "document_type": "guide",
                        "product": "movilidad",
                        "section": "Paso a paso",
                    }
                ],
                citations=[
                    {
                        "document_name": "Manual Procedimiento Financiacion de polizas individuales",
                        "source_pdf_relative_path": (
                            "MOVILIDAD/TRANSVERSALES/instructivo financiacion de polizas v1.pdf"
                        ),
                        "document_type": "guide",
                        "product": "movilidad",
                        "chunk_id": "fin:v2:0004",
                        "section": "Paso a paso",
                    }
                ],
                confidence="high",
                limitations=[],
                advisor_review_notice="Se requiere revisión del asesor antes del uso externo.",
            ),
            verification=GroundingVerification(
                supported=True,
                confidence="high",
                unsupported_claims=[],
                missing_citations=[],
            ),
        )

    result = run_mvp_acceptance_smoke(
        acceptance_set_path=smoke_dataset_path,
        retrieve_chunks_fn=retrieve_chunks_fn,
        answer_query_fn=answer_query_fn,
    )

    assert result.acceptance_set_version == "test-v1"
    assert len(result.results) == 1
    assert result.results[0].case_id == "case-001"
    assert result.results[0].status == "matched"
    assert result.results[0].retrieval_matched is True
    assert result.results[0].answer_matched is True


def test_run_mvp_acceptance_smoke_reports_mismatched_case(tmp_path: Path) -> None:
    smoke_dataset_path = tmp_path / "mvp-acceptance-smokes.json"
    smoke_dataset_path.write_text(
        """
{
  "version": "test-v1",
  "cases": [
    {
      "case_id": "case-002",
      "category_family": "MOVILIDAD/VIAJES",
      "retrieval_query": "¿Qué cubre el seguro de viaje nacional?",
      "grounded_answer_query": "¿Qué cubre el seguro de viaje internacional?",
      "filters": {
        "product": "viajes",
        "document_type": "policy"
      },
      "expected_retrieval_evidence": ["clausulado viaje nacional v1.pdf"],
      "expected_answer_evidence": ["clausulado viaje internacional v1.pdf"]
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    def retrieve_chunks_fn(_query: RetrievalQuery) -> DocumentRetrievalResult:
        return DocumentRetrievalResult(
            chunks=[
                RetrievedChunk(
                    chunk_id="wrong:v2:0001",
                    source_pdf_id="movilidad__transversales__pv-planes-movilidad-v1",
                    source_pdf_relative_path="MOVILIDAD/TRANSVERSALES/pv planes movilidad v1.pdf",
                    chunk_schema_version="v2",
                    chunk_index=1,
                    text="Texto incorrecto.",
                    document_name="PROPUESTA DE VALOR MOVILIDAD",
                    document_type="guide",
                    product="movilidad",
                    section="Asistencia",
                    section_path=["PROPUESTA DE VALOR MOVILIDAD", "Asistencia"],
                    score=0.95,
                )
            ]
        )

    def answer_query_fn(_query: RetrievalQuery) -> GroundedAnswerResult:
        return GroundedAnswerResult(
            query="¿Qué cubre el seguro de viaje internacional?",
            response=AdvisorDraftResponse(
                suggested_answer="Respuesta incorrecta.",
                documentary_basis=[
                    {
                        "document_name": "PROPUESTA DE VALOR MOVILIDAD",
                        "source_pdf_relative_path": "MOVILIDAD/TRANSVERSALES/pv planes movilidad v1.pdf",
                        "document_type": "guide",
                        "product": "movilidad",
                        "section": "Asistencia",
                    }
                ],
                citations=[],
                confidence="low",
                limitations=[],
                advisor_review_notice="Se requiere revisión del asesor antes del uso externo.",
            ),
            verification=GroundingVerification(
                supported=True,
                confidence="low",
                unsupported_claims=[],
                missing_citations=[],
            ),
        )

    result = run_mvp_acceptance_smoke(
        acceptance_set_path=smoke_dataset_path,
        retrieve_chunks_fn=retrieve_chunks_fn,
        answer_query_fn=answer_query_fn,
    )

    assert len(result.results) == 1
    assert result.results[0].case_id == "case-002"
    assert result.results[0].status == "mismatched"
    assert result.results[0].retrieval_matched is False
    assert result.results[0].answer_matched is False
