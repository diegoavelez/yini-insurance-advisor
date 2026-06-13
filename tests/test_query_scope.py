from __future__ import annotations

from core.query_scope import classify_query_scope


def test_classify_query_scope_keeps_english_supported_queries_supported() -> None:
    decision = classify_query_scope("Compare coverage and deductible requirements.")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_spanish_insurance_queries() -> None:
    decision = classify_query_scope("¿Qué cobertura aplica a la hospitalización y al deducible?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_spanish_autos_assistance_queries() -> None:
    decision = classify_query_scope("¿Qué cubre la asistencia en pequeños eventos para autos?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_spanish_arl_rui_queries() -> None:
    decision = classify_query_scope(
        "¿Cuál es la normatividad que rige el registro único de intermediarios en ARL?"
    )

    assert decision.scope == "supported"


def test_classify_query_scope_supports_spanish_bicicletas_y_patinetas_queries() -> None:
    decision = classify_query_scope("¿Qué cubre el seguro para bicicletas y patinetas?")

    assert decision.scope == "supported"


def test_classify_query_scope_keeps_non_insurance_spanish_queries_unsupported() -> None:
    decision = classify_query_scope("¿Cómo está el clima en Bogotá hoy?")

    assert decision.scope == "unsupported"
