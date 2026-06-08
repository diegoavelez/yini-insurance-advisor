from __future__ import annotations

from core.query_scope import classify_query_scope


def test_classify_query_scope_keeps_english_supported_queries_supported() -> None:
    decision = classify_query_scope("Compare coverage and deductible requirements.")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_spanish_insurance_queries() -> None:
    decision = classify_query_scope("¿Qué cobertura aplica a la hospitalización y al deducible?")

    assert decision.scope == "supported"


def test_classify_query_scope_keeps_non_insurance_spanish_queries_unsupported() -> None:
    decision = classify_query_scope("¿Cómo está el clima en Bogotá hoy?")

    assert decision.scope == "unsupported"
