"""CLI command adapters and request lifecycle helpers for the RAG entrypoint."""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from contracts import RetrievalQuery


def call_with_optional_request_id(function, *args, request_id: str | None = None, **kwargs):
    """Call a seam with request_id when supported, otherwise retry without it."""

    if request_id is None:
        return function(*args, **kwargs)
    try:
        return function(*args, request_id=request_id, **kwargs)
    except TypeError as exc:
        if "request_id" not in str(exc):
            raise
        return function(*args, **kwargs)


def build_retrieval_query_from_args(
    args: argparse.Namespace,
    *,
    default_top_k: int,
) -> RetrievalQuery:
    """Build the shared retrieval contract from CLI args."""

    return RetrievalQuery(
        query=args.query,
        top_k=args.top_k if args.top_k is not None else default_top_k,
        filters={
            "document_type": args.document_type,
            "product": args.product,
            "document_name": args.document_name,
            "version": args.version,
        },
    )


def run_docling_warmup_command(
    args: argparse.Namespace,
    *,
    ensure_pdf_conversion_backend_available_fn: Callable[..., None],
    convert_pdf_to_markdown_with_docling_fn: Callable[..., str],
    output_fn: Callable[[str], None] = print,
    error_output_fn: Callable[[str], None] | None = None,
) -> int:
    """Warm up Docling assets through a thin CLI adapter."""

    if error_output_fn is None:
        def error_output_fn(message: str) -> None:
            print(message, file=sys.stderr)

    sample_pdf = Path(args.sample_pdf)
    if not sample_pdf.exists() or not sample_pdf.is_file():
        error_output_fn(f"Sample PDF does not exist: {sample_pdf}")
        return 2

    ensure_pdf_conversion_backend_available_fn(backend="docling")
    markdown = convert_pdf_to_markdown_with_docling_fn(
        sample_pdf,
        startup_timeout_seconds=args.docling_startup_timeout_seconds,
    )
    if not markdown.strip():
        error_output_fn("Docling warm-up did not produce markdown output.")
        return 1
    output_fn(
        f"Docling warm-up succeeded for {sample_pdf.name}. "
        "Required assets should now be cached locally."
    )
    return 0


def run_embedding_warmup_command(
    *,
    get_settings_fn: Callable[[], Any],
    validate_embedding_settings_fn: Callable[[Any], Any],
    ensure_embedding_backend_available_fn: Callable[[Any], None],
    load_sentence_transformer_fn: Callable[..., Any],
    output_fn: Callable[[str], None] = print,
) -> int:
    """Warm up embedding-model assets through a thin CLI adapter."""

    settings = validate_embedding_settings_fn(get_settings_fn())
    ensure_embedding_backend_available_fn(settings)
    load_sentence_transformer_fn(settings.embedding_model, local_files_only=False)
    output_fn(
        f"Embedding warm-up succeeded for {settings.embedding_model}. "
        "Required assets should now be cached locally."
    )
    return 0


def run_retrieval_command(
    args: argparse.Namespace,
    *,
    request_id: str | None,
    default_top_k: int,
    retrieve_ranked_chunks_fn: Callable[..., Any],
    output_fn: Callable[[str], None] = print,
) -> int:
    """Run retrieval from the shared CLI adapter surface."""

    retrieval_query = build_retrieval_query_from_args(args, default_top_k=default_top_k)
    result = retrieve_ranked_chunks_fn(retrieval_query, request_id=request_id)
    output_fn(result.model_dump_json(indent=2))
    return 0


def run_grounded_answer_command(
    args: argparse.Namespace,
    *,
    request_id: str | None,
    default_top_k: int,
    generate_grounded_answer_fn: Callable[..., Any],
    output_fn: Callable[[str], None] = print,
) -> int:
    """Run grounded answering from the shared CLI adapter surface."""

    retrieval_query = build_retrieval_query_from_args(args, default_top_k=default_top_k)
    result = generate_grounded_answer_fn(retrieval_query, request_id=request_id)
    output_fn(result.model_dump_json(indent=2))
    return 0


