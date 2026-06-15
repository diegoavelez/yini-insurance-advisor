from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import pytest

from contracts import ChunkBundle, ProcessedDocument
from rag.ingestion import (
    build_chunk_records,
    build_ingestion_artifact_paths,
    build_parser,
    clean_markdown,
    convert_pdf_to_markdown_with_backend,
    derive_source_pdf_id,
    docling_is_available,
    extract_document_metadata,
    main,
    normalize_known_document_markdown,
    normalize_pv_commercial_block,
    parse_bool,
    split_markdown_blocks,
)


def test_parse_bool_accepts_true_and_false() -> None:
    assert parse_bool("true") is True
    assert parse_bool("false") is False


def test_parse_bool_rejects_invalid_values() -> None:
    with pytest.raises(argparse.ArgumentTypeError):
        parse_bool("yes")


def test_parser_builds_canonical_ingest_command() -> None:
    args = build_parser().parse_args(
        [
            "ingest-pdfs",
            "--input-dir",
            "data/raw",
            "--markdown-dir",
            "data/markdown",
            "--processed-dir",
            "data/processed",
            "--manifest-path",
            "data/processed/ingestion-manifest.jsonl",
            "--overwrite",
            "true",
        ]
    )

    assert args.command == "ingest-pdfs"
    assert args.chunk_size == 1200
    assert args.chunk_overlap == 200
    assert args.glob == "*.pdf"
    assert args.overwrite is True
    assert args.fail_fast is False
    assert args.pdf_conversion_backend == "docling"
    assert args.docling_startup_timeout_seconds == 1800.0


@pytest.mark.parametrize(
    ("flag", "value"),
    [
        ("--chunk-size", "0"),
        ("--chunk-overlap", "-1"),
    ],
)
def test_parser_rejects_invalid_chunk_configuration(flag: str, value: str) -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(
            [
                "ingest-pdfs",
                "--input-dir",
                "data/raw",
                "--markdown-dir",
                "data/markdown",
                "--processed-dir",
                "data/processed",
                "--manifest-path",
                "data/processed/ingestion-manifest.jsonl",
                flag,
                value,
            ]
        )


def test_parser_accepts_chunk_configuration_overrides() -> None:
    args = build_parser().parse_args(
        [
            "ingest-pdfs",
            "--input-dir",
            "data/raw",
            "--markdown-dir",
            "data/markdown",
            "--processed-dir",
            "data/processed",
            "--manifest-path",
            "data/processed/ingestion-manifest.jsonl",
            "--chunk-size",
            "800",
            "--chunk-overlap",
            "100",
        ]
    )

    assert args.chunk_size == 800
    assert args.chunk_overlap == 100


def test_parser_accepts_docling_backend_controls() -> None:
    args = build_parser().parse_args(
        [
            "ingest-pdfs",
            "--input-dir",
            "data/raw",
            "--markdown-dir",
            "data/markdown",
            "--processed-dir",
            "data/processed",
            "--manifest-path",
            "data/processed/ingestion-manifest.jsonl",
            "--pdf-conversion-backend",
            "auto",
            "--docling-startup-timeout-seconds",
            "180",
        ]
    )

    assert args.pdf_conversion_backend == "auto"
    assert args.docling_startup_timeout_seconds == 180.0


def test_parser_builds_docling_warmup_command() -> None:
    args = build_parser().parse_args(
        [
            "warmup-docling-assets",
            "--sample-pdf",
            "data/raw/sample.pdf",
        ]
    )

    assert args.command == "warmup-docling-assets"
    assert args.sample_pdf == "data/raw/sample.pdf"
    assert args.docling_startup_timeout_seconds == 1800.0


def test_docling_smoke_check_reflects_importability() -> None:
    assert isinstance(docling_is_available(), bool)


def test_clean_markdown_is_conservative_and_deterministic() -> None:
    dirty_markdown = "# Policy Title\r\n\r\n\r\nClause 1   \r\n[]()\r\n\r\nClause 2\r\n"

    cleaned_markdown = clean_markdown(dirty_markdown)

    assert cleaned_markdown == "# Policy Title\n\nClause 1\n\nClause 2\n"


def test_extract_document_metadata_uses_heading_and_version_when_available() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=Path(".") / "policy-a.pdf",
        cleaned_markdown_text="# Sura Health Policy\nVersion: 2026-01\n\nCoverage text",
    )

    assert document_name == "Sura Health Policy"
    assert document_version == "2026-01"


def test_extract_document_metadata_falls_back_without_heading_or_version() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=Path(".") / "policy-a.pdf",
        cleaned_markdown_text="Coverage text only",
    )

    assert document_name == "policy-a"
    assert document_version is None


def test_extract_document_metadata_rejects_noisy_media_heading() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=(
            Path(".")
            / "preguntas frecuentes registro unico de intermediacion - rui.pdf"
        ),
        cleaned_markdown_text=(
            "# Grabación: https://player.vimeo.com/video/943790015\n\n"
            "Preguntas frecuentes sobre el registro único de intermediación.\n"
        ),
    )

    assert (
        document_name
        == "preguntas frecuentes registro unico de intermediacion - rui"
    )
    assert document_version is None


def test_extract_document_metadata_rejects_noisy_promotional_heading() -> None:
    document_name, document_version = extract_document_metadata(
        source_pdf_path=Path(".") / "como tomar fotos choque simple v2.pdf",
        cleaned_markdown_text=(
            "## estas recomendaciones para en un choque simple "
            "Ten en cuenta tomar fotos y videos\n\n"
            "Todas las fotos y videos que tomes nos ayudan a entender cómo fue el choque.\n\n"
            "## ¿Cómo tomar fotos y videos?\n"
        ),
    )

    assert document_name == "¿Cómo tomar fotos y videos?"
    assert document_version is None


def test_normalize_known_document_markdown_rewrites_choque_simple_photo_guide() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "como tomar fotos choque simple v2.pdf",
        cleaned_markdown_text=(
            "## estas recomendaciones para en un choque simple "
            "Ten en cuenta tomar fotos y videos\n\n"
            "Texto introductorio.\n\n"
            "## ¿Cómo tomar fotos y videos?\n\n"
            "## Antes de tomar las evidencias:\n\n"
            "Pon los conos.\n\n"
            "## Asegúrate de vivir\n\n"
            "segurossura.com.co\n"
        ),
    )

    assert normalized.startswith("# ¿Cómo tomar fotos y videos?\n\nTexto introductorio.")
    assert "## ¿Cómo tomar fotos y videos?" not in normalized
    assert "## Asegúrate de vivir" not in normalized
    assert "segurossura.com.co" not in normalized


def test_normalize_known_document_markdown_rewrites_arl_rui_faq_structure() -> None:
    source_pdf_path = (
        Path(".") / "preguntas frecuentes registro unico de intermediacion - rui.pdf"
    )
    question_1 = "## 1. ¿Cuál es la normatividad que rige el registro único de intermediarios?"
    question_2 = "## 2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?"
    question_3 = (
        "## 3. ¿Si realice el diplomado el 15 de enero del 2024 "
        "aplica el vencimiento de 4 años?"
    )
    normalized = normalize_known_document_markdown(
        source_pdf_path=source_pdf_path,
        cleaned_markdown_text=(
            "Memorias Streaming, conoce las novedades para la intermediación de seguros.\n\n"
            "Resolución 0136 de 2024.\n\n"
            "## Grabación: https:/ /player.vimeo.com/video/943790015\n\n"
            "Preguntas:\n\n"
            "1. ¿Cuál es la normatividad que rige el registro único de intermediarios?\n"
            "- Ley 1562 de 2012\n\n"
            "2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?\n"
            "Revisando el reporte.\n\n"
            "LINK:\n\n"
            "https:/ /www.fondoriesgoslaborales.gov.co/sin-categoria/apoya-eltalento/\n\n"
            "## iRegistro Unico de Intermediarios! Consulte aqui el estado de su registro\n\n"
            "Ingresa al RUI\n\n"
            "## MINISTERIODELTRABAJO\n\n"
            "| ITEM | ESTADO |\n"
            "|------|--------|\n"
            "| 1 | APROBADO |\n\n"
            "3. ¿Si realice el diplomado el 15 de enero del 2024 aplica el vencimiento de 4 años?\n"
            "No.\n"
        ),
    )

    assert normalized.startswith("# Preguntas frecuentes registro único de intermediación - RUI")
    assert question_1 in normalized
    assert question_2 in normalized
    assert question_3 in normalized
    assert "## Grabación:" not in normalized
    assert "## MINISTERIODELTRABAJO" not in normalized
    assert "iRegistro Unico de Intermediarios" not in normalized
    assert "| ITEM | ESTADO |" not in normalized


def test_normalize_known_document_markdown_rewrites_arl_commissions_guide() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "instructivos consulta de comisiones arl sura v2.pdf",
        cleaned_markdown_text=(
            "## Consulta liquidación de comisiones para intermediarios de Riesgos Laborales\n\n"
            "C a p a c i d a d :   A R L\n\n"
            "[   C a p a c i d a d   -   A R L ]\n\n"
            "- Ingresar a www.arlsura.com.\n"
            "- Selecciona iniciar sesión.\n\n"
            "sura\n\n"
            "- Seleccionar el módulo Intermediarios.\n\n"
            "sura sura\n\n"
            "- Diligenciar oficina, fecha inicial y fecha final.\n"
        ),
    )

    assert "C a p a c i d a d" not in normalized
    assert "[   C a p a c i d a d" not in normalized
    assert "\nsura\n" not in normalized
    assert "sura sura" not in normalized
    assert "- Ingresar a www.arlsura.com." in normalized
    assert "- Seleccionar el módulo Intermediarios." in normalized


