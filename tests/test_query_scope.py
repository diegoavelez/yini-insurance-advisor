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


def test_classify_query_scope_supports_soat_queries() -> None:
    decision = classify_query_scope("¿Cuáles son las tarifas del SOAT 2026?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_muevete_libre_queries() -> None:
    decision = classify_query_scope("¿Qué cubre Muévete Libre?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_choque_simple_queries() -> None:
    decision = classify_query_scope("¿Qué debo hacer en un choque simple?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_utilitarios_pesados_queries() -> None:
    decision = classify_query_scope("¿Qué cubre el plan de utilitarios y pesados?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_viajes_queries() -> None:
    decision = classify_query_scope("¿Qué cubre el seguro de viajes internacional?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_pac_queries() -> None:
    decision = classify_query_scope("¿Qué cubre el PAC 60 Más?")

    assert decision.scope == "supported"


def test_classify_query_scope_supports_pac_operational_queries() -> None:
    decision = classify_query_scope(
        "¿Cómo actualizar el correo para factura global web del plan complementario PAC?"
    )

    assert decision.scope == "supported"


def test_classify_query_scope_supports_suscripcion_facturacion_por_asegurado_queries() -> None:
    decision = classify_query_scope(
        "¿Qué condiciones aplican a la facturación por asegurado en pólizas colectivas?"
    )

    assert decision.scope == "supported"


def test_classify_query_scope_keeps_non_insurance_spanish_queries_unsupported() -> None:
    decision = classify_query_scope("¿Cómo está el clima en Bogotá hoy?")

    assert decision.scope == "unsupported"
