"""Markdown normalization and semantic block grouping helpers."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from rag.term_equivalences import normalize_equivalence_text, tokenize_lexical_surface

CLAUSE_LIKE_PATTERN = re.compile(r"^(?:\d+[.)]|[A-Z][.)]|[IVXLCDM]+[.)])(?:\s+\S.*)?$")
MAX_STRUCTURAL_BLOCK_LENGTH = 120
MARKDOWN_TABLE_SEPARATOR_PATTERN = re.compile(r"^\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$")
PAGE_HEADING_PATTERN = re.compile(r"(?i)^page\s+\d+$")
SEMANTIC_SECTION_LABELS = (
    "propuesta de valor",
    "coberturas y planes",
    "generalidades",
    "expedición requisitos",
    "deducible",
    "asunto choque simple",
    "artículo 16 — daños materiales",
    "informe policial y recaudo probatorio",
    "instrucciones operativas choque simple",
)
ARL_RUI_FAQ_QUESTION_PATTERN = re.compile(r"^(?P<number>\d+)\.\s*(?P<question>.+)$")
CHOQUE_SIMPLE_BOILERPLATE_PATTERNS = (
    "documentofirmadodigitalmenteporelministeriodetransporte",
    "www.mintransporte.gov.co",
    "powered by tcpdf",
    "ministerio de transporte",
    "radicado no.",
    "radicado no",
    "para:",
    "de:",
    "fecha:",
)
PV_SLOGAN_NORMALIZED_LINES = {
    "sentirte acompanado",
    "ahorrar tiempo",
    "ahorrar dinero",
}
SUSCRIPCION_TOP_LEVEL_HEADING_PATTERN = re.compile(r"^(?P<number>\d{1,2})\.?\s+(?P<title>.+)$")
SUSCRIPCION_SUBSECTION_HEADING_PATTERN = re.compile(
    r"^(?P<number>\d{1,2}\.\d{1,2})\.?\s+(?P<title>.+)$"
)
SUSCRIPCION_NESTED_SUBSECTION_HEADING_PATTERN = re.compile(
    r"^(?P<number>\d{1,2}\.\d{1,2}\.\d{1,2})\.?\s+(?P<title>.+)$"
)
SUSCRIPCION_PAGE_HEADING_PATTERN = re.compile(r"^##\s+Page\s+\d+\s*$", re.IGNORECASE)
SUSCRIPCION_TOC_ENTRY_PATTERN = re.compile(
    r"^\d{1,2}(?:\.\d{1,2})?\.?\s+.+\.{5,}\s*\d+\s*$"
)
MUEVETE_LIBRE_ROOT_HEADING_PATTERN = re.compile(
    r"^#+\s+PLAN\s+MU[EÉ]VETE\s+LIBRE\s*$",
    re.IGNORECASE,
)
MUEVETE_LIBRE_SECTION_GROUP_PATTERN = re.compile(
    r"^SECCI[ÓO]N\s+\d+\s+.+$",
    re.IGNORECASE,
)
MUEVETE_LIBRE_TOP_LEVEL_HEADING_PATTERN = re.compile(r"^\d+\.\s+.+$")
MUEVETE_LIBRE_SUBSECTION_HEADING_PATTERN = re.compile(r"^\d+\.\d+\.?\s+.+$")
MUEVETE_LIBRE_LITERAL_SUBSECTION_PATTERN = re.compile(r"^[a-z]\)\s+.+$", re.IGNORECASE)
NORMALIZED_SEMANTIC_SECTION_LABELS = {
    normalize_equivalence_text(label) for label in SEMANTIC_SECTION_LABELS
}


@dataclass(frozen=True)
class MarkdownBlock:
    """One deterministic cleaned-markdown block with structural context."""

    text: str
    section: str | None
    section_path: tuple[str, ...]
    kind: str


def suscripcion_heading_has_uppercase_surface(value: str) -> bool:
    """Return whether one suscripción heading candidate has heading-like casing."""

    alphabetic_characters = [character for character in value if character.isalpha()]
    if not alphabetic_characters:
        return False
    uppercase_characters = sum(character.isupper() for character in alphabetic_characters)
    return (uppercase_characters / len(alphabetic_characters)) >= 0.6


def normalize_suscripcion_policy_markdown(cleaned_markdown_text: str) -> str:
    """Normalize the suscripción policy fallback surface into semantic headings."""

    raw_lines = cleaned_markdown_text.splitlines()
    root_heading = "# politicas de suscripcion de movilidad"
    version_line: str | None = None
    normalized_lines: list[str] = [root_heading]
    started_semantic_body = False
    current_subsection_number: str | None = None

    def append_line(line: str) -> None:
        stripped_line = line.strip()
        if not stripped_line:
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            return
        if normalized_lines and normalized_lines[-1] == stripped_line:
            return
        normalized_lines.append(stripped_line)

    def append_numbered_heading(level: str, number: str, title: str) -> None:
        append_line("")
        append_line(f"{level} {number}. {title.strip()}")

    def rewrite_collective_nested_subsection_heading(
        *,
        number: str,
        title: str,
    ) -> tuple[str, str] | None:
        if current_subsection_number not in {"14.6", "14.6.1", "14.6.2"}:
            return None
        if number == "2.1":
            return ("14.6.1", title)
        if number == "2.2":
            return ("14.6.2", title)
        return None

    for raw_line in raw_lines:
        stripped_line = raw_line.strip()
        normalized_line = normalize_equivalence_text(stripped_line)
        if not stripped_line:
            continue
        if stripped_line.startswith("# politicas de suscripcion de movilidad"):
            continue
        if SUSCRIPCION_PAGE_HEADING_PATTERN.match(stripped_line):
            continue
        if normalized_line in {"volver", "al inicio", "tabla de contenido"}:
            continue
        if re.fullmatch(r"\d+", stripped_line):
            continue
        if SUSCRIPCION_TOC_ENTRY_PATTERN.match(stripped_line):
            continue
        if version_line is None and "version" in normalized_line:
            version_line = stripped_line
            continue
        if not started_semantic_body:
            nested_subsection_match = SUSCRIPCION_NESTED_SUBSECTION_HEADING_PATTERN.match(
                stripped_line
            )
            if nested_subsection_match is not None and len(stripped_line) <= 140:
                started_semantic_body = True
                current_subsection_number = nested_subsection_match.group("number")
                append_numbered_heading(
                    "####",
                    nested_subsection_match.group("number"),
                    nested_subsection_match.group("title"),
                )
                continue
            subsection_match = SUSCRIPCION_SUBSECTION_HEADING_PATTERN.match(stripped_line)
            if subsection_match is not None:
                started_semantic_body = True
                current_subsection_number = subsection_match.group("number")
                append_numbered_heading(
                    "###",
                    subsection_match.group("number"),
                    subsection_match.group("title"),
                )
                continue
            top_level_match = SUSCRIPCION_TOP_LEVEL_HEADING_PATTERN.match(stripped_line)
            if (
                top_level_match is not None
                and len(stripped_line) <= 100
                and suscripcion_heading_has_uppercase_surface(top_level_match.group("title"))
            ):
                started_semantic_body = True
                current_subsection_number = None
                append_numbered_heading(
                    "##",
                    top_level_match.group("number"),
                    top_level_match.group("title"),
                )
                continue
            continue

        nested_subsection_match = SUSCRIPCION_NESTED_SUBSECTION_HEADING_PATTERN.match(
            stripped_line
        )
        if nested_subsection_match is not None and len(stripped_line) <= 140:
            current_subsection_number = nested_subsection_match.group("number")
            append_numbered_heading(
                "####",
                nested_subsection_match.group("number"),
                nested_subsection_match.group("title"),
            )
            continue

        subsection_match = SUSCRIPCION_SUBSECTION_HEADING_PATTERN.match(stripped_line)
        if subsection_match is not None and len(stripped_line) <= 120:
            rewritten_nested_subsection = rewrite_collective_nested_subsection_heading(
                number=subsection_match.group("number"),
                title=subsection_match.group("title"),
            )
            if rewritten_nested_subsection is not None:
                current_subsection_number = rewritten_nested_subsection[0]
                append_numbered_heading(
                    "####",
                    rewritten_nested_subsection[0],
                    rewritten_nested_subsection[1],
                )
                continue
            current_subsection_number = subsection_match.group("number")
            append_numbered_heading(
                "###",
                subsection_match.group("number"),
                subsection_match.group("title"),
            )
            continue

        top_level_match = SUSCRIPCION_TOP_LEVEL_HEADING_PATTERN.match(stripped_line)
        if (
            top_level_match is not None
            and len(stripped_line) <= 100
            and suscripcion_heading_has_uppercase_surface(top_level_match.group("title"))
        ):
            current_subsection_number = None
            append_numbered_heading(
                "##",
                top_level_match.group("number"),
                top_level_match.group("title"),
            )
            continue
        append_line(stripped_line)

    if version_line is not None:
        normalized_lines.insert(1, "")
        normalized_lines.insert(2, version_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def normalize_choque_simple_process_markdown(
    cleaned_markdown_text: str,
    *,
    root_heading: str,
    drop_leading_lines: set[str] | None = None,
) -> str:
    """Promote one stable root heading and trim noisy preamble lines."""

    normalized_drop_lines = {
        normalize_equivalence_text(line) for line in (drop_leading_lines or set())
    }
    raw_lines = cleaned_markdown_text.splitlines()
    normalized_lines: list[str] = []
    emitted_root_heading = False
    skipped_leading_noise = False

    def emit_root_heading() -> None:
        nonlocal emitted_root_heading
        if emitted_root_heading:
            return
        normalized_lines.append(f"# {root_heading}")
        emitted_root_heading = True

    for raw_line in raw_lines:
        stripped_line = raw_line.strip()
        normalized_line = normalize_equivalence_text(stripped_line.lstrip("#").strip())

        if not stripped_line:
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            continue

        if not skipped_leading_noise and normalized_line in normalized_drop_lines:
            skipped_leading_noise = True
            continue

        if normalized_line == normalize_equivalence_text(root_heading):
            emit_root_heading()
            continue

        if stripped_line.startswith("#"):
            emit_root_heading()
            normalized_lines.append(raw_line)
            continue

        emit_root_heading()
        normalized_lines.append(raw_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def normalize_muevete_libre_markdown(cleaned_markdown_text: str) -> str:
    """Rewrite the Muévete Libre clausulado into a semantic heading hierarchy."""

    normalized_lines: list[str] = ["# PLAN MUÉVETE LIBRE"]
    emitted_root = True

    def append_line(line: str) -> None:
        stripped_line = line.strip()
        if not stripped_line:
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            return
        if normalized_lines and normalized_lines[-1] == stripped_line:
            return
        normalized_lines.append(stripped_line)

    def append_heading(level: str, heading_text: str) -> None:
        append_line("")
        append_line(f"{level} {heading_text.strip()}")

    for raw_line in cleaned_markdown_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            append_line("")
            continue

        if MUEVETE_LIBRE_ROOT_HEADING_PATTERN.match(stripped_line):
            if not emitted_root:
                append_line("# PLAN MUÉVETE LIBRE")
                emitted_root = True
            continue

        heading_candidate = stripped_line.lstrip("#").strip()
        if not heading_candidate:
            continue

        if MUEVETE_LIBRE_SECTION_GROUP_PATTERN.match(heading_candidate):
            append_heading("##", heading_candidate)
            continue

        if MUEVETE_LIBRE_SUBSECTION_HEADING_PATTERN.match(heading_candidate):
            append_heading("####", heading_candidate)
            continue

        if MUEVETE_LIBRE_TOP_LEVEL_HEADING_PATTERN.match(heading_candidate):
            append_heading("###", heading_candidate)
            continue

        if MUEVETE_LIBRE_LITERAL_SUBSECTION_PATTERN.match(heading_candidate):
            append_heading("#####", heading_candidate)
            continue

        append_line(heading_candidate if stripped_line.startswith("#") else stripped_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def normalize_arl_rui_faq_markdown(cleaned_markdown_text: str) -> str:
    """Rewrite the ARL/RUI FAQ into semantic question-led markdown."""

    normalized_lines: list[str] = ["# Preguntas frecuentes registro único de intermediación - RUI"]
    seen_first_question = False
    skipping_portal_block = False

    def append_line(line: str) -> None:
        if not line:
            if normalized_lines[-1] != "":
                normalized_lines.append("")
            return
        normalized_lines.append(line)

    for raw_line in cleaned_markdown_text.splitlines():
        stripped_line = raw_line.strip()
        normalized_line = normalize_equivalence_text(stripped_line.lstrip("#").strip())

        if not stripped_line:
            append_line("")
            continue

        question_match = ARL_RUI_FAQ_QUESTION_PATTERN.match(
            stripped_line.lstrip("#").strip()
        )
        if question_match is not None and "?" in question_match.group("question"):
            if normalized_lines[-1] != "":
                normalized_lines.append("")
            normalized_lines.append(
                f"## {question_match.group('number')}. {question_match.group('question').strip()}"
            )
            seen_first_question = True
            skipping_portal_block = False
            continue

        if normalized_line in {"preguntas", "preguntas:"}:
            continue

        portal_block_markers = {
            "grabacion https player vimeo com video 943790015",
            "iregistro unico de intermediarios consulte aqui el estado de su registro",
            "ministeriodeltrabajo",
            "ingresa al rui",
            "descargue aqui el rul con corte a 14marzo de 2025",
            "regresar",
        }
        if normalized_line in portal_block_markers or normalized_line.startswith("link"):
            skipping_portal_block = True
            continue

        if skipping_portal_block and (
            stripped_line.startswith("|")
            or MARKDOWN_TABLE_SEPARATOR_PATTERN.match(stripped_line) is not None
        ):
            continue

        if skipping_portal_block:
            continue

        if not seen_first_question and stripped_line.startswith("#"):
            continue

        append_line(stripped_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def compact_alphanumeric_text(value: str) -> str:
    """Return one lowercased alphanumeric-only surface for noisy OCR matching."""

    normalized_value = normalize_equivalence_text(value)
    return "".join(character for character in normalized_value if character.isalnum())


def normalize_arl_commissions_guide_markdown(cleaned_markdown_text: str) -> str:
    """Remove narrow portal boilerplate from the ARL commissions guide."""

    normalized_lines: list[str] = []
    ignored_compact_surfaces = {
        "capacidadarl",
        "sura",
        "surasura",
    }

    for raw_line in cleaned_markdown_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            continue

        compact_surface = compact_alphanumeric_text(stripped_line.strip("[]"))
        if compact_surface in ignored_compact_surfaces:
            continue

        normalized_lines.append(stripped_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def normalize_known_document_markdown(
    *,
    source_pdf_path: Path,
    cleaned_markdown_text: str,
) -> str:
    """Apply narrow document-specific markdown normalization for known noisy guides."""

    normalized_stem = normalize_equivalence_text(source_pdf_path.stem)
    if "preguntas frecuentes registro unico de intermediacion" in normalized_stem:
        return normalize_arl_rui_faq_markdown(cleaned_markdown_text)
    if "instructivos consulta de comisiones arl sura" in normalized_stem:
        return normalize_arl_commissions_guide_markdown(cleaned_markdown_text)
    if "politicas de suscripcion de movilidad" in normalized_stem:
        return normalize_suscripcion_policy_markdown(cleaned_markdown_text)
    if "clausulado muevete libre" in normalized_stem:
        return normalize_muevete_libre_markdown(cleaned_markdown_text)
    if "proceso atencion choque simple" in normalized_stem:
        return normalize_choque_simple_process_markdown(
            cleaned_markdown_text,
            root_heading="EN EVENTOS DE CHOQUES",
            drop_leading_lines={"Normatividad vigente"},
        )
    if "proceso recobro choque simple" in normalized_stem:
        return normalize_choque_simple_process_markdown(
            cleaned_markdown_text,
            root_heading="Servicios de recobro para accidentes",
        )
    if "como tomar fotos choque simple" not in normalized_stem:
        return cleaned_markdown_text

    normalized_lines: list[str] = []
    replaced_root_heading = False

    for raw_line in cleaned_markdown_text.splitlines():
        stripped_line = raw_line.strip()
        normalized_line = normalize_equivalence_text(stripped_line.lstrip("#").strip())
        tokenized_line = tokenize_lexical_surface(stripped_line.lstrip("#").strip())

        if (
            stripped_line.startswith("#")
            and normalized_line
            == "estas recomendaciones para en un choque simple ten en cuenta tomar fotos y videos"
        ):
            if not replaced_root_heading:
                normalized_lines.append("# ¿Cómo tomar fotos y videos?")
                replaced_root_heading = True
            continue

        if stripped_line.startswith("#") and tokenized_line == {"como", "tomar", "fotos", "videos"}:
            continue

        if stripped_line == "segurossura.com.co":
            continue
        if stripped_line.startswith("#") and normalized_line in {
            "asegurate de vivir",
            "asegúrate de vivir",
        }:
            continue

        normalized_lines.append(raw_line)

    normalized_text = "\n".join(normalized_lines).strip()
    if not normalized_text:
        return cleaned_markdown_text
    return f"{normalized_text}\n"


def detect_block_kind(block_text: str) -> str:
    """Classify a cleaned-markdown block using deterministic local rules."""

    first_line = block_text.splitlines()[0].strip()
    if first_line.startswith("#"):
        return "heading"
    if "\n" not in block_text and CLAUSE_LIKE_PATTERN.match(first_line):
        return "clause_marker"
    return "paragraph"


def parse_markdown_table_row(line: str) -> list[str] | None:
    """Parse one markdown table row into stripped cells."""

    stripped_line = line.strip()
    if "|" not in stripped_line:
        return None
    trimmed_line = stripped_line.strip("|")
    if not trimmed_line:
        return None
    return [cell.strip() for cell in trimmed_line.split("|")]


def is_markdown_table_separator(line: str) -> bool:
    """Return whether one line is a markdown table separator row."""

    return MARKDOWN_TABLE_SEPARATOR_PATTERN.match(line.strip()) is not None


def normalize_table_cell_text(value: str) -> str:
    """Normalize one markdown-table cell into compact semantic text."""

    normalized_value = re.sub(r"\s*[•·]\s*", "; ", value.strip())
    normalized_value = re.sub(r"\s+", " ", normalized_value)
    normalized_value = re.sub(r";\s*;", ";", normalized_value)
    return normalized_value.strip(" ;")


def normalize_comparison_table_block(block_text: str) -> str:
    """Rewrite comparison-oriented markdown tables into plan-centric statements."""

    lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    if len(lines) < 3:
        return block_text
    header_cells = parse_markdown_table_row(lines[0])
    if header_cells is None or not is_markdown_table_separator(lines[1]):
        return block_text
    if len(header_cells) < 3:
        return block_text

    normalized_header_cells = [normalize_table_cell_text(cell) for cell in header_cells]
    plan_labels = [
        header_cell
        for header_cell in normalized_header_cells[1:]
        if header_cell.casefold().startswith("plan ")
    ]
    if len(plan_labels) < 2:
        return block_text

    plan_attributes: dict[str, list[str]] = {}
    plan_order: list[str] = []

    for raw_row in lines[2:]:
        row_cells = parse_markdown_table_row(raw_row)
        if row_cells is None:
            return block_text
        if len(row_cells) < len(normalized_header_cells):
            row_cells = [*row_cells, *([""] * (len(normalized_header_cells) - len(row_cells)))]

        row_label = normalize_table_cell_text(row_cells[0])
        if not row_label:
            continue

        for plan_label, cell_value in zip(normalized_header_cells[1:], row_cells[1:], strict=False):
            if not plan_label.casefold().startswith("plan "):
                continue
            normalized_cell_value = normalize_table_cell_text(cell_value)
            if not normalized_cell_value:
                continue
            if plan_label not in plan_attributes:
                plan_attributes[plan_label] = []
                plan_order.append(plan_label)
            statement = f"- {row_label}: {normalized_cell_value}"
            if statement not in plan_attributes[plan_label]:
                plan_attributes[plan_label].append(statement)

    if not plan_attributes:
        return block_text

    normalized_sections: list[str] = []
    for plan_label in plan_order:
        plan_statements = plan_attributes.get(plan_label, [])
        if not plan_statements:
            continue
        normalized_sections.append(plan_label)
        normalized_sections.extend(plan_statements)
        normalized_sections.append("")

    if normalized_sections and normalized_sections[-1] == "":
        normalized_sections.pop()
    return "\n\n".join(normalized_sections)


def is_page_heading_text(value: str) -> bool:
    """Return whether one heading text is a plain page marker."""

    return PAGE_HEADING_PATTERN.match(value.strip()) is not None


def find_semantic_section_label(block_text: str) -> str | None:
    """Return a stronger semantic section label when present in a block."""

    for raw_line in block_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized_line = normalize_equivalence_text(line)
        if normalized_line in NORMALIZED_SEMANTIC_SECTION_LABELS:
            return line
    return None


def normalize_diagrammatic_coverage_block(block_text: str) -> str:
    """Rewrite line-grid coverage blocks into more semantic statements."""

    semantic_label = find_semantic_section_label(block_text)
    if normalize_equivalence_text(semantic_label or "") != "coberturas y planes":
        return block_text

    raw_lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    content_lines = [
        line
        for line in raw_lines
        if "todos los derechos reservados" not in normalize_equivalence_text(line)
        and normalize_equivalence_text(line) != "coberturas y planes"
    ]
    if len(content_lines) < 4:
        return block_text

    statements: list[str] = []
    index = 0
    while index < len(content_lines):
        label = content_lines[index]
        normalized_label = normalize_equivalence_text(label)
        if not label or normalized_label == "asistencia":
            index += 1
            continue
        if len(label) > 40 or label.startswith(("Con ", "de ", "$")):
            index += 1
            continue

        continuation_lines: list[str] = []
        cursor = index + 1
        while cursor < len(content_lines):
            candidate = content_lines[cursor]
            normalized_candidate = normalize_equivalence_text(candidate)
            if normalized_candidate in SEMANTIC_SECTION_LABELS:
                break
            if len(candidate) <= 40 and not candidate.startswith(("Con ", "de ", "$")):
                if continuation_lines:
                    break
                if candidate and candidate[0].islower():
                    label = f"{label} {candidate}"
                    cursor += 1
                    continue
                break
            continuation_lines.append(candidate)
            cursor += 1

        if continuation_lines:
            normalized_value = normalize_table_cell_text(" ".join(continuation_lines))
            statements.append(f"- {label}: {normalized_value}")
            index = cursor
            continue
        index += 1

    if not statements:
        return block_text
    return "COBERTURAS Y PLANES\n" + "\n".join(statements)


def normalize_expedition_requirements_block(block_text: str) -> str:
    """Rewrite the expedition requirements line-grid into statement-style text."""

    semantic_label = normalize_equivalence_text(find_semantic_section_label(block_text) or "")
    if semantic_label != "expedicion requisitos":
        return block_text

    raw_lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    content_lines = [
        line
        for line in raw_lines
        if "todos los derechos reservados" not in normalize_equivalence_text(line)
        and "actualizado al 2025" not in normalize_equivalence_text(line)
        and normalize_equivalence_text(line) != "expedicion requisitos"
    ]
    if "Requisitos Vinculaciones" not in content_lines:
        return block_text

    statements: list[str] = []
    current_product: str | None = None
    index = 0
    while index < len(content_lines):
        line = content_lines[index]
        normalized_line = normalize_equivalence_text(line)
        if normalized_line in {"bicis", "patinetas"}:
            current_product = line
            index += 1
            continue
        if not line.startswith("Entre $"):
            index += 1
            continue

        range_parts = [line]
        cursor = index + 1
        while cursor < len(content_lines) and not content_lines[cursor].startswith("•"):
            candidate = content_lines[cursor]
            normalized_candidate = normalize_equivalence_text(candidate)
            if normalized_candidate in {"bicis", "patinetas"}:
                break
            if candidate.startswith("Entre $"):
                break
            range_parts.append(candidate)
            cursor += 1

        requirement_parts: list[str] = []
        while cursor < len(content_lines):
            candidate = content_lines[cursor]
            normalized_candidate = normalize_equivalence_text(candidate)
            if normalized_candidate in {"bicis", "patinetas"}:
                break
            if candidate.startswith("Entre $"):
                break
            if (
                requirement_parts
                and not candidate.startswith("•")
                and "vinculaciones minimas" not in normalized_candidate
                and "todos los clientes" not in normalized_candidate
                and not candidate.startswith(("de $", "$"))
            ):
                break
            requirement_parts.append(candidate)
            cursor += 1

        if current_product and requirement_parts:
            normalized_range = normalize_table_cell_text(" ".join(range_parts))
            normalized_requirements = normalize_table_cell_text(" ".join(requirement_parts))
            statements.append(
                f"- {current_product} / {normalized_range}: {normalized_requirements}"
            )
        index = cursor

    if not statements:
        return block_text
    return "EXPEDICIÓN REQUISITOS\n" + "\n".join(statements)


def normalize_deductible_block(block_text: str) -> str:
    """Rewrite the deductible line-grid into statement-style text."""

    semantic_label = normalize_equivalence_text(find_semantic_section_label(block_text) or "")
    if semantic_label != "deducible":
        return block_text

    raw_lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    content_lines = [
        line
        for line in raw_lines
        if "todos los derechos reservados" not in normalize_equivalence_text(line)
        and normalize_equivalence_text(line) != "deducible"
    ]
    current_product: str | None = None
    statements: list[str] = []
    index = 0
    while index < len(content_lines):
        line = content_lines[index]
        normalized_line = normalize_equivalence_text(line)
        if normalized_line in {"bicis", "patinetas"}:
            current_product = line
            index += 1
            continue
        if not line.startswith("Entre $"):
            index += 1
            continue

        row_parts = [line]
        cursor = index + 1
        while cursor < len(content_lines):
            candidate = content_lines[cursor]
            normalized_candidate = normalize_equivalence_text(candidate)
            if normalized_candidate in {"bicis", "patinetas"}:
                break
            if candidate.startswith("Entre $"):
                break
            if normalized_candidate.startswith("es el valor que"):
                break
            row_parts.append(candidate)
            cursor += 1

        if current_product and len(row_parts) > 1:
            normalized_row = normalize_table_cell_text(" ".join(row_parts))
            statements.append(f"- {current_product}: {normalized_row}")
        index = cursor

    if not statements:
        return block_text
    return "DEDUCIBLE\n" + "\n".join(statements)


def normalize_choque_simple_circular_block(block_text: str) -> str:
    """Rewrite choque-simple circular blocks into more semantic evidence sections."""

    raw_lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    if not raw_lines:
        return block_text

    content_lines = [
        line
        for line in raw_lines
        if not any(
            pattern in normalize_equivalence_text(line)
            for pattern in CHOQUE_SIMPLE_BOILERPLATE_PATTERNS
        )
        and normalize_equivalence_text(line)
        not in {"circular externa", "bogota d.c.", "*20224000000057*"}
        and not re.fullmatch(r"\d{2}-\d{2}-\d{4}", line)
        and not re.fullmatch(r"\d{11,}", line)
    ]
    if not content_lines:
        return ""

    normalized_block = "\n".join(content_lines)
    normalized_surface = normalize_equivalence_text(normalized_block)

    if normalized_surface in {"para:", "de:"}:
        return ""
    if normalized_surface.startswith("gobernadores alcaldes organismos de transito"):
        return ""
    if "director de transporte y transito" in normalized_surface and len(normalized_surface) < 120:
        return ""
    if normalized_surface == "asunto:":
        return "ASUNTO CHOQUE SIMPLE"

    if (
        "articulo 16 de la ley 2251 de 2022" in normalized_surface
        and (
            "asunto:" in normalized_surface
            or "instrucciones para el cumplimiento del articulo 16" in normalized_surface
        )
    ):
        return "ASUNTO CHOQUE SIMPLE\n" + normalized_block
    if (
        "articulo 16." in normalized_surface
        or "articulo 143. danos materiales" in normalized_surface
    ):
        return "ARTÍCULO 16 — DAÑOS MATERIALES\n" + normalized_block
    if (
        "no tendran que elaborar el informe policial" in normalized_surface
        or "material probatorio recaudado" in normalized_surface
    ):
        return "INFORME POLICIAL Y RECAUDO PROBATORIO\n" + normalized_block
    if (
        "retirar inmediatamente los vehiculos" in normalized_surface
        or "centros de conciliacion" in normalized_surface
        or "1. en los accidentes de transito" in normalized_surface
    ):
        return "INSTRUCCIONES OPERATIVAS CHOQUE SIMPLE\n" + normalized_block
    return normalized_block


def normalize_pv_heading_text(value: str) -> str:
    """Canonicalize common PV headings with unstable casing or number."""

    normalized_value = normalize_equivalence_text(value)
    if normalized_value in {"planes que aplica", "planes que aplican", "plan que aplica"}:
        return "PLANES QUE APLICA"
    return value.strip()


def is_pv_slogan_line(value: str) -> bool:
    """Return whether a line is a commercial PV slogan without retrieval value."""

    normalized_value = normalize_equivalence_text(value.lstrip("#").strip())
    if not normalized_value:
        return False
    parts = [part.strip() for part in normalized_value.split("/") if part.strip()]
    if not parts:
        return False
    return all(part in PV_SLOGAN_NORMALIZED_LINES for part in parts)


def strip_inline_pv_slogan_suffix(value: str) -> str:
    """Remove trailing PV slogan fragments when appended to a meaningful line."""

    stripped_value = value.strip()
    patterns = (
        r"\s+SENTIRTE\s+ACOMPAÑADO\s*/\s*AHORRAR\s+TIEMPO\s*/\s*AHORRAR\s+DINERO\s*$",
        r"\s+SENTIRTE\s+ACOMPAÑADO\s*/\s*AHORRAR\s+TIEMPO\s*$",
        r"\s+SENTIRTE\s+ACOMPAÑADO\s*/\s*AHORRAR\s+DINERO\s*$",
        r"\s+AHORRAR\s+TIEMPO\s*/\s*AHORRAR\s+DINERO\s*$",
        r"\s+SENTIRTE\s+ACOMPAÑADO\s*$",
        r"\s+AHORRAR\s+TIEMPO\s*$",
        r"\s+AHORRAR\s+DINERO\s*$",
    )
    for pattern in patterns:
        substituted_value = re.sub(pattern, "", stripped_value, flags=re.IGNORECASE)
        if substituted_value != stripped_value:
            updated_value = substituted_value.strip(" -:/")
            if updated_value:
                return updated_value
    return stripped_value


def normalize_pv_commercial_block(block_text: str) -> str:
    """Rewrite noisy PV slide blocks into compact retrieval-oriented text."""

    raw_lines = [line.strip() for line in block_text.splitlines() if line.strip()]
    if not raw_lines:
        return block_text

    normalized_lines: list[str] = []
    bullet_lines: list[str] = []
    removed_pv_noise = False
    modified_pv_surface = False

    for line in raw_lines:
        original_line = line
        line = strip_inline_pv_slogan_suffix(line)
        if line != original_line:
            modified_pv_surface = True
        if is_pv_slogan_line(line):
            removed_pv_noise = True
            continue
        canonical_heading = normalize_pv_heading_text(line)
        if canonical_heading != line.strip():
            modified_pv_surface = True
            normalized_lines.append(canonical_heading)
            continue

        normalized_line = re.sub(r"^-\s*o\s*$", "", line, flags=re.IGNORECASE).strip()
        normalized_line = re.sub(r"^-\s*o\s+", "- ", normalized_line, flags=re.IGNORECASE)
        normalized_line = re.sub(r"^o\s+", "- ", normalized_line, flags=re.IGNORECASE)
        normalized_line = re.sub(r"\s+", " ", normalized_line).strip()
        if not normalized_line or normalized_line in {"-", "o"}:
            removed_pv_noise = True
            continue
        if normalized_line in {".", "·", "•"}:
            removed_pv_noise = True
            continue
        if normalized_line.startswith("- "):
            if normalized_line not in bullet_lines:
                bullet_lines.append(normalized_line)
            continue
        normalized_lines.append(normalized_line)

    if bullet_lines:
        normalized_lines.extend(bullet_lines)

    if not normalized_lines:
        return ""

    if removed_pv_noise or modified_pv_surface:
        return "\n".join(normalized_lines)

    if not any(
        normalize_equivalence_text(line) == "propuesta de valor movilidad"
        or normalize_equivalence_text(normalize_pv_heading_text(line)) == "planes que aplica"
        or line.startswith("- ")
        for line in normalized_lines
    ):
        return block_text

    return "\n".join(normalized_lines)


def normalize_heading_prefixed_pv_block(block_text: str) -> str:
    """Apply PV commercial cleanup to the body of heading-prefixed blocks."""

    lines = block_text.splitlines()
    if len(lines) <= 1:
        return block_text
    heading_line = lines[0].rstrip()
    body = "\n".join(lines[1:]).strip()
    if not body:
        return heading_line
    normalized_body = normalize_pv_commercial_block(body)
    if not normalized_body:
        return heading_line
    return f"{heading_line}\n\n{normalized_body}"


def split_markdown_blocks(cleaned_markdown_text: str) -> list[MarkdownBlock]:
    """Split cleaned markdown into deterministic text blocks with structural context."""

    heading_stack: list[str] = []
    blocks: list[MarkdownBlock] = []
    replaceable_semantic_headings = {"circular externa", "bogota d.c."}

    for raw_block in cleaned_markdown_text.strip().split("\n\n"):
        block = raw_block.strip()
        if not block:
            continue
        first_line = block.splitlines()[0].strip()
        if first_line.startswith("#"):
            level = len(first_line) - len(first_line.lstrip("#"))
            heading_text = normalize_pv_heading_text(first_line.lstrip("#").strip())
            if is_pv_slogan_line(heading_text):
                continue
            if heading_text:
                while len(heading_stack) >= level:
                    heading_stack.pop()
                heading_stack.append(heading_text)
            if (
                heading_text
                and len(block.splitlines()) == 1
                and normalize_equivalence_text(heading_text) in replaceable_semantic_headings
            ):
                continue
            if is_page_heading_text(heading_text):
                continue
            if len(block.splitlines()) > 1:
                block = normalize_heading_prefixed_pv_block(block)
        else:
            block = normalize_comparison_table_block(block)
            block = normalize_diagrammatic_coverage_block(block)
            block = normalize_expedition_requirements_block(block)
            block = normalize_deductible_block(block)
            block = normalize_choque_simple_circular_block(block)
            block = normalize_pv_commercial_block(block)
            if not block:
                continue
        semantic_section = find_semantic_section_label(block)
        if semantic_section and normalize_equivalence_text(block) == normalize_equivalence_text(
            semantic_section
        ):
            if (
                heading_stack
                and (
                    is_page_heading_text(heading_stack[-1])
                    or normalize_equivalence_text(heading_stack[-1])
                    in replaceable_semantic_headings
                )
            ):
                heading_stack[-1] = semantic_section
            elif not heading_stack or heading_stack[-1] != semantic_section:
                heading_stack.append(semantic_section)
            continue
        if normalize_equivalence_text(block) == "gracias":
            continue
        effective_section_path = tuple(heading_stack)
        if (
            semantic_section
            and effective_section_path
            and (
                is_page_heading_text(effective_section_path[-1])
                or normalize_equivalence_text(effective_section_path[-1])
                in replaceable_semantic_headings
            )
        ):
            effective_section_path = (*effective_section_path[:-1], semantic_section)
        section = effective_section_path[-1] if effective_section_path else None
        blocks.append(
            MarkdownBlock(
                text=block,
                section=section,
                section_path=effective_section_path,
                kind=detect_block_kind(block),
            )
        )

    return blocks


def expand_large_blocks(
    blocks: list[MarkdownBlock],
    chunk_size: int,
) -> list[MarkdownBlock]:
    """Split oversized blocks deterministically to respect chunk size."""

    expanded_blocks: list[MarkdownBlock] = []

    for block in blocks:
        if len(block.text) <= chunk_size:
            expanded_blocks.append(block)
            continue

        start = 0
        while start < len(block.text):
            expanded_blocks.append(
                MarkdownBlock(
                    text=block.text[start : start + chunk_size],
                    section=block.section,
                    section_path=block.section_path,
                    kind=block.kind,
                )
            )
            start += chunk_size

    return expanded_blocks


def can_merge_structural_pair(
    current_block: MarkdownBlock,
    next_block: MarkdownBlock,
    chunk_size: int,
) -> bool:
    """Return whether two neighboring blocks should be kept together."""

    combined_length = len(current_block.text) + 2 + len(next_block.text)
    if combined_length > chunk_size:
        return False
    if current_block.kind == "heading":
        if (
            current_block.section_path != next_block.section_path
            and (
                is_arl_rui_question_section_path(current_block.section_path)
                or is_arl_rui_question_section_path(next_block.section_path)
            )
        ):
            return False
        return True
    if current_block.kind == "clause_marker":
        return True
    return (
        len(current_block.text) <= MAX_STRUCTURAL_BLOCK_LENGTH
        and next_block.section_path == current_block.section_path
    )


def is_root_pv_block(block: MarkdownBlock) -> bool:
    """Return whether a block belongs to the PV movilidad corpus root."""

    return bool(block.section_path) and normalize_equivalence_text(
        block.section_path[0]
    ) == "propuesta de valor movilidad"


def is_pv_applicability_block(block: MarkdownBlock) -> bool:
    """Return whether a block is the applicability list for one PV benefit."""

    return normalize_equivalence_text(block.section or "") == "planes que aplica"


def can_merge_pv_benefit_with_applicability(
    current_block: MarkdownBlock,
    next_block: MarkdownBlock,
    chunk_size: int,
) -> bool:
    """Keep one PV benefit together with its immediately following applicability list."""

    if current_block.kind == "heading" or next_block.kind == "heading":
        return False
    if not is_root_pv_block(current_block) or not is_root_pv_block(next_block):
        return False
    if is_pv_applicability_block(current_block) or not is_pv_applicability_block(next_block):
        return False
    if len(current_block.section_path) != 2 or len(next_block.section_path) != 2:
        return False
    combined_length = len(current_block.text) + 2 + len(next_block.text)
    return combined_length <= chunk_size


def can_merge_pv_benefit_with_applicability_heading_triplet(
    current_block: MarkdownBlock,
    next_heading_block: MarkdownBlock,
    next_block: MarkdownBlock,
    chunk_size: int,
) -> bool:
    """Keep one PV benefit with an immediately following applicability heading+list."""

    if current_block.kind == "heading":
        return False
    if next_heading_block.kind != "heading":
        return False
    if not is_root_pv_block(current_block) or not is_root_pv_block(next_heading_block):
        return False
    if not is_root_pv_block(next_block) or not is_pv_applicability_block(next_block):
        return False
    if normalize_equivalence_text(next_heading_block.section or "") != "planes que aplica":
        return False
    combined_length = (
        len(current_block.text) + 2 + len(next_heading_block.text) + 2 + len(next_block.text)
    )
    return combined_length <= chunk_size


def group_semantic_blocks(blocks: list[MarkdownBlock], chunk_size: int) -> list[MarkdownBlock]:
    """Group related structural blocks before chunk assembly."""

    grouped_blocks: list[MarkdownBlock] = []
    index = 0

    while index < len(blocks):
        current_block = blocks[index]
        if index + 2 < len(blocks):
            next_heading_block = blocks[index + 1]
            next_block = blocks[index + 2]
            if can_merge_pv_benefit_with_applicability_heading_triplet(
                current_block,
                next_heading_block,
                next_block,
                chunk_size,
            ):
                grouped_blocks.append(
                    MarkdownBlock(
                        text=(
                            f"{current_block.text}\n\n"
                            f"{next_heading_block.text}\n\n"
                            f"{next_block.text}"
                        ),
                        section=current_block.section,
                        section_path=current_block.section_path,
                        kind="grouped",
                    )
                )
                index += 3
                continue
        if index + 1 < len(blocks):
            next_block = blocks[index + 1]
            if can_merge_pv_benefit_with_applicability(current_block, next_block, chunk_size):
                grouped_blocks.append(
                    MarkdownBlock(
                        text=f"{current_block.text}\n\n{next_block.text}",
                        section=current_block.section,
                        section_path=current_block.section_path,
                        kind="grouped",
                    )
                )
                index += 2
                continue
        if current_block.kind in {"heading", "clause_marker"} and index + 1 < len(blocks):
            next_block = blocks[index + 1]
            if can_merge_structural_pair(current_block, next_block, chunk_size):
                grouped_blocks.append(
                    MarkdownBlock(
                        text=f"{current_block.text}\n\n{next_block.text}",
                        section=next_block.section or current_block.section,
                        section_path=next_block.section_path or current_block.section_path,
                        kind="grouped",
                    )
                )
                index += 2
                continue

        if current_block.kind != "heading":
            combined_text = current_block.text
            combined_section = current_block.section
            combined_section_path = current_block.section_path
            next_index = index + 1

            while next_index < len(blocks):
                next_block = blocks[next_index]
                if next_block.kind == "heading":
                    break
                if next_block.section_path != combined_section_path:
                    break
                if len(combined_text) + 2 + len(next_block.text) > chunk_size:
                    break
                combined_text = f"{combined_text}\n\n{next_block.text}"
                combined_section = next_block.section or combined_section
                combined_section_path = next_block.section_path or combined_section_path
                next_index += 1

            if next_index > index + 1:
                grouped_blocks.append(
                    MarkdownBlock(
                        text=combined_text,
                        section=combined_section,
                        section_path=combined_section_path,
                        kind="grouped",
                    )
                )
                index = next_index
                continue
        grouped_blocks.append(current_block)
        index += 1

    return grouped_blocks


def render_section_path_heading_prefix(section_path: Sequence[str]) -> str:
    """Render one markdown heading prefix from a chunk section path."""

    heading_lines: list[str] = []
    for index, heading in enumerate(section_path, start=1):
        normalized_heading = heading.strip()
        if not normalized_heading:
            continue
        heading_lines.append(f"{'#' * min(index, 6)} {normalized_heading}")
    return "\n\n".join(heading_lines)


def strip_duplicate_prefixed_headings(
    *,
    chunk_text: str,
    section_path: Sequence[str],
) -> str:
    """Remove duplicated leading headings already represented in section-path prefix."""

    remaining_text = chunk_text
    section_headings = [heading.strip() for heading in section_path if heading.strip()]
    if not section_headings:
        return chunk_text

    for index, heading in enumerate(section_headings):
        level = min(index + 1, 6)
        heading_line = f"{'#' * level} {heading}"
        lines = remaining_text.splitlines()
        if not lines:
            break
        if normalize_equivalence_text(lines[0]) != normalize_equivalence_text(heading_line):
            break
        remaining_text = "\n".join(lines[1:]).lstrip("\n")

    return remaining_text or chunk_text


def strip_leading_heading_scaffold_covered_by_section_path(
    *,
    chunk_text: str,
    section_path: Sequence[str],
) -> str:
    """Drop leading heading scaffolds already represented by section_path."""

    section_headings = {
        normalize_equivalence_text(heading.strip()) for heading in section_path if heading.strip()
    }
    if not section_headings:
        return chunk_text

    lines = chunk_text.splitlines()
    leading_heading_indexes: list[int] = []
    matched_section_heading = False
    index = 0

    while index < len(lines):
        stripped_line = lines[index].strip()
        if not stripped_line:
            index += 1
            continue
        if not stripped_line.startswith("#"):
            break
        normalized_heading = normalize_equivalence_text(stripped_line.lstrip("#").strip())
        if normalized_heading in section_headings:
            matched_section_heading = True
        leading_heading_indexes.append(index)
        index += 1

    if not matched_section_heading or not leading_heading_indexes:
        return chunk_text

    remainder = "\n".join(lines[index:]).lstrip("\n")
    return remainder or chunk_text


def collapse_consecutive_duplicate_heading_lines(chunk_text: str) -> str:
    """Collapse repeated consecutive markdown headings conservatively."""

    collapsed_lines: list[str] = []
    previous_heading: str | None = None

    for raw_line in chunk_text.splitlines():
        stripped_line = raw_line.strip()
        if stripped_line.startswith("#"):
            heading_body = stripped_line.lstrip("#").strip()
            normalized_heading = normalize_equivalence_text(
                normalize_pv_heading_text(heading_body)
            )
            if normalized_heading == previous_heading:
                continue
            previous_heading = normalized_heading
            collapsed_lines.append(raw_line)
            continue
        if stripped_line:
            previous_heading = None
        collapsed_lines.append(raw_line)

    return "\n".join(collapsed_lines)


def drop_repeated_section_path_heading_lines(
    *,
    chunk_text: str,
    section_path: Sequence[str],
) -> str:
    """Drop repeated heading lines that duplicate already-prefixed section headings."""

    normalized_section_headings = {
        normalize_equivalence_text(heading.strip()) for heading in section_path if heading.strip()
    }
    if not normalized_section_headings:
        return chunk_text

    deduplicated_lines: list[str] = []
    seen_section_headings: set[str] = set()

    for raw_line in chunk_text.splitlines():
        stripped_line = raw_line.strip()
        if stripped_line.startswith("#"):
            normalized_heading = normalize_equivalence_text(stripped_line.lstrip("#").strip())
            if (
                normalized_heading in normalized_section_headings
                and normalized_heading in seen_section_headings
            ):
                continue
            if normalized_heading in normalized_section_headings:
                seen_section_headings.add(normalized_heading)
        deduplicated_lines.append(raw_line)

    return "\n".join(deduplicated_lines)


def markdown_has_non_heading_content(chunk_text: str) -> bool:
    """Return whether one chunk surface contains substantive non-heading text."""

    for raw_line in chunk_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue
        if stripped_line.startswith("#"):
            continue
        return True
    return False


def ensure_chunk_text_includes_section_context(
    *,
    chunk_text: str,
    section_path: Sequence[str],
) -> str:
    """Prefix governing section-path headings when the chunk text is missing them."""

    heading_prefix = render_section_path_heading_prefix(section_path)
    if not heading_prefix:
        return chunk_text

    chunk_text = strip_duplicate_prefixed_headings(
        chunk_text=chunk_text,
        section_path=section_path,
    )
    chunk_text = strip_leading_heading_scaffold_covered_by_section_path(
        chunk_text=chunk_text,
        section_path=section_path,
    )
    chunk_text = collapse_consecutive_duplicate_heading_lines(chunk_text)

    normalized_chunk_text = normalize_equivalence_text(chunk_text)
    normalized_prefix = normalize_equivalence_text(heading_prefix)
    if normalized_prefix and normalized_prefix in normalized_chunk_text:
        return drop_repeated_section_path_heading_lines(
            chunk_text=chunk_text,
            section_path=section_path,
        )
    return drop_repeated_section_path_heading_lines(
        chunk_text=collapse_consecutive_duplicate_heading_lines(
            f"{heading_prefix}\n\n{chunk_text}"
        ),
        section_path=section_path,
    )


def is_pv_applicability_section_path(section_path: Sequence[str]) -> bool:
    """Return whether a section path points to the PV applicability lane."""

    return (
        len(section_path) >= 2
        and normalize_equivalence_text(section_path[0]) == "propuesta de valor movilidad"
        and normalize_equivalence_text(section_path[-1]) == "planes que aplica"
    )


def is_arl_rui_question_section_path(section_path: Sequence[str]) -> bool:
    """Return whether one section path points to an explicit ARL/RUI FAQ question."""

    return (
        len(section_path) >= 2
        and normalize_equivalence_text(section_path[0])
        == "preguntas frecuentes registro unico de intermediacion - rui"
        and ARL_RUI_FAQ_QUESTION_PATTERN.match(section_path[-1]) is not None
    )


def should_disable_chunk_overlap_for_entries(entries: Sequence[MarkdownBlock]) -> bool:
    """Disable overlap for narrow applicability-heavy PV chunks."""

    if not entries:
        return False
    return all(
        is_pv_applicability_section_path(entry.section_path)
        or is_arl_rui_question_section_path(entry.section_path)
        for entry in entries
    )