def test_split_markdown_blocks_uses_semantic_arl_rui_question_sections() -> None:
    source_pdf_path = (
        Path(".") / "preguntas frecuentes registro unico de intermediacion - rui.pdf"
    )
    question_1 = "1. ¿Cuál es la normatividad que rige el registro único de intermediarios?"
    question_2 = "2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?"
    normalized = normalize_known_document_markdown(
        source_pdf_path=source_pdf_path,
        cleaned_markdown_text=(
            "Memorias Streaming, conoce las novedades para la intermediación de seguros.\n\n"
            "## Grabación: https:/ /player.vimeo.com/video/943790015\n\n"
            "1. ¿Cuál es la normatividad que rige el registro único de intermediarios?\n"
            "- Ley 1562 de 2012\n"
            "- Decreto 1117 de 2016\n\n"
            "2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?\n"
            "Revisando el reporte.\n"
        ),
    )

    blocks = split_markdown_blocks(normalized)

    assert blocks[1].section == question_1
    assert blocks[1].section_path == (
        "Preguntas frecuentes registro único de intermediación - RUI",
        question_1,
    )
    assert blocks[2].section == question_2
    assert all(block.section != "MINISTERIODELTRABAJO" for block in blocks if block.section)


def test_build_chunk_records_disables_overlap_between_arl_rui_questions() -> None:
    source_pdf_path = (
        Path("data/raw")
        / "ARL/preguntas frecuentes registro unico de intermediacion - rui.pdf"
    )
    source_pdf_relative_path = Path(
        "ARL/preguntas frecuentes registro unico de intermediacion - rui.pdf"
    )
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / source_pdf_relative_path,
        cleaned_markdown_text=(
            "Memorias Streaming, conoce las novedades.\n\n"
            "1. ¿Cuál es la normatividad que rige el registro único de intermediarios?\n"
            "- Ley 1562 de 2012\n"
            "- Decreto 1117 de 2016\n"
            "- Resolución 0136 de 2024\n\n"
            "2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?\n"
            "Revisando el reporte de asesores aprobados.\n"
        ),
    )

    chunk_records = build_chunk_records(
        source_pdf_id="arl__preguntas-frecuentes-registro-unico-de-intermediacion-rui",
        document_name="Preguntas frecuentes registro único de intermediación - RUI",
        document_version=None,
        document_type="faq",
        product="arl",
        source_pdf_path=source_pdf_path,
        source_pdf_relative_path=source_pdf_relative_path,
        cleaned_markdown_output_path=Path(
            "data/processed/arl__preguntas-frecuentes-registro-unico-de-intermediacion-rui.cleaned.md"
        ),
        cleaned_markdown_text=normalized,
        chunk_size=1200,
        chunk_overlap=200,
    )

    question_chunks = [
        chunk
        for chunk in chunk_records
        if chunk.section and chunk.section[0].isdigit()
    ]

    assert question_chunks[0].section.startswith("1. ¿Cuál es la normatividad")
    assert "## 2." not in question_chunks[0].text
    assert question_chunks[1].section.startswith("2. Teniendo en cuenta la resolución 0136")
    assert "## 1." not in question_chunks[1].text
    assert [chunk.section for chunk in question_chunks[:2]] == [
        (
            "1. ¿Cuál es la normatividad que rige el registro único "
            "de intermediarios?"
        ),
        "2. Teniendo en cuenta la resolución 0136 de 2024, ¿cómo sé mi vigencia?",
    ]


def test_build_chunk_records_preserves_clean_arl_commissions_procedure() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "instructivos consulta de comisiones arl sura v2.pdf",
        cleaned_markdown_text=(
            "## Consulta liquidación de comisiones para intermediarios de Riesgos Laborales\n\n"
            "C a p a c i d a d :   A R L\n\n"
            "sura\n\n"
            "- Ingresar a www.arlsura.com.\n"
            "- Selecciona iniciar sesión.\n"
            "- Seleccionar el módulo Intermediarios.\n"
        ),
    )

    chunk_records = build_chunk_records(
        source_pdf_id="arl__instructivos-consulta-de-comisiones-arl-sura-v2",
        document_name="Consulta liquidación de comisiones para intermediarios de Riesgos Laborales",
        document_version=None,
        document_type="guide",
        product="arl",
        source_pdf_path=Path("data/raw/ARL/instructivos consulta de comisiones arl sura v2.pdf"),
        source_pdf_relative_path=Path("ARL/instructivos consulta de comisiones arl sura v2.pdf"),
        cleaned_markdown_output_path=Path(
            "data/processed/arl__instructivos-consulta-de-comisiones-arl-sura-v2.cleaned.md"
        ),
        cleaned_markdown_text=normalized,
        chunk_size=1200,
        chunk_overlap=200,
    )

    assert len(chunk_records) == 1
    assert "C a p a c i d a d" not in chunk_records[0].text
    assert "\nsura\n" not in chunk_records[0].text
    assert "- Ingresar a www.arlsura.com." in chunk_records[0].text
    assert "- Seleccionar el módulo Intermediarios." in chunk_records[0].text


def test_build_chunk_records_deduplicates_leading_heading_scaffold() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        document_type="policy",
        product="arl",
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Section A\n\n"
            "## Section A\n\n"
            "Body text.\n"
        ),
        chunk_size=1200,
        chunk_overlap=200,
    )

    section_chunk = next(
        chunk for chunk in chunk_records if chunk.section == "Section A"
    )

    assert section_chunk.text.count("## Section A") == 1
    assert "Body text." in section_chunk.text


def test_build_chunk_records_deduplicates_arl_remuneracion_heading_surface() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="arl__politica-de-remuneracion-canal-externo-v4",
        document_name="Canal Externo ARL V1 Esquema remuneración y políticas que lo complementan",
        document_version=None,
        document_type="policy",
        product="arl",
        source_pdf_path=Path("data/raw/ARL/politica de remuneracion canal externo v4.pdf"),
        source_pdf_relative_path=Path("ARL/politica de remuneracion canal externo v4.pdf"),
        cleaned_markdown_output_path=Path(
            "data/processed/arl__politica-de-remuneracion-canal-externo-v4.cleaned.md"
        ),
        cleaned_markdown_text=(
            "## Canal Externo ARL V1 Esquema remuneración y políticas que lo complementan\n\n"
            "## Canales para la afiliación a ARL SURA\n\n"
            "## Canales para la afiliación a ARL SURA\n\n"
            "En ARL SURA tenemos definidos diversos canales.\n"
        ),
        chunk_size=1200,
        chunk_overlap=200,
    )

    section_chunk = next(
        chunk
        for chunk in chunk_records
        if chunk.section == "Canales para la afiliación a ARL SURA"
    )

    assert section_chunk.text.count("## Canales para la afiliación a ARL SURA") == 1
    assert "En ARL SURA tenemos definidos diversos canales." in section_chunk.text


def test_build_chunk_records_drops_repeated_section_heading_inside_chunk() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        document_type="policy",
        product="arl",
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Section A\n\n"
            "## Parent Heading\n\n"
            "## Section A\n\n"
            "Body text.\n"
        ),
        chunk_size=1200,
        chunk_overlap=200,
    )

    section_chunk = next(chunk for chunk in chunk_records if chunk.section == "Section A")

    assert section_chunk.text.count("## Section A") == 1
    assert "## Parent Heading" not in section_chunk.text
    assert "Body text." in section_chunk.text


def test_normalize_known_document_markdown_rewrites_suscripcion_pdfium_surface() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "politicas de suscripcion de movilidad.pdf",
        cleaned_markdown_text=(
            "# politicas de suscripcion de movilidad\n\n"
            "## Page 1\n\n"
            "1\n"
            "Volver\n"
            "al inicio\n"
            "Versión 6 5 – abril 202 6\n\n"
            "## Page 2\n\n"
            "2\n"
            "Volver\n"
            "al inicio\n"
            "Tabla de contenido\n"
            "1. DEFINICIÓN DE RIESGO ESTÁNDAR ................................ 5\n\n"
            "## Page 5\n\n"
            "5\n"
            "Volver\n"
            "al inicio\n"
            "1. DEFINICIÓN DE RIESGO ESTÁNDAR\n"
            "Texto de política.\n\n"
            "## Page 31\n\n"
            "31\n"
            "Volver\n"
            "al inicio\n"
            "13. PROCEDIMIENTOS\n"
            "13.1. Lineamientos de suscripción.\n"
            "El intermediario será responsable.\n"
        ),
    )

    assert normalized.startswith(
        "# politicas de suscripcion de movilidad\n\nVersión 6 5 – abril 202 6"
    )
    assert "## Page 1" not in normalized
    assert "## Page 2" not in normalized
    assert "Tabla de contenido" not in normalized
    assert "Volver" not in normalized
    assert "................................" not in normalized
    assert "## 1. DEFINICIÓN DE RIESGO ESTÁNDAR" in normalized
    assert "## 13. PROCEDIMIENTOS" in normalized
    assert "### 13.1. Lineamientos de suscripción." in normalized


