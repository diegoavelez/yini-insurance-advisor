from __future__ import annotations

import contextlib
import importlib.util
import os
import subprocess
import sys
from collections.abc import Callable, Iterator
from pathlib import Path

from rag.term_equivalences import tokenize_lexical_surface

EMPTY_BOILERPLATE_LINES = {"[]", "[ ]", "[]()", "![]()", "<!-- image -->"}


def docling_is_available() -> bool:
    """Return whether Docling is importable in the current runtime."""

    return importlib.util.find_spec("docling") is not None


def ensure_docling_available() -> None:
    """Fail loudly when Docling is not available locally."""

    if not docling_is_available():
        raise RuntimeError(
            "Docling is not installed. Install project dependencies before running "
            "the ingestion CLI."
        )


def pdfium_backend_is_available() -> bool:
    """Return whether the PDFium fallback backend is importable."""

    return importlib.util.find_spec("pypdfium2") is not None


def ensure_pdf_conversion_backend_available(
    *,
    backend: str,
    docling_is_available_fn: Callable[[], bool] = docling_is_available,
    pdfium_backend_is_available_fn: Callable[[], bool] = pdfium_backend_is_available,
) -> None:
    """Fail loudly when no supported local PDF conversion backend is available."""

    if backend == "docling":
        if docling_is_available_fn():
            return
        raise RuntimeError(
            "Docling is not installed. Install project dependencies before running "
            "the ingestion CLI with the Docling backend."
        )
    if backend == "pdfium":
        if pdfium_backend_is_available_fn():
            return
        raise RuntimeError(
            "pypdfium2 is not installed. Install project dependencies before running "
            "the ingestion CLI with the PDFium backend."
        )
    if docling_is_available_fn() or pdfium_backend_is_available_fn():
        return
    raise RuntimeError(
        "No supported PDF conversion backend is installed. Install Docling or "
        "pypdfium2 before running the ingestion CLI."
    )


@contextlib.contextmanager
def offline_huggingface_resolution(*, enabled: bool) -> Iterator[None]:
    """Force offline Hugging Face resolution when loading cached local assets."""

    if not enabled:
        yield
        return

    override_values = {
        "HF_HUB_OFFLINE": "1",
        "TRANSFORMERS_OFFLINE": "1",
    }
    previous_values = {key: os.environ.get(key) for key in override_values}
    try:
        for key, value in override_values.items():
            os.environ[key] = value
        yield
    finally:
        for key, previous_value in previous_values.items():
            if previous_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous_value