def dispatch_cli_command(
    args: argparse.Namespace,
    *,
    parser: argparse.ArgumentParser,
    request_id: str,
    run_ingestion_fn: Callable[[argparse.Namespace], int],
    run_docling_warmup_fn: Callable[[argparse.Namespace], int],
    run_embedding_warmup_fn: Callable[[], int],
    run_embedding_generation_fn: Callable[[argparse.Namespace], int],
    run_qdrant_indexing_fn: Callable[[argparse.Namespace], int],
    run_retrieval_fn: Callable[..., int],
    run_grounded_answer_generation_fn: Callable[..., int],
) -> int:
    """Dispatch one parsed CLI command through injected adapters."""

    if args.command == "ingest-pdfs":
        return run_ingestion_fn(args)
    if args.command == "warmup-docling-assets":
        return run_docling_warmup_fn(args)
    if args.command == "warmup-embedding-assets":
        return run_embedding_warmup_fn()
    if args.command == "generate-embeddings":
        return run_embedding_generation_fn(args)
    if args.command == "index-embeddings":
        return run_qdrant_indexing_fn(args)
    if args.command == "retrieve-chunks":
        return run_retrieval_fn(args, request_id=request_id)
    if args.command == "answer-query":
        return run_grounded_answer_generation_fn(args, request_id=request_id)
    parser.error(f"Unsupported command: {args.command}")


def run_cli_request(
    argv: Sequence[str] | None = None,
    *,
    build_parser_fn: Callable[[], argparse.ArgumentParser],
    get_settings_fn: Callable[[], Any],
    configure_logging_fn: Callable[[str], None],
    log_startup_diagnostics_fn: Callable[..., None],
    logger: logging.Logger,
    generate_request_id_fn: Callable[[str], str],
    log_event_fn: Callable[..., None],
    run_ingestion_fn: Callable[[argparse.Namespace], int],
    run_docling_warmup_fn: Callable[[argparse.Namespace], int],
    run_embedding_warmup_fn: Callable[[], int],
    run_embedding_generation_fn: Callable[[argparse.Namespace], int],
    run_qdrant_indexing_fn: Callable[[argparse.Namespace], int],
    run_retrieval_fn: Callable[..., int],
    run_grounded_answer_generation_fn: Callable[..., int],
    runtime_surface: str = "cli",
) -> int:
    """Execute one full CLI request lifecycle with injected command runners."""

    settings = get_settings_fn()
    configure_logging_fn(settings.log_level)
    log_startup_diagnostics_fn(logger, settings, runtime_surface=runtime_surface)

    parser = build_parser_fn()
    args = parser.parse_args(argv)
    request_id = generate_request_id_fn(runtime_surface)
    log_event_fn(
        logger,
        event_type="request_started",
        request_id=request_id,
        runtime_surface=runtime_surface,
        command=args.command,
    )

    try:
        exit_code = dispatch_cli_command(
            args,
            parser=parser,
            request_id=request_id,
            run_ingestion_fn=run_ingestion_fn,
            run_docling_warmup_fn=run_docling_warmup_fn,
            run_embedding_warmup_fn=run_embedding_warmup_fn,
            run_embedding_generation_fn=run_embedding_generation_fn,
            run_qdrant_indexing_fn=run_qdrant_indexing_fn,
            run_retrieval_fn=run_retrieval_fn,
            run_grounded_answer_generation_fn=run_grounded_answer_generation_fn,
        )
        if exit_code == 0:
            log_event_fn(
                logger,
                event_type="request_succeeded",
                request_id=request_id,
                runtime_surface=runtime_surface,
                command=args.command,
                exit_code=exit_code,
            )
        else:
            log_event_fn(
                logger,
                event_type="request_failed",
                request_id=request_id,
                level=logging.ERROR,
                runtime_surface=runtime_surface,
                command=args.command,
                error_type="CommandExit",
                error_message=f"Command exited with status {exit_code}.",
                exit_code=exit_code,
            )
        return exit_code
    except Exception as exc:
        log_event_fn(
            logger,
            event_type="request_failed",
            request_id=request_id,
            level=logging.ERROR,
            runtime_surface=runtime_surface,
            command=args.command,
            error_type=type(exc).__name__,
            error_message=str(exc),
        )
        print(str(exc), file=sys.stderr)
        return 1