def test_build_chunk_records_is_deterministic() -> None:
    cleaned_markdown_text = (
        "# Policy Title\n\n"
        "Paragraph one.\n\n"
        "Paragraph two is slightly longer.\n\n"
        "## Section A\n\n"
        "Paragraph three."
    )

    first_chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=60,
        chunk_overlap=20,
    )
    second_chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=cleaned_markdown_text,
        chunk_size=60,
        chunk_overlap=20,
    )

    assert [record.chunk_id for record in first_chunk_records] == [
        record.chunk_id for record in second_chunk_records
    ]
    assert [record.text for record in first_chunk_records] == [
        record.text for record in second_chunk_records
    ]
    assert all(record.chunk_schema_version == "v2" for record in first_chunk_records)


def test_build_chunk_records_keeps_heading_with_following_body_when_it_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n## Coverage\n\nCoverage applies to outpatient care."
        ),
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert "## Coverage\n\nCoverage applies to outpatient care." in chunk_records[0].text
    assert chunk_records[0].section == "Coverage"
    assert chunk_records[0].section_path == ["Policy Title", "Coverage"]


def test_build_chunk_records_deduplicates_leading_section_heading_from_chunk_body() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="guide-a",
        document_name="Guide A",
        document_version=None,
        source_pdf_path=Path("data/raw/guide-a.pdf"),
        source_pdf_relative_path=Path("guide-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/guide-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Guide A\n\n"
            "## Before taking evidence\n\n"
            "## Before taking evidence\n\n"
            "Place safety cones first."
        ),
        chunk_size=400,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert chunk_records[0].text.startswith("# Guide A\n\n## Before taking evidence\n\n")
    assert "## Before taking evidence\n\n## Before taking evidence" not in chunk_records[0].text


def test_build_chunk_records_skips_heading_only_overlap_chunk() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        document_type="policy",
        product="arl",
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Section A\n\n"
            + ("Body text for section A. " * 50)
            + "\n\n"
            "## Parent Heading\n\n"
            "## Section A\n\n"
            "## Section B\n\n"
            "Body text for section B.\n"
        ),
        chunk_size=500,
        chunk_overlap=120,
    )

    assert all(
        any(
            line.strip() and not line.strip().startswith("#")
            for line in chunk.text.splitlines()
        )
        for chunk in chunk_records
    )
    assert any(chunk.section == "Section A" for chunk in chunk_records)
    assert any(chunk.section == "Section B" for chunk in chunk_records)


def test_build_chunk_records_keeps_clause_marker_with_following_text_when_it_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text="# Policy Title\n\n1. Coverage\n\nApplies only after deductible.",
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert "1. Coverage\n\nApplies only after deductible." in chunk_records[0].text


def test_build_chunk_records_avoids_tiny_heading_only_chunk_when_next_body_fits() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n## Exclusions\n\nNo coverage applies to cosmetic surgery.\n\n"
            "## Waiting Period\n\nThirty days."
        ),
        chunk_size=120,
        chunk_overlap=20,
    )

    assert all(record.text.strip() != "## Exclusions" for record in chunk_records)
    assert all(record.text.strip() != "## Waiting Period" for record in chunk_records)


def test_build_chunk_records_preserves_clause_split_fallback_for_oversized_content() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text="# Policy Title\n\n1. Coverage\n\n" + ("A" * 160),
        chunk_size=80,
        chunk_overlap=20,
    )

    assert len(chunk_records) >= 2
    assert chunk_records[0].text.startswith("# Policy Title")
    assert any("1. Coverage" in record.text for record in chunk_records)


def test_build_chunk_records_prefixes_missing_section_context_for_follow_on_chunks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Comparison Section\n\n"
            "Alpha.\n\n"
            "Beta.\n\n"
            "Gamma.\n\n"
            "Delta.\n\n"
            "Epsilon.\n\n"
            "Zeta."
        ),
        chunk_size=70,
        chunk_overlap=10,
    )

    assert len(chunk_records) >= 2
    assert all("## Comparison Section" in record.text for record in chunk_records)
    assert all(record.section == "Comparison Section" for record in chunk_records)


def test_build_chunk_records_does_not_duplicate_existing_section_context() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n## Coverage\n\nCoverage applies to outpatient care."
        ),
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert chunk_records[0].text.count("## Coverage") == 1


def test_build_chunk_records_greedily_aggregates_short_same_section_blocks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Comparison Grid\n\n"
            "Alpha\n\n"
            "Beta\n\n"
            "Gamma\n\n"
            "Delta\n\n"
            "Epsilon"
        ),
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert "Alpha" in chunk_records[0].text
    assert "Beta" in chunk_records[0].text
    assert "Gamma" in chunk_records[0].text
    assert "Delta" in chunk_records[0].text
    assert "Epsilon" in chunk_records[0].text


def test_split_markdown_blocks_normalizes_comparison_tables_into_plan_statements() -> None:
    blocks = split_markdown_blocks(
        "## DIFERENCIALES SURA\n\n"
        "## Planes SURA\n\n"
        "| | Plan Autos Global | Plan Autos Clásico |\n"
        "|---|---|---|\n"
        "| Estrategia | Acompañamiento integral | Cobertura estándar |\n"
        "| Segmento | • Vehículos 0 km • Viajeros | • Vehículos usados • Ahorro |\n"
    )

    assert len(blocks) == 3
    assert blocks[2].section == "Planes SURA"
    assert blocks[2].section_path == ("DIFERENCIALES SURA", "Planes SURA")
    assert "Plan Autos Global" in blocks[2].text
    assert "- Estrategia: Acompañamiento integral" in blocks[2].text
    assert "- Segmento: Vehículos 0 km; Viajeros" in blocks[2].text
    assert "Plan Autos Clásico" in blocks[2].text
    assert "- Segmento: Vehículos usados; Ahorro" in blocks[2].text
    assert "| Estrategia |" not in blocks[2].text


def test_split_markdown_blocks_leaves_non_comparison_content_unchanged() -> None:
    blocks = split_markdown_blocks(
        "## Coberturas\n\nTexto normal sin tabla.\n\n1. Condición especial"
    )

    assert len(blocks) == 3
    assert blocks[1].text == "Texto normal sin tabla."
    assert blocks[2].text == "1. Condición especial"


def test_split_markdown_blocks_skips_page_heading_blocks_and_promotes_semantic_section() -> None:
    blocks = split_markdown_blocks(
        "# pv bicis y patinetas v2\n\n"
        "## Page 4\n\n"
        "Daños a Terceros\n"
        "Con opción de valor asegurado\n"
        "de $64.000.000 ó $160.000.000\n"
        "Accidentes personales\n"
        "Con valor asegurado de\n"
        "$10.000.000\n"
        "COBERTURAS Y PLANES\n"
        "Asistencia\n"
    )

    assert len(blocks) == 2
    assert blocks[1].section == "COBERTURAS Y PLANES"
    assert blocks[1].section_path == ("pv bicis y patinetas v2", "COBERTURAS Y PLANES")
    assert (
        "- Daños a Terceros: Con opción de valor asegurado de $64.000.000 ó $160.000.000"
        in blocks[1].text
    )
    assert "- Accidentes personales: Con valor asegurado de $10.000.000" in blocks[1].text


def test_split_markdown_blocks_uses_semantic_suscripcion_headings_after_normalization() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "politicas de suscripcion de movilidad.pdf",
        cleaned_markdown_text=(
            "# politicas de suscripcion de movilidad\n\n"
            "## Page 5\n\n"
            "5\n"
            "Volver\n"
            "al inicio\n"
            "1. DEFINICIÓN DE RIESGO ESTÁNDAR\n"
            "Texto de política.\n\n"
            "## Page 31\n\n"
            "31\n"
            "Volver\n"
            "al inicio\n"
            "13. PROCEDIMIENTOS\n"
            "13.1. Lineamientos de suscripción.\n"
            "El intermediario será responsable.\n"
        ),
    )

    blocks = split_markdown_blocks(normalized)

    assert blocks[1].section == "1. DEFINICIÓN DE RIESGO ESTÁNDAR"
    assert blocks[1].section_path == (
        "politicas de suscripcion de movilidad",
        "1. DEFINICIÓN DE RIESGO ESTÁNDAR",
    )
    assert blocks[-1].section == "13.1. Lineamientos de suscripción."
    assert blocks[-1].section_path == (
        "politicas de suscripcion de movilidad",
        "13. PROCEDIMIENTOS",
        "13.1. Lineamientos de suscripción.",
    )


def test_normalize_known_document_markdown_promotes_root_heading_for_choque_simple_atencion(
) -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "proceso atencion choque simple v2.pdf",
        cleaned_markdown_text=(
            "Normatividad vigente\n\n"
            "## EN EVENTOS DE CHOQUES\n\n"
            "Solo danos materiales\n"
        ),
    )

    blocks = split_markdown_blocks(normalized)

    assert normalized.startswith("# EN EVENTOS DE CHOQUES")
    assert "Normatividad vigente" not in normalized
    assert blocks[1].section == "EN EVENTOS DE CHOQUES"
    assert blocks[1].section_path == ("EN EVENTOS DE CHOQUES",)


