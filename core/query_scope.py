"""Deterministic query-scope classification for supported insurance workflows."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

QueryScope = Literal["supported", "unsupported"]

SUPPORTED_QUERY_TOKENS = {
    "asistencia",
    "assist",
    "arl",
    "auto",
    "autos",
    "accident",
    "accidente",
    "authorization",
    "autorizacion",
    "autorización",
    "benefit",
    "beneficio",
    "bici",
    "bicicleta",
    "bicicletas",
    "bicis",
    "claim",
    "choque",
    "clause",
    "clausula",
    "cláusula",
    "compare",
    "comparison",
    "copay",
    "copago",
    "comparacion",
    "comparación",
    "comparar",
    "complementario",
    "coverage",
    "cobertura",
    "covered",
    "cotizador",
    "deductible",
    "deducible",
    "declinacion",
    "declinación",
    "difference",
    "diferencia",
    "endorsement",
    "endoso",
    "exclusion",
    "exclusión",
    "afiliacion",
    "afiliación",
    "asegurabilidad",
    "factura",
    "hospital",
    "hospitalizacion",
    "hospitalización",
    "insurance",
    "intermediacion",
    "intermediación",
    "intermediario",
    "intermediarios",
    "laborales",
    "poliza",
    "policy",
    "póliza",
    "pac",
    "pospuestos",
    "premium",
    "prima",
    "procedure",
    "procedimiento",
    "registro",
    "reembolso",
    "reimbursement",
    "restriccion",
    "restriction",
    "restricción",
    "evento",
    "eventos",
    "facturacion",
    "facturación",
    "moto",
    "motos",
    "movilidad",
    "muevete",
    "muévete",
    "polizas",
    "pólizas",
    "suscripcion",
    "suscripción",
    "siniestro",
    "soat",
    "patineta",
    "patinetas",
    "tarifa",
    "tarifas",
    "transito",
    "tránsito",
    "travel",
    "utilitario",
    "utilitarios",
    "vehiculo",
    "vehículo",
    "viaje",
    "viajes",
    "versus",
    "vs",
    "pesado",
    "pesados",
    "riesgos",
    "rui",
}


class QueryScopeDecision(BaseModel):
    """Typed scope decision for one user query."""

    scope: QueryScope
    reason: str = Field(min_length=1)


def classify_query_scope(user_query: str) -> QueryScopeDecision:
    """Return a deterministic scope decision for one user query."""

    normalized_tokens = {
        token.strip(".,:;!?()[]{}'\"").lower()
        for token in user_query.split()
        if token.strip(".,:;!?()[]{}'\"")
    }
    if normalized_tokens & SUPPORTED_QUERY_TOKENS:
        return QueryScopeDecision(
            scope="supported",
            reason="Query matches supported insurance-document workflow patterns.",
        )
    return QueryScopeDecision(
        scope="unsupported",
        reason="Query is outside the supported insurance-document scope.",
    )
