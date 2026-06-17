from __future__ import annotations

import logging
from types import SimpleNamespace

import pytest

from rag import cli_runtime
from rag.ingestion import build_parser


def make_settings() -> SimpleNamespace:
    return SimpleNamespace(log_level="INFO", top_k=5)


def test_build_retrieval_query_from_args_uses_default_top_k_and_filters() -> None:
    args = build_parser().parse_args(
        [
            "retrieve-chunks",
            "--query",
            "coverage",
            "--product",
            "auto",
            "--document-type",
            "guide",
            "--document-name",
            "policy-a",
            "--version",
            "2026-01",
        ]
    )

    retrieval_query = cli_runtime.build_retrieval_query_from_args(args, default_top_k=7)

    assert retrieval_query.query == "coverage"
    assert retrieval_query.top_k == 7
    assert retrieval_query.filters.product == "auto"
    assert retrieval_query.filters.document_type == "guide"
    assert retrieval_query.filters.document_name == "policy-a"
    assert retrieval_query.filters.version == "2026-01"


def test_call_with_optional_request_id_retries_without_request_id_support() -> None:
    calls: list[tuple[str, str | None]] = []

    def function_without_request_id(argument: str) -> str:
        calls.append((argument, None))
        return f"ok:{argument}"

    result = cli_runtime.call_with_optional_request_id(
        function_without_request_id,
        "value",
        request_id="req-123",
    )

    assert result == "ok:value"
    assert calls == [("value", None)]


def test_run_cli_request_emits_started_and_succeeded_events(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)
    captured_request_ids: list[str | None] = []

    def run_retrieval(args, request_id=None):
        captured_request_ids.append(request_id)
        assert args.command == "retrieve-chunks"
        return 0

    exit_code = cli_runtime.run_cli_request(
        ["retrieve-chunks", "--query", "What is covered?"],
        build_parser_fn=build_parser,
        get_settings_fn=make_settings,
        configure_logging_fn=lambda _level: None,
        log_startup_diagnostics_fn=lambda logger, settings, runtime_surface: logger.info(
            "startup",
            extra={"event_type": "startup_diagnostics", "runtime_surface": runtime_surface},
        ),
        logger=logging.getLogger("test.cli_runtime.success"),
        generate_request_id_fn=lambda surface: f"{surface}-req-1",
        log_event_fn=lambda logger, **kwargs: logger.info(
            kwargs["event_type"],
            extra=kwargs,
        ),
        run_ingestion_fn=lambda _args: 0,
        run_docling_warmup_fn=lambda _args: 0,
        run_embedding_warmup_fn=lambda: 0,
        run_embedding_generation_fn=lambda _args: 0,
        run_qdrant_indexing_fn=lambda _args: 0,
        run_retrieval_fn=run_retrieval,
        run_grounded_answer_generation_fn=lambda _args, request_id=None: 0,
    )

    assert exit_code == 0
    assert captured_request_ids == ["cli-req-1"]
    event_types = [record.event_type for record in caplog.records if hasattr(record, "event_type")]
    assert event_types.count("request_started") == 1
    assert event_types.count("request_succeeded") == 1


def test_run_cli_request_emits_request_failed_for_non_zero_exit(
    caplog: pytest.LogCaptureFixture,
) -> None:
    caplog.set_level(logging.INFO)

    exit_code = cli_runtime.run_cli_request(
        ["retrieve-chunks", "--query", "What is covered?"],
        build_parser_fn=build_parser,
        get_settings_fn=make_settings,
        configure_logging_fn=lambda _level: None,
        log_startup_diagnostics_fn=lambda logger, settings, runtime_surface: logger.info(
            "startup",
            extra={"event_type": "startup_diagnostics", "runtime_surface": runtime_surface},
        ),
        logger=logging.getLogger("test.cli_runtime.failure"),
        generate_request_id_fn=lambda surface: f"{surface}-req-2",
        log_event_fn=lambda logger, **kwargs: logger.info(
            kwargs["event_type"],
            extra=kwargs,
        ),
        run_ingestion_fn=lambda _args: 0,
        run_docling_warmup_fn=lambda _args: 0,
        run_embedding_warmup_fn=lambda: 0,
        run_embedding_generation_fn=lambda _args: 0,
        run_qdrant_indexing_fn=lambda _args: 0,
        run_retrieval_fn=lambda _args, request_id=None: 3,
        run_grounded_answer_generation_fn=lambda _args, request_id=None: 0,
    )

    assert exit_code == 3
    failure_records = [
        record
        for record in caplog.records
        if getattr(record, "event_type", None) == "request_failed"
    ]
    assert len(failure_records) == 1
    assert failure_records[0].error_type == "CommandExit"
    assert failure_records[0].exit_code == 3