def test_normalize_known_document_markdown_promotes_root_heading_for_choque_simple_recobro(
) -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "proceso recobro choque simple v2.pdf",
        cleaned_markdown_text=(
            "SURA te asignará un abogado para acompañarte.\n\n"
            "## Servicios de recobro para accidentes\n\n"
            "## Solo daños materiales\n\n"
            "CHOQUE SIMPLE: definición.\n"
        ),
    )

    blocks = split_markdown_blocks(normalized)

    assert normalized.startswith("# Servicios de recobro para accidentes")
    assert blocks[0].section == "Servicios de recobro para accidentes"
    assert blocks[0].section_path == ("Servicios de recobro para accidentes",)
    assert blocks[1].section == "Solo daños materiales"
    assert blocks[1].section_path == (
        "Servicios de recobro para accidentes",
        "Solo daños materiales",
    )


def test_normalize_known_document_markdown_rewrites_collective_nested_headings() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "politicas de suscripcion de movilidad.pdf",
        cleaned_markdown_text=(
            "# politicas de suscripcion de movilidad\n\n"
            "## Page 60\n\n"
            "60\n"
            "Volver\n"
            "al inicio\n"
            "14. PÓLIZAS COLECTIVAS\n"
            "14.6. Modalidades de facturación – Autos Colectivos :\n"
            "En el negocio de autos colectivos se definen las siguientes modalidades.\n"
            "2.1. Facturación agrupada\n"
            "El sistema factura en un único documento.\n"
            "2.2. Facturación (cobro) agrupada con devolución por asegurado\n"
            "El sistema genera una única factura diaria.\n"
        ),
    )

    assert "### 14.6. Modalidades de facturación – Autos Colectivos :" in normalized
    assert "#### 14.6.1. Facturación agrupada" in normalized
    assert (
        "#### 14.6.2. Facturación (cobro) agrupada con devolución por asegurado"
        in normalized
    )
    assert "### 2.1. Facturación agrupada" not in normalized
    assert (
        "### 2.2. Facturación (cobro) agrupada con devolución por asegurado"
        not in normalized
    )


def test_split_markdown_blocks_uses_normalized_suscripcion_collective_nested_path() -> None:
    normalized = normalize_known_document_markdown(
        source_pdf_path=Path(".") / "politicas de suscripcion de movilidad.pdf",
        cleaned_markdown_text=(
            "# politicas de suscripcion de movilidad\n\n"
            "14. PÓLIZAS COLECTIVAS\n"
            "14.6. Modalidades de facturación – Autos Colectivos :\n"
            "2.1. Facturación agrupada\n"
            "El sistema factura en un único documento.\n"
        ),
    )

    blocks = split_markdown_blocks(normalized)

    assert blocks[-1].section == "14.6.1. Facturación agrupada"
    assert blocks[-1].section_path == (
        "politicas de suscripcion de movilidad",
        "14. PÓLIZAS COLECTIVAS",
        "14.6. Modalidades de facturación – Autos Colectivos :",
        "14.6.1. Facturación agrupada",
    )


def test_build_chunk_records_avoids_page_heading_only_chunks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="policy-a",
        document_name="Policy Title",
        document_version=None,
        source_pdf_path=Path("data/raw/policy-a.pdf"),
        source_pdf_relative_path=Path("policy-a.pdf"),
        cleaned_markdown_output_path=Path("data/processed/policy-a.cleaned.md"),
        cleaned_markdown_text=(
            "# Policy Title\n\n"
            "## Page 6\n\n"
            "GENERALIDADES\n\n"
            "Bicis: Desde $600mil hasta $30mill.\n"
        ),
        chunk_size=200,
        chunk_overlap=20,
    )

    assert len(chunk_records) == 1
    assert chunk_records[0].section == "GENERALIDADES"
    assert chunk_records[0].section_path == ["Policy Title", "GENERALIDADES"]
    assert "## Page 6" not in chunk_records[0].text


def test_split_markdown_blocks_normalizes_expedition_requirements_linear_grid() -> None:
    blocks = split_markdown_blocks(
        "# pv bicis y patinetas v2\n\n"
        "## Page 6\n\n"
        "Requisitos Vinculaciones\n"
        "Bicis\n"
        "Entre $600.000 y\n"
        "$3.000.000\n"
        "• fotos marco\n"
        "• factura de compra\n"
        "Todos los clientes\n"
        "Patinetas\n"
        "Entre $3.000.001 y\n"
        "$10.000.000\n"
        "• Inspección virtual\n"
        "• factura de compra\n"
        "EXPEDICIÓN REQUISITOS\n"
    )

    assert blocks[1].section == "EXPEDICIÓN REQUISITOS"
    assert "- Bicis / Entre $600.000 y $3.000.000:" in blocks[1].text
    assert "- Patinetas / Entre $3.000.001 y $10.000.000:" in blocks[1].text


def test_split_markdown_blocks_normalizes_deductible_linear_grid() -> None:
    blocks = split_markdown_blocks(
        "# pv bicis y patinetas v2\n\n"
        "## Page 9\n\n"
        "Bicis\n"
        "Entre $600.000 y\n"
        "$3.000.000 $0 No aplica cobertura 15%\n"
        "A partir de las 48 horas\n"
        "Patinetas\n"
        "Entre $3.000.001 y\n"
        "$10.000.000 $0 No aplica cobertura 15% min 1 SMLMV\n"
        "A partir de las 48 horas\n"
        "DEDUCIBLE\n"
    )

    assert blocks[1].section == "DEDUCIBLE"
    assert "- Bicis: Entre $600.000 y $3.000.000 $0 No aplica cobertura 15%" in blocks[1].text
    assert (
        "- Patinetas: Entre $3.000.001 y $10.000.000 $0 No aplica cobertura 15% min 1 SMLMV"
        in blocks[1].text
    )


def test_split_markdown_blocks_normalizes_choque_simple_circular_sections() -> None:
    blocks = split_markdown_blocks(
        "# CIRCULAR EXTERNA\n\n"
        "DocumentofirmadodigitalmenteporelMinisteriodeTransporte\n"
        "www.mintransporte.gov.co\n\n"
        "CIRCULAR EXTERNA\n"
        "29-09-2022\n"
        "ASUNTO:\n"
        "Instrucciones para el cumplimiento del Artículo 16 de la Ley 2251 de 2022.\n\n"
        "\" Artículo 16. El artículo 143 de la Ley 769 de 2002 quedará así:\n"
        "'Artículo 143. Daños materiales.\n\n"
        "Los conductores deben retirar inmediatamente los vehículos colisionados\n"
        "y acudir a los centros de conciliación.\n\n"
        "No tendrán que elaborar el informe policial de accidentes de tránsito.\n\n"
        "1. En los accidentes de tránsito donde solo se causen daños materiales,\n"
        "los conductores deben retirar inmediatamente los vehículos.\n"
    )

    sections = [block.section for block in blocks]

    assert "CIRCULAR EXTERNA" not in sections
    assert sections == [
        "ASUNTO CHOQUE SIMPLE",
        "ARTÍCULO 16 — DAÑOS MATERIALES",
        "INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE",
        "INFORME POLICIAL Y RECAUDO PROBATORIO",
        "INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE",
    ]
    assert "Artículo 16 de la Ley 2251 de 2022" in blocks[0].text
    assert "Artículo 143. Daños materiales." in blocks[1].text
    assert "retirar inmediatamente los vehículos" in blocks[2].text
    assert "informe policial de accidentes de tránsito" in blocks[3].text


def test_normalize_pv_commercial_block_removes_slogans_and_normalizes_applicability() -> None:
    normalized = normalize_pv_commercial_block(
        "PLANES QUE APLICAN\n"
        "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO\n"
        "- o Plan Autos Global\n"
        "- o Plan Motos\n"
        "- o\n"
    )

    assert normalized == "PLANES QUE APLICA\n- Plan Autos Global\n- Plan Motos"


def test_normalize_pv_commercial_block_strips_inline_slogan_suffixes() -> None:
    normalized = normalize_pv_commercial_block(
        "Si necesitas ir a algún lugar y no puedes manejar "
        "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO\n"
        "o Plan Autos Global\n"
    )

    assert "SENTIRTE ACOMPAÑADO" not in normalized
    assert normalized == "Si necesitas ir a algún lugar y no puedes manejar\n- Plan Autos Global"


def test_split_markdown_blocks_merges_pv_benefit_with_following_applicability() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="pv-demo",
        document_name="PROPUESTA DE VALOR MOVILIDAD",
        document_version=None,
        document_type="guide",
        product="movilidad",
        source_pdf_path=Path("data/raw/MOVILIDAD/TRANSVERSALES/pv-demo.pdf"),
        source_pdf_relative_path=Path("MOVILIDAD/TRANSVERSALES/pv-demo.pdf"),
        cleaned_markdown_output_path=Path("data/processed/pv-demo.cleaned.md"),
        cleaned_markdown_text=(
            "# PROPUESTA DE VALOR MOVILIDAD\n\n"
            "## APP\n\n"
            "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO\n"
            "Puedes pedir grúa y conductor elegido desde la App.\n\n"
            "## PLANES QUE APLICAN\n\n"
            "- o Plan Autos Global\n"
            "- o Plan Motos\n"
        ),
        chunk_size=500,
        chunk_overlap=50,
    )

    matching_chunk = next(
        chunk
        for chunk in chunk_records
        if chunk.section == "APP"
        and "## PLANES QUE APLICA" in chunk.text
        and "- Plan Autos Global" in chunk.text
    )

    assert matching_chunk.section_path == ["PROPUESTA DE VALOR MOVILIDAD", "APP"]
    assert "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO" not in matching_chunk.text


