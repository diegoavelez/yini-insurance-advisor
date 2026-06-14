from __future__ import annotations

from pathlib import Path

from contracts import QueryExpansionRule, TermEquivalenceSet
from rag.term_equivalences import (
    augment_query_with_term_equivalences,
    load_term_equivalences,
    normalize_equivalence_text,
    query_contains_equivalent_phrase,
    tokenize_lexical_surface,
)


def test_normalize_equivalence_text_strips_accents_and_collapses_whitespace() -> None:
    assert normalize_equivalence_text("  Muévete   Libre \n") == "muevete libre"


def test_query_contains_equivalent_phrase_uses_word_boundaries() -> None:
    assert query_contains_equivalent_phrase("Quiero póliza colectiva", "poliza colectiva")
    assert not query_contains_equivalent_phrase("polizacolectiva", "poliza colectiva")


def test_augment_query_with_term_equivalences_appends_canonical_terms_once() -> None:
    augmented_query = augment_query_with_term_equivalences(
        "¿Qué cubre Muévete Libre?",
        TermEquivalenceSet(
            query_aliases={"muevete libre": ["muévete libre"]},
            query_expansion_rules=[
                QueryExpansionRule(
                    all_of=["muevete libre"],
                    any_of=["qué cubre", "cubre"],
                    append_terms=["cobertura", "cobertura"],
                )
            ],
        ),
    )

    assert augmented_query.endswith("Términos equivalentes: cobertura")


def test_tokenize_lexical_surface_returns_normalized_tokens() -> None:
    assert tokenize_lexical_surface("Actualización de cuenta bancaria") == {
        "actualizacion",
        "cuenta",
        "bancaria",
    }


def test_load_term_equivalences_returns_empty_set_for_missing_file() -> None:
    assert load_term_equivalences(Path("ops/does-not-exist.json")) == TermEquivalenceSet()