def convert_pdf_to_markdown_with_docling(
    source_pdf_path: Path,
    *,
    startup_timeout_seconds: float,
    force_full_page_ocr: bool = False,
) -> str:
    """Convert one PDF to markdown through Docling in an isolated subprocess."""

    script = """
from pathlib import Path
import sys
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import OcrAutoOptions, PdfPipelineOptions

source_pdf_path = Path(sys.argv[1])
force_full_page_ocr = sys.argv[2].lower() == "true"

if force_full_page_ocr:
    pipeline_options = PdfPipelineOptions(
        do_ocr=True,
        ocr_options=OcrAutoOptions(force_full_page_ocr=True),
    )
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )
else:
    converter = DocumentConverter()
result = converter.convert(str(source_pdf_path))
document = getattr(result, "document", None)
if document is not None and hasattr(document, "export_to_markdown"):
    markdown = document.export_to_markdown()
else:
    markdown = getattr(result, "markdown", None)
if not isinstance(markdown, str) or not markdown.strip():
    raise RuntimeError("Docling conversion result did not expose markdown output.")
sys.stdout.write(markdown)
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(source_pdf_path),
            str(force_full_page_ocr).lower(),
        ],
        capture_output=True,
        text=True,
        timeout=startup_timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip()
            or "Docling conversion failed without a detailed error message."
        )
    markdown = completed.stdout
    if not markdown.strip():
        raise RuntimeError("Docling conversion produced empty markdown output.")
    return markdown


def convert_pdf_to_markdown_with_pdfium(source_pdf_path: Path) -> str:
    """Convert one PDF into simple markdown through the PDFium text fallback."""

    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(source_pdf_path))
    markdown_sections = [f"# {source_pdf_path.stem}"]

    for page_index in range(len(pdf)):
        page = pdf[page_index]
        text_page = page.get_textpage()
        page_text = text_page.get_text_range().strip()
        if not page_text:
            continue
        markdown_sections.extend(
            [
                "",
                f"## Page {page_index + 1}",
                "",
                page_text,
            ]
        )

    markdown = "\n".join(markdown_sections).strip()
    if not markdown:
        raise RuntimeError("PDFium fallback conversion produced empty markdown output.")
    return f"{markdown}\n"


def markdown_has_usable_text_surface(markdown_text: str) -> bool:
    """Return whether markdown exposes enough non-placeholder text to keep."""

    image_placeholder_count = 0
    lexical_lines: list[str] = []

    for raw_line in markdown_text.splitlines():
        stripped_line = raw_line.strip()
        if not stripped_line:
            continue
        if stripped_line == "<!-- image -->":
            image_placeholder_count += 1
            continue
        if stripped_line in EMPTY_BOILERPLATE_LINES:
            continue
        lexical_lines.append(stripped_line)

    if not lexical_lines:
        return False

    lexical_surface = "\n".join(lexical_lines)
    lexical_tokens = tokenize_lexical_surface(lexical_surface)
    alphabetic_characters = sum(character.isalpha() for character in lexical_surface)

    if image_placeholder_count >= 2 and len(lexical_tokens) <= 3:
        return False
    if image_placeholder_count >= 2 and alphabetic_characters < 40:
        return False
    return True


def is_docling_insufficient_text_error(error: Exception) -> bool:
    """Return whether one conversion error means Docling produced too little text."""

    return isinstance(error, RuntimeError) and str(error) in {
        "Docling conversion produced insufficient non-placeholder text.",
        "Docling OCR conversion produced insufficient non-placeholder text.",
    }


def convert_pdf_to_markdown_with_backend(
    source_pdf_path: Path,
    *,
    backend: str,
    docling_startup_timeout_seconds: float,
    docling_is_available_fn: Callable[[], bool] = docling_is_available,
    pdfium_backend_is_available_fn: Callable[[], bool] = pdfium_backend_is_available,
    convert_pdf_to_markdown_with_docling_fn: Callable[..., str] = (
        convert_pdf_to_markdown_with_docling
    ),
    convert_pdf_to_markdown_with_pdfium_fn: Callable[[Path], str] = (
        convert_pdf_to_markdown_with_pdfium
    ),
    markdown_has_usable_text_surface_fn: Callable[[str], bool] = (
        markdown_has_usable_text_surface
    ),
    is_docling_insufficient_text_error_fn: Callable[[Exception], bool] = (
        is_docling_insufficient_text_error
    ),
    ensure_pdf_conversion_backend_available_fn: Callable[..., None] = (
        ensure_pdf_conversion_backend_available
    ),
) -> str:
    """Convert one PDF to markdown using the selected backend policy."""

    fallback_error: Exception | None = None
    if backend in {"docling", "auto"} and docling_is_available_fn():
        try:
            markdown = convert_pdf_to_markdown_with_docling_fn(
                source_pdf_path,
                startup_timeout_seconds=docling_startup_timeout_seconds,
            )
            if markdown_has_usable_text_surface_fn(markdown):
                return markdown
            fallback_error = RuntimeError(
                "Docling conversion produced insufficient non-placeholder text."
            )
            ocr_markdown = convert_pdf_to_markdown_with_docling_fn(
                source_pdf_path,
                startup_timeout_seconds=docling_startup_timeout_seconds,
                force_full_page_ocr=True,
            )
            if markdown_has_usable_text_surface_fn(ocr_markdown):
                return ocr_markdown
            fallback_error = RuntimeError(
                "Docling OCR conversion produced insufficient non-placeholder text."
            )
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            fallback_error = exc

    if backend == "docling" and fallback_error is not None:
        if (
            isinstance(fallback_error, subprocess.TimeoutExpired)
            or is_docling_insufficient_text_error_fn(fallback_error)
        ) and pdfium_backend_is_available_fn():
            return convert_pdf_to_markdown_with_pdfium_fn(source_pdf_path)
        raise RuntimeError(
            "Docling conversion did not produce a usable markdown surface."
        ) from fallback_error

    if backend in {"pdfium", "auto"} and pdfium_backend_is_available_fn():
        return convert_pdf_to_markdown_with_pdfium_fn(source_pdf_path)

    if fallback_error is not None:
        raise RuntimeError(
            "Docling conversion did not complete and no PDFium fallback backend is available."
        ) from fallback_error
    ensure_pdf_conversion_backend_available_fn(
        backend=backend,
        docling_is_available_fn=docling_is_available_fn,
        pdfium_backend_is_available_fn=pdfium_backend_is_available_fn,
    )
    raise RuntimeError("No PDF conversion backend produced markdown output.")


def clean_markdown(markdown_text: str) -> str:
    """Apply conservative, deterministic cleaning to Docling markdown."""

    normalized_text = markdown_text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_lines: list[str] = []
    previous_line_blank = False

    for raw_line in normalized_text.split("\n"):
        line = raw_line.rstrip()
        stripped_line = line.strip()

        if stripped_line in EMPTY_BOILERPLATE_LINES:
            continue

        if not stripped_line:
            if previous_line_blank:
                continue
            cleaned_lines.append("")
            previous_line_blank = True
            continue

        cleaned_lines.append(line)
        previous_line_blank = False

    cleaned_text = "\n".join(cleaned_lines).strip()
    if not cleaned_text:
        raise RuntimeError("Cleaned markdown is empty after conservative processing.")
    return f"{cleaned_text}\n"