def test_split_markdown_blocks_skips_pv_slogan_headings() -> None:
    blocks = split_markdown_blocks(
        "# PROPUESTA DE VALOR MOVILIDAD\n\n"
        "## Taller móvil ilimitado\n\n"
        "## SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO\n\n"
        "Si te varas, SURA envía un taller móvil.\n"
    )

    sections = [block.section for block in blocks]

    assert "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO" not in sections
    assert sections[0] == "PROPUESTA DE VALOR MOVILIDAD"
    assert sections[1:] == ["Taller móvil ilimitado", "Taller móvil ilimitado"]


def test_build_chunk_records_disables_overlap_for_pv_applicability_chunks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="pv-applicability",
        document_name="PROPUESTA DE VALOR MOVILIDAD",
        document_version=None,
        document_type="guide",
        product="movilidad",
        source_pdf_path=Path("data/raw/MOVILIDAD/TRANSVERSALES/pv.pdf"),
        source_pdf_relative_path=Path("MOVILIDAD/TRANSVERSALES/pv.pdf"),
        cleaned_markdown_output_path=Path("data/processed/pv.cleaned.md"),
        cleaned_markdown_text=(
            "# PROPUESTA DE VALOR MOVILIDAD\n\n"
            "## PLANES QUE APLICA\n\n"
            "- Plan Autos Global: beneficio uno beneficio uno beneficio uno.\n\n"
            "- Plan Autos Clásico: beneficio dos beneficio dos beneficio dos.\n\n"
            "- Plan Motos: beneficio tres beneficio tres beneficio tres.\n"
        ),
        chunk_size=120,
        chunk_overlap=80,
    )

    assert len(chunk_records) == 3
    assert "beneficio uno" in chunk_records[0].text
    assert "beneficio uno" not in chunk_records[1].text
    assert "beneficio dos" in chunk_records[1].text
    assert "beneficio dos" not in chunk_records[2].text
    assert "beneficio tres" in chunk_records[2].text


def test_build_chunk_records_collapse_equivalent_pv_applicability_headings() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="pv-heading-variants",
        document_name="PROPUESTA DE VALOR MOVILIDAD",
        document_version=None,
        document_type="guide",
        product="movilidad",
        source_pdf_path=Path("data/raw/MOVILIDAD/TRANSVERSALES/pv.pdf"),
        source_pdf_relative_path=Path("MOVILIDAD/TRANSVERSALES/pv.pdf"),
        cleaned_markdown_output_path=Path("data/processed/pv.cleaned.md"),
        cleaned_markdown_text=(
            "# PROPUESTA DE VALOR MOVILIDAD\n\n"
            "## PLANES QUE APLICA\n\n"
            "## Plan que aplica\n"
            "- Plan Autos Global\n"
        ),
        chunk_size=300,
        chunk_overlap=50,
    )

    assert "## Plan que aplica" not in chunk_records[0].text


def test_build_chunk_records_deduplicate_exact_standalone_pv_applicability_chunks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="pv-dedup",
        document_name="PROPUESTA DE VALOR MOVILIDAD",
        document_version=None,
        document_type="guide",
        product="movilidad",
        source_pdf_path=Path("data/raw/MOVILIDAD/TRANSVERSALES/pv.pdf"),
        source_pdf_relative_path=Path("MOVILIDAD/TRANSVERSALES/pv.pdf"),
        cleaned_markdown_output_path=Path("data/processed/pv.cleaned.md"),
        cleaned_markdown_text=(
            "# PROPUESTA DE VALOR MOVILIDAD\n\n"
            "## PLANES QUE APLICA\n\n"
            "- Plan Autos Global\n"
            "- Plan Autos Clásico\n\n"
            "## PLANES QUE APLICA\n\n"
            "- Plan Autos Global\n"
            "- Plan Autos Clásico\n\n"
            "## Anticipo\n\n"
            "Beneficio distinto.\n"
        ),
        chunk_size=300,
        chunk_overlap=50,
    )

    applicability_chunks = [
        chunk for chunk in chunk_records if chunk.section == "PLANES QUE APLICA"
    ]

    assert len(applicability_chunks) == 1
    assert len(chunk_records) == 2
    assert chunk_records[0].chunk_id == "pv-dedup:v2:0000"
    assert chunk_records[1].chunk_id == "pv-dedup:v2:0001"


def test_build_chunk_records_keep_distinct_standalone_pv_applicability_chunks() -> None:
    chunk_records = build_chunk_records(
        source_pdf_id="pv-dedup-distinct",
        document_name="PROPUESTA DE VALOR MOVILIDAD",
        document_version=None,
        document_type="guide",
        product="movilidad",
        source_pdf_path=Path("data/raw/MOVILIDAD/TRANSVERSALES/pv.pdf"),
        source_pdf_relative_path=Path("MOVILIDAD/TRANSVERSALES/pv.pdf"),
        cleaned_markdown_output_path=Path("data/processed/pv.cleaned.md"),
        cleaned_markdown_text=(
            "# PROPUESTA DE VALOR MOVILIDAD\n\n"
            "## PLANES QUE APLICA\n\n"
            "- Plan Autos Global: aplica al beneficio A.\n\n"
            "## PLANES QUE APLICA\n\n"
            "- Plan Motos: aplica al beneficio B.\n"
        ),
        chunk_size=90,
        chunk_overlap=50,
    )

    applicability_chunks = [
        chunk for chunk in chunk_records if chunk.section == "PLANES QUE APLICA"
    ]

    assert any(
        "Plan Autos Global: aplica al beneficio A." in chunk.text
        for chunk in applicability_chunks
    )
    assert any(
        "Plan Motos: aplica al beneficio B." in chunk.text
        for chunk in applicability_chunks
    )


def test_split_markdown_blocks_normalize_heading_prefixed_pv_applicability_body() -> None:
    blocks = split_markdown_blocks(
        "# PROPUESTA DE VALOR MOVILIDAD\n\n"
        "## PLANES QUE APLICA\n"
        "Si necesitas ir a algún lugar y no puedes manejar "
        "SENTIRTE ACOMPAÑADO / AHORRAR TIEMPO / AHORRAR DINERO\n"
        "- Plan Autos Global\n"
    )

    assert "SENTIRTE ACOMPAÑADO" not in blocks[-1].text
    assert "Si necesitas ir a algún lugar y no puedes manejar" in blocks[-1].text


def test_cli_fails_when_input_directory_is_missing(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(tmp_path / "missing"),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "Input directory does not exist" in captured.err


def test_cli_fails_loudly_when_no_pdf_conversion_backend_is_available(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: False)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: False)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Docling is not installed" in captured.err


def test_convert_pdf_to_markdown_falls_back_to_pdfium_when_docling_times_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: True)

    def fake_docling(_path, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="docling", timeout=20.0)

    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown_with_docling", fake_docling)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_pdfium",
        lambda _path: "# fallback markdown\n",
    )

    rendered = convert_pdf_to_markdown_with_backend(
        Path("policy-a.pdf"),
        backend="auto",
        docling_startup_timeout_seconds=1800.0,
    )

    assert rendered == "# fallback markdown\n"


def test_convert_pdf_to_markdown_docling_backend_falls_back_to_pdfium_on_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: True)

    def fake_docling(_path, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="docling", timeout=20.0)

    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown_with_docling", fake_docling)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_pdfium",
        lambda _path: "# fallback markdown\n",
    )

    rendered = convert_pdf_to_markdown_with_backend(
        Path("policy-a.pdf"),
        backend="docling",
        docling_startup_timeout_seconds=1800.0,
    )

    assert rendered == "# fallback markdown\n"


def test_convert_pdf_to_markdown_docling_backend_still_fails_for_non_timeout_docling_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: True)

    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_docling",
        lambda _path, **_kwargs: (_ for _ in ()).throw(RuntimeError("docling parse failure")),
    )

    with pytest.raises(RuntimeError, match="Docling conversion did not produce"):
        convert_pdf_to_markdown_with_backend(
            Path("policy-a.pdf"),
            backend="docling",
            docling_startup_timeout_seconds=1800.0,
        )


def test_convert_pdf_to_markdown_retries_docling_with_full_page_ocr_when_output_is_insufficient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: True)

    def fake_docling(_path, **kwargs):
        if kwargs.get("force_full_page_ocr") is True:
            return "# financing guide\n\nFinanciación de pólizas\n"
        return "<!-- image -->\n\n<!-- image -->\n\nsura\n"

    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown_with_docling", fake_docling)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_pdfium",
        lambda _path: pytest.fail("pdfium fallback should not run when OCR rerun succeeds"),
    )

    rendered = convert_pdf_to_markdown_with_backend(
        Path("policy-a.pdf"),
        backend="docling",
        docling_startup_timeout_seconds=1800.0,
    )

    assert rendered == "# financing guide\n\nFinanciación de pólizas\n"


