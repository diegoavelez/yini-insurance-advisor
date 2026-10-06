"""Real corpus checks: separately authorized opt-in, with no collection-time reads."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from contracts import RetrievalQuery
from rag.ingestion import normalize_retrieval_query_with_term_equivalences
from rag.term_equivalences import load_term_equivalences, normalize_equivalence_text

pytestmark = pytest.mark.corpus_evaluation
MOVILIDAD_DEDUCTIBLES_QA_PATH = Path("data/eval/movilidad-deductibles-qa.json")


@pytest.fixture(scope="module")
def corpus_cases(request: pytest.FixtureRequest) -> list[dict[str, object]]:
    if not request.config.getoption("--run-corpus-evaluation"):
        pytest.fail("Corpus evaluation requires explicit --run-corpus-evaluation")
    payload = json.loads(MOVILIDAD_DEDUCTIBLES_QA_PATH.read_text(encoding="utf-8"))
    cases = payload["cases"]
    assert cases, "Corpus evaluation must not pass with zero cases"
    return cases


def combined_chunk_text(chunk_files: list[str]) -> str:
    text_parts: list[str] = []
    for chunk_file in chunk_files:
        payload = json.loads(Path(chunk_file).read_text(encoding="utf-8"))
        text_parts.extend(chunk["text"] for chunk in payload["chunks"])
    return "\n".join(text_parts)


def test_movilidad_deductibles_qa_cases_normalize_to_expected_filters(
    corpus_cases: list[dict[str, object]],
) -> None:
    for case in corpus_cases:
        normalized_query = normalize_retrieval_query_with_term_equivalences(
            RetrievalQuery(query=str(case["prompt"])),
            term_equivalences=load_term_equivalences(Path("ops/term-equivalences.json")),
        )
        expected_filters = case["expected_filters"]
        assert isinstance(expected_filters, dict)
        for field_name, expected_value in expected_filters.items():
            assert getattr(normalized_query.filters, field_name) == expected_value, case["case_id"]


def test_movilidad_deductibles_qa_expected_terms_exist_in_local_chunks(
    corpus_cases: list[dict[str, object]],
) -> None:
    for case in corpus_cases:
        chunk_files = case["expected_chunk_files"]
        expected_terms = case["expected_answer_terms"]
        assert isinstance(chunk_files, list)
        assert isinstance(expected_terms, list)
        chunk_surface = normalize_equivalence_text(
            combined_chunk_text([str(chunk_file) for chunk_file in chunk_files])
        )
        for expected_term in expected_terms:
            assert normalize_equivalence_text(str(expected_term)) in chunk_surface, case["case_id"]