def test_convert_pdf_to_markdown_falls_back_to_pdfium_when_docling_ocr_retry_is_still_insufficient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.pdfium_backend_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_docling",
        lambda _path, **_kwargs: "<!-- image -->\n\n<!-- image -->\n\nsura\n",
    )
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_pdfium",
        lambda _path: "# fallback markdown\n\nFinanciación de pólizas\n",
    )

    rendered = convert_pdf_to_markdown_with_backend(
        Path("policy-a.pdf"),
        backend="docling",
        docling_startup_timeout_seconds=1800.0,
    )

    assert rendered == "# fallback markdown\n\nFinanciación de pólizas\n"


def test_cli_fails_when_no_matching_pdfs_are_found(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(tmp_path / "processed" / "ingestion-manifest.jsonl"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "No PDF files matched glob" in captured.err


def test_successful_ingestion_writes_deterministic_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    markdown_output = markdown_dir / "policy-a.md"
    cleaned_markdown_output = processed_dir / "policy-a.cleaned.md"
    processed_output = processed_dir / "policy-a.json"
    chunk_output = processed_dir / "chunks" / "policy-a.chunks.json"
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())
    chunk_bundle = ChunkBundle.model_validate_json(chunk_output.read_text())

    assert exit_code == 0
    assert markdown_output.read_text(encoding="utf-8") == "# Converted policy-a"
    assert cleaned_markdown_output.read_text(encoding="utf-8") == "# Converted policy-a\n"
    assert processed_document.source_pdf_id == "policy-a"
    assert processed_document.markdown_output_path == str(markdown_output)
    assert processed_document.cleaned_markdown_output_path == str(cleaned_markdown_output)
    assert processed_document.processed_output_path == str(processed_output)
    assert processed_document.ingestion_status == "succeeded"
    assert chunk_bundle.chunk_artifact_path == str(chunk_output)
    assert chunk_bundle.chunks
    assert chunk_bundle.chunks[0].source_pdf_id == "policy-a"
    assert chunk_bundle.chunks[0].chunk_id.startswith("policy-a:v2:")
    assert chunk_bundle.chunk_schema_version == "v2"
    assert isinstance(chunk_bundle.chunks[0].section_path, list)
    assert len(manifest_records) == 1


def test_recursive_ingestion_uses_path_derived_ids(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    nested_dir = input_dir / "AUTONOMIA" / "SOLUCIONES INDIVIDUALES" / "EDUCACION"
    nested_dir.mkdir(parents=True)
    source_pdf = nested_dir / "clausulado seguro de educacion.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    source_pdf_id = derive_source_pdf_id(input_dir=input_dir, source_pdf_path=source_pdf)
    (
        markdown_output,
        cleaned_output,
        processed_output,
        chunk_output,
    ) = build_ingestion_artifact_paths(
        source_pdf_id=source_pdf_id,
        markdown_dir=markdown_dir,
        processed_dir=processed_dir,
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert markdown_output.exists()
    assert cleaned_output.exists()
    assert chunk_output.exists()
    assert processed_document.source_pdf_id == source_pdf_id
    assert processed_document.source_pdf_relative_path == (
        "AUTONOMIA/SOLUCIONES INDIVIDUALES/EDUCACION/clausulado seguro de educacion.pdf"
    )


def test_ingestion_applies_operator_curated_metadata_overlay(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    overlay_path = tmp_path / "document-metadata-overlays.json"
    source_pdf = input_dir / "ARL" / "policy-a.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    overlay_path.write_text(
        (
            '{\n'
            '  "documents": {\n'
            '    "arl__policy-a": {\n'
            '      "document_type": "policy",\n'
            '      "product": "arl"\n'
            "    }\n"
            "  }\n"
            "}\n"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            str(overlay_path),
        ]
    )

    processed_output = processed_dir / "arl__policy-a.json"
    chunk_output = processed_dir / "chunks" / "arl__policy-a.chunks.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())
    chunk_bundle = ChunkBundle.model_validate_json(chunk_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "policy"
    assert processed_document.product == "arl"
    assert chunk_bundle.document_type == "policy"
    assert chunk_bundle.product == "arl"
    assert chunk_bundle.chunks[0].document_type == "policy"
    assert chunk_bundle.chunks[0].product == "arl"


def test_ingestion_infers_product_from_source_relative_path_when_overlay_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "AUTOS" / "diferenciales planes autos.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__autos__diferenciales-planes-autos.json"
    chunk_output = (
        processed_dir / "chunks" / "movilidad__autos__diferenciales-planes-autos.chunks.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())
    chunk_bundle = ChunkBundle.model_validate_json(chunk_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "auto"
    assert chunk_bundle.product == "auto"
    assert chunk_bundle.chunks[0].product == "auto"


def test_ingestion_overlay_product_takes_precedence_over_path_inference(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    overlay_path = tmp_path / "document-metadata-overlays.json"
    source_pdf = input_dir / "MOVILIDAD" / "AUTOS" / "policy-a.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    overlay_path.write_text(
        (
            '{\n'
            '  "documents": {\n'
            '    "movilidad__autos__policy-a": {\n'
            '      "product": "moto"\n'
            "    }\n"
            "  }\n"
            "}\n"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            str(overlay_path),
        ]
    )

    processed_output = processed_dir / "movilidad__autos__policy-a.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "moto"


def test_ingestion_infers_document_type_from_source_relative_path_when_overlay_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "AUTOS" / "ayudaventas autos v2.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__autos__ayudaventas-autos-v2.json"
    chunk_output = processed_dir / "chunks" / "movilidad__autos__ayudaventas-autos-v2.chunks.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())
    chunk_bundle = ChunkBundle.model_validate_json(chunk_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "guide"
    assert chunk_bundle.document_type == "guide"
    assert chunk_bundle.chunks[0].document_type == "guide"


def test_ingestion_infers_document_type_for_diferenciales_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "AUTOS" / "diferenciales planes autos.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__autos__diferenciales-planes-autos.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "guide"


def test_ingestion_infers_document_type_for_pv_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "BICICLETAS Y PATINETAS" / "pv bicis y patinetas v2.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = (
        processed_dir / "movilidad__bicicletas-y-patinetas__pv-bicis-y-patinetas-v2.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "guide"


def test_ingestion_infers_document_type_for_comparativo_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "MOTOS" / "comparativo motos.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__motos__comparativo-motos.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "guide"
    assert processed_document.product == "moto"


def test_ingestion_infers_product_for_soat_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "SOAT" / "clausulado soat.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__soat__clausulado-soat.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "soat"
    assert processed_document.document_type == "policy"


def test_ingestion_infers_product_for_muevete_libre_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "MUEVETE LIBRE" / "clausulado muevete libre v2.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__muevete-libre__clausulado-muevete-libre-v2.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "muevete libre"
    assert processed_document.document_type == "policy"


def test_ingestion_infers_product_for_utilitarios_pesados_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "MOVILIDAD"
        / "UTILITARIO Y PESADOS"
        / "clausulado-plan utilitarios y pesados.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = (
        processed_dir
        / "movilidad__utilitario-y-pesados__clausulado-plan-utilitarios-y-pesados.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "utilitarios y pesados"
    assert processed_document.document_type == "policy"


def test_ingestion_infers_product_for_viajes_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "VIAJES" / "clausulado viaje internacional v1.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = processed_dir / "movilidad__viajes__clausulado-viaje-internacional-v1.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "viajes"
    assert processed_document.document_type == "policy"


def test_ingestion_infers_product_for_pac_source_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "clausulado pac 60 mas sura v1.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    processed_output = (
        processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "policy"


def test_repository_overlay_covers_movilidad_transversales_baseline_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "movilidad__transversales__circular-choque-simple": "guide",
        "movilidad__transversales__como-tomar-fotos-choque-simple-v2": "guide",
        "movilidad__transversales__instructivo-financiacion-de-polizas-v1": "guide",
        "movilidad__transversales__ley-2251-de-2022-choque-simple": "guide",
        "movilidad__transversales__politicas-de-suscripcion-de-movilidad": "policy",
        "movilidad__transversales__proceso-atencion-choque-simple-v2": "guide",
        "movilidad__transversales__proceso-recobro-choque-simple-v2": "guide",
        "movilidad__transversales__pv-planes-movilidad-v1": "guide",
        "movilidad__transversales__pv-portafolio-movilidad-v2": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "movilidad"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_movilidad_utilitarios_pesados_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "movilidad__utilitario-y-pesados__ayudaventas-utilitarios-y-pesados-v2": "guide",
        "movilidad__utilitario-y-pesados__clausulado-plan-utilitarios-y-pesados": "policy",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "utilitarios y pesados"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_movilidad_viajes_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "movilidad__viajes__ayudaventas-viaje-ingles-v2": "guide",
        "movilidad__viajes__ayudaventas-viajes-espanol-v2": "guide",
        "movilidad__viajes__clausulado-viaje-internacional-v1": "policy",
        "movilidad__viajes__clausulado-viaje-nacional-v1": "policy",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "viajes"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_60_mas_core_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1": "policy",
        "eps__plan-complementario-pac__politicas-asegurabilidad-pac-60-mas": "policy",
        "eps__plan-complementario-pac__preguntas-frecuentes-pac-60-mas": "faq",
        "eps__plan-complementario-pac__tarifas-pac-con-iva-2026": "guide",
        "eps__plan-complementario-pac__tips-asesores-pac-60-mas-v2": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_formularios_y_gestion_basica_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__formato-firma-cliente-pac-v1": "form",
        "eps__plan-complementario-pac__formulario-de-afiliacion-pac-v2": "form",
        "eps__plan-complementario-pac__politica-cambio-de-asesor-pac-v4": "policy",
        "eps__plan-complementario-pac__tips-medios-de-pago-v3": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_global_web_guides_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2": "guide",
        "eps__plan-complementario-pac__instructivo-descarga-carta-de-declinacion-y-pospuestos-global-web-v2": "guide",
        "eps__plan-complementario-pac__instructivo-informe-de-relacion-de-asegurados-global-web-v2": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_long_instructivos_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2": "guide",
        "eps__plan-complementario-pac__instructivo-formularios-web-novedades-pac-v6": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_policy_follow_on_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16": "policy",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_clausulado_tradicional_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1": "policy",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_repository_overlay_covers_eps_pac_canales_transaccionales_documents() -> None:
    overlay_path = Path("ops/document-metadata-overlays.json")
    overlay_payload = json.loads(overlay_path.read_text(encoding="utf-8"))
    documents = overlay_payload["documents"]

    expected_documents = {
        "eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1": "guide",
    }

    for source_pdf_id, expected_document_type in expected_documents.items():
        assert source_pdf_id in documents
        assert documents[source_pdf_id]["product"] == "pac"
        assert documents[source_pdf_id]["document_type"] == expected_document_type


def test_ingestion_applies_movilidad_viajes_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "MOVILIDAD" / "VIAJES" / "clausulado viaje nacional v1.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = processed_dir / "movilidad__viajes__clausulado-viaje-nacional-v1.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "viajes"
    assert processed_document.document_type == "policy"


def test_ingestion_applies_eps_pac_60_mas_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir / "EPS" / "PLAN COMPLEMENTARIO PAC" / "tips asesores pac 60 mas v2.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir / "eps__plan-complementario-pac__tips-asesores-pac-60-mas-v2.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "guide"


def test_ingestion_applies_eps_pac_formularios_y_gestion_basica_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = input_dir / "EPS" / "PLAN COMPLEMENTARIO PAC" / "formulario de afiliacion pac v2.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir / "eps__plan-complementario-pac__formulario-de-afiliacion-pac-v2.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "form"


def test_ingestion_applies_eps_pac_global_web_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "instructivo actualizacion correo para factura global web v2.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "eps__plan-complementario-pac__instructivo-actualizacion-correo-para-factura-global-web-v2.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "guide"


def test_ingestion_applies_eps_pac_long_instructivos_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "instructivo inclusion de asegurados cotizador v2.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "eps__plan-complementario-pac__instructivo-inclusion-de-asegurados-cotizador-v2.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "guide"


def test_ingestion_applies_eps_pac_policy_follow_on_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "politicas asegurabilidad pac v16.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "eps__plan-complementario-pac__politicas-asegurabilidad-pac-v16.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "policy"


def test_ingestion_applies_eps_pac_clausulado_tradicional_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "clausulado pac tradicional sura v1.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "eps__plan-complementario-pac__clausulado-pac-tradicional-sura-v1.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "policy"


def test_ingestion_applies_eps_pac_canales_transaccionales_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "informacion canales transaccionales y apoyo v1.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "eps__plan-complementario-pac__informacion-canales-transaccionales-y-apoyo-v1.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "pac"
    assert processed_document.document_type == "guide"


def test_ingestion_applies_movilidad_utilitarios_pesados_overlay_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "MOVILIDAD"
        / "UTILITARIO Y PESADOS"
        / "clausulado-plan utilitarios y pesados.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    processed_output = (
        processed_dir
        / "movilidad__utilitario-y-pesados__clausulado-plan-utilitarios-y-pesados.json"
    )
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.product == "utilitarios y pesados"
    assert processed_document.document_type == "policy"


def test_ingestion_overlay_document_type_takes_precedence_over_path_inference(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    overlay_path = tmp_path / "document-metadata-overlays.json"
    source_pdf = input_dir / "MOVILIDAD" / "AUTOS" / "preguntas frecuentes autos.pdf"
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")

    overlay_path.write_text(
        (
            '{\n'
            '  "documents": {\n'
            '    "movilidad__autos__preguntas-frecuentes-autos": {\n'
            '      "document_type": "policy"\n'
            "    }\n"
            "  }\n"
            "}\n"
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.stem}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            str(overlay_path),
        ]
    )

    processed_output = processed_dir / "movilidad__autos__preguntas-frecuentes-autos.json"
    processed_document = ProcessedDocument.model_validate_json(processed_output.read_text())

    assert exit_code == 0
    assert processed_document.document_type == "policy"


def test_duplicate_basenames_in_different_folders_do_not_collide(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_a = input_dir / "ARL" / "clausulado.pdf"
    source_b = input_dir / "EPS" / "PLAN COMPLEMENTARIO PAC" / "clausulado.pdf"
    source_a.parent.mkdir(parents=True)
    source_b.parent.mkdir(parents=True)
    source_a.write_bytes(b"%PDF-1.4")
    source_b.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda source_pdf_path, **_kwargs: f"# Converted {source_pdf_path.parent.name}",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    source_a_id = derive_source_pdf_id(input_dir=input_dir, source_pdf_path=source_a)
    source_b_id = derive_source_pdf_id(input_dir=input_dir, source_pdf_path=source_b)
    source_a_markdown, _, source_a_processed, source_a_chunk = build_ingestion_artifact_paths(
        source_pdf_id=source_a_id,
        markdown_dir=markdown_dir,
        processed_dir=processed_dir,
    )
    source_b_markdown, _, source_b_processed, source_b_chunk = build_ingestion_artifact_paths(
        source_pdf_id=source_b_id,
        markdown_dir=markdown_dir,
        processed_dir=processed_dir,
    )

    assert exit_code == 0
    assert source_a_id != source_b_id
    assert source_a_markdown.exists()
    assert source_b_markdown.exists()
    assert source_a_processed.exists()
    assert source_b_processed.exists()
    assert source_a_chunk.exists()
    assert source_b_chunk.exists()


def test_existing_outputs_are_skipped_when_overwrite_is_false(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")
    markdown_dir.mkdir()
    processed_dir.mkdir()
    (markdown_dir / "policy-a.md").write_text("existing markdown", encoding="utf-8")
    existing_record = ProcessedDocument(
        source_pdf_id="policy-a",
        source_pdf_path=str(source_pdf),
        source_pdf_relative_path="policy-a.pdf",
        markdown_output_path=str(markdown_dir / "policy-a.md"),
        cleaned_markdown_output_path=str(processed_dir / "policy-a.cleaned.md"),
        processed_output_path=str(processed_dir / "policy-a.json"),
        document_name="policy-a",
        document_version=None,
        ingestion_status="succeeded",
        error_message=None,
        ingested_at="2026-05-18T00:00:00Z",
    )
    (processed_dir / "policy-a.cleaned.md").write_text("existing cleaned", encoding="utf-8")
    (processed_dir / "chunks").mkdir()
    (processed_dir / "chunks" / "policy-a.chunks.json").write_text(
        ChunkBundle(
            source_pdf_id="policy-a",
            document_name="policy-a",
            document_version=None,
            source_pdf_path=str(source_pdf),
            source_pdf_relative_path="policy-a.pdf",
            cleaned_markdown_output_path=str(processed_dir / "policy-a.cleaned.md"),
            chunk_artifact_path=str(processed_dir / "chunks" / "policy-a.chunks.json"),
            chunk_size=1200,
            chunk_overlap=200,
            chunks=[],
        ).model_dump_json(indent=2),
        encoding="utf-8",
    )
    (processed_dir / "policy-a.json").write_text(
        existing_record.model_dump_json(indent=2),
        encoding="utf-8",
    )

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").read_text(encoding="utf-8") == "existing markdown"
    assert (processed_dir / "policy-a.cleaned.md").read_text(encoding="utf-8") == "existing cleaned"
    assert (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert manifest_record.ingestion_status == "skipped"


def test_existing_outputs_are_regenerated_when_metadata_is_stale(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    source_pdf = (
        input_dir
        / "EPS"
        / "PLAN COMPLEMENTARIO PAC"
        / "clausulado pac 60 mas sura v1.pdf"
    )
    source_pdf.parent.mkdir(parents=True)
    source_pdf.write_bytes(b"%PDF-1.4")
    markdown_dir.mkdir()
    processed_dir.mkdir()
    (markdown_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.md").write_text(
        "existing markdown",
        encoding="utf-8",
    )
    (processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.cleaned.md").write_text(
        "existing cleaned",
        encoding="utf-8",
    )
    (processed_dir / "chunks").mkdir()
    stale_processed = ProcessedDocument(
        source_pdf_id="eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1",
        source_pdf_path=str(source_pdf),
        source_pdf_relative_path="EPS/PLAN COMPLEMENTARIO PAC/clausulado pac 60 mas sura v1.pdf",
        markdown_output_path=str(
            markdown_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.md"
        ),
        cleaned_markdown_output_path=str(
            processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.cleaned.md"
        ),
        processed_output_path=str(
            processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.json"
        ),
        document_name="Stale Policy",
        document_version=None,
        document_type=None,
        product=None,
        ingestion_status="succeeded",
        error_message=None,
        ingested_at="2026-05-18T00:00:00Z",
    )
    stale_chunk_bundle = ChunkBundle(
        source_pdf_id="eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1",
        document_name="Stale Policy",
        document_version=None,
        document_type=None,
        product=None,
        source_pdf_path=str(source_pdf),
        source_pdf_relative_path="EPS/PLAN COMPLEMENTARIO PAC/clausulado pac 60 mas sura v1.pdf",
        cleaned_markdown_output_path=str(
            processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.cleaned.md"
        ),
        chunk_artifact_path=str(
            processed_dir
            / "chunks"
            / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.chunks.json"
        ),
        chunk_size=1200,
        chunk_overlap=200,
        chunks=[],
    )
    (
        processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.json"
    ).write_text(stale_processed.model_dump_json(indent=2), encoding="utf-8")
    (
        processed_dir
        / "chunks"
        / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.chunks.json"
    ).write_text(stale_chunk_bundle.model_dump_json(indent=2), encoding="utf-8")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Plan Complementario 60 más\n\n## 1. OBJETO DEL CONTRATO\n\nCobertura del plan.",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--metadata-overlay-path",
            "ops/document-metadata-overlays.json",
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )
    refreshed_processed = ProcessedDocument.model_validate_json(
        (
            processed_dir / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.json"
        ).read_text(encoding="utf-8")
    )
    refreshed_chunk_bundle = ChunkBundle.model_validate_json(
        (
            processed_dir
            / "chunks"
            / "eps__plan-complementario-pac__clausulado-pac-60-mas-sura-v1.chunks.json"
        ).read_text(encoding="utf-8")
    )

    assert exit_code == 0
    assert manifest_record.ingestion_status == "succeeded"
    assert refreshed_processed.document_type == "policy"
    assert refreshed_processed.product == "pac"
    assert refreshed_chunk_bundle.document_type == "policy"
    assert refreshed_chunk_bundle.product == "pac"


def test_overwrite_true_regenerates_outputs(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")
    markdown_dir.mkdir()
    processed_dir.mkdir()
    (markdown_dir / "policy-a.md").write_text("stale markdown", encoding="utf-8")
    (processed_dir / "policy-a.cleaned.md").write_text("stale cleaned", encoding="utf-8")
    (processed_dir / "chunks").mkdir()
    (processed_dir / "chunks" / "policy-a.chunks.json").write_text("{}", encoding="utf-8")
    (processed_dir / "policy-a.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Fresh markdown",
    )

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
            "--overwrite",
            "true",
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").read_text(encoding="utf-8") == "# Fresh markdown"
    assert (
        processed_dir / "policy-a.cleaned.md"
    ).read_text(encoding="utf-8") == "# Fresh markdown\n"
    assert (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert manifest_record.ingestion_status == "succeeded"


def test_manifest_is_append_only_across_reruns(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# First markdown",
    )

    first_exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    second_exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_records = [
        ProcessedDocument.model_validate_json(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]

    assert first_exit_code == 0
    assert second_exit_code == 0
    assert len(manifest_records) == 2
    assert [record.ingestion_status for record in manifest_records] == ["succeeded", "skipped"]


def test_cleaning_failure_records_failed_manifest_and_no_cleaned_artifacts(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Raw markdown",
    )

    def fail_cleaning(_: str) -> str:
        raise RuntimeError("cleaning failed")

    monkeypatch.setattr("rag.ingestion.clean_markdown", fail_cleaning)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "cleaning failed"


def test_chunk_generation_failure_records_failed_manifest_and_no_chunk_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Raw markdown",
    )

    def fail_chunk_build(*args, **kwargs):
        raise RuntimeError("chunk generation failed")

    monkeypatch.setattr("rag.ingestion.build_chunk_bundle", fail_chunk_build)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert not (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "chunk generation failed"


def test_refined_chunk_generation_failure_records_failed_manifest_and_no_chunk_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    input_dir = tmp_path / "raw"
    markdown_dir = tmp_path / "markdown"
    processed_dir = tmp_path / "processed"
    manifest_path = processed_dir / "ingestion-manifest.jsonl"
    input_dir.mkdir()
    source_pdf = input_dir / "policy-a.pdf"
    source_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Policy Title\n\n## Coverage\n\nCoverage applies.",
    )

    def fail_refined_chunk_generation(*args, **kwargs):
        raise RuntimeError("refined chunk generation failed")

    monkeypatch.setattr("rag.ingestion.build_chunk_records", fail_refined_chunk_generation)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(markdown_dir),
            "--processed-dir",
            str(processed_dir),
            "--manifest-path",
            str(manifest_path),
        ]
    )

    manifest_record = ProcessedDocument.model_validate_json(
        manifest_path.read_text(encoding="utf-8").splitlines()[0]
    )

    assert exit_code == 0
    assert (markdown_dir / "policy-a.md").exists()
    assert not (processed_dir / "chunks" / "policy-a.chunks.json").exists()
    assert not (processed_dir / "policy-a.json").exists()
    assert not (processed_dir / "policy-a.cleaned.md").exists()
    assert manifest_record.ingestion_status == "failed"
    assert manifest_record.error_message == "refined chunk generation failed"


def test_fail_fast_true_stops_after_first_cleaning_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_backend",
        lambda _source_pdf_path, **_kwargs: "# Raw markdown",
    )

    def fail_cleaning(_: str) -> str:
        raise RuntimeError("cleaning failed")

    monkeypatch.setattr("rag.ingestion.clean_markdown", fail_cleaning)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
            "--fail-fast",
            "true",
        ]
    )
    captured = capsys.readouterr()
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()

    assert exit_code == 1
    assert "Failed to ingest policy-a.pdf: cleaning failed" in captured.err
    assert len(manifest_records) == 1
    assert ProcessedDocument.model_validate_json(manifest_records[0]).ingestion_status == "failed"


def test_fail_fast_false_records_failures_and_continues(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    def fake_convert(source_pdf_path, **_kwargs):
        if source_pdf_path.stem == "policy-a":
            raise RuntimeError("conversion failed")
        return "# Converted"

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown_with_backend", fake_convert)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
        ]
    )
    captured = capsys.readouterr()
    manifest_records = [
        ProcessedDocument.model_validate_json(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
    ]

    assert exit_code == 0
    assert "Failed to ingest policy-a.pdf" in captured.err
    assert [record.ingestion_status for record in manifest_records] == ["failed", "succeeded"]


def test_fail_fast_true_stops_after_first_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    (input_dir / "policy-a.pdf").write_bytes(b"%PDF-1.4")
    (input_dir / "policy-b.pdf").write_bytes(b"%PDF-1.4")
    manifest_path = tmp_path / "processed" / "ingestion-manifest.jsonl"

    def fake_convert(_source_pdf_path, **_kwargs):
        raise RuntimeError("conversion failed")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr("rag.ingestion.convert_pdf_to_markdown_with_backend", fake_convert)

    exit_code = main(
        [
            "ingest-pdfs",
            "--input-dir",
            str(input_dir),
            "--markdown-dir",
            str(tmp_path / "markdown"),
            "--processed-dir",
            str(tmp_path / "processed"),
            "--manifest-path",
            str(manifest_path),
            "--fail-fast",
            "true",
        ]
    )
    captured = capsys.readouterr()
    manifest_records = manifest_path.read_text(encoding="utf-8").splitlines()

    assert exit_code == 1
    assert "Failed to ingest policy-a.pdf" in captured.err
    assert len(manifest_records) == 1
    assert ProcessedDocument.model_validate_json(manifest_records[0]).ingestion_status == "failed"


def test_docling_warmup_runs_on_sample_pdf(
    monkeypatch: pytest.MonkeyPatch, tmp_path, capsys
) -> None:
    sample_pdf = tmp_path / "sample.pdf"
    sample_pdf.write_bytes(b"%PDF-1.4")

    monkeypatch.setattr("rag.ingestion.docling_is_available", lambda: True)
    monkeypatch.setattr(
        "rag.ingestion.convert_pdf_to_markdown_with_docling",
        lambda _path, **_kwargs: "# Warmed markdown\n",
    )

    exit_code = main(
        [
            "warmup-docling-assets",
            "--sample-pdf",
            str(sample_pdf),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Docling warm-up succeeded" in captured.out


def test_processed_document_requires_error_message_for_failed_status() -> None:
    with pytest.raises(ValueError):
        ProcessedDocument(
            source_pdf_id="policy-a",
            source_pdf_path="data/raw/policy-a.pdf",
            source_pdf_relative_path="policy-a.pdf",
            markdown_output_path="data/markdown/policy-a.md",
            cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
            processed_output_path="data/processed/policy-a.json",
            document_name="policy-a",
            document_version=None,
            ingestion_status="failed",
            error_message=None,
            ingested_at="2026-05-18T00:00:00Z",
        )


def test_processed_document_rejects_invalid_ingestion_status() -> None:
    with pytest.raises(ValueError):
        ProcessedDocument(
            source_pdf_id="policy-a",
            source_pdf_path="data/raw/policy-a.pdf",
            source_pdf_relative_path="policy-a.pdf",
            markdown_output_path="data/markdown/policy-a.md",
            cleaned_markdown_output_path="data/processed/policy-a.cleaned.md",
            processed_output_path="data/processed/policy-a.json",
            document_name="policy-a",
            document_version=None,
            ingestion_status="completed",
            error_message=None,
            ingested_at="2026-05-18T00:00:00Z",
        )
