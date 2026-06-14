"""Shared lexical normalization helpers for retrieval term equivalences."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from contracts import TermEquivalenceSet

DEFAULT_TERM_EQUIVALENCE_PATH = "ops/term-equivalences.json"


def normalize_equivalence_text(value: str) -> str:
    """Normalize one term-equivalence key for stable phrase matching."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return " ".join(ascii_text.strip().lower().split())


def load_term_equivalences(term_equivalence_path: Path | None = None) -> TermEquivalenceSet:
    """Load optional operator-curated term equivalences."""

    resolved_path = term_equivalence_path or Path(DEFAULT_TERM_EQUIVALENCE_PATH)
    if not resolved_path.exists():
        return TermEquivalenceSet()
    return TermEquivalenceSet.model_validate_json(resolved_path.read_text(encoding="utf-8"))


def query_contains_equivalent_phrase(query: str, phrase: str) -> bool:
    """Return whether a normalized phrase appears in the normalized query."""

    normalized_phrase = normalize_equivalence_text(phrase)
    if not normalized_phrase:
        return False
    pattern = rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"
    return re.search(pattern, normalize_equivalence_text(query)) is not None


def augment_query_with_term_equivalences(query: str, term_equivalences: TermEquivalenceSet) -> str:
    """Append operator-curated canonical terms when aliases appear in the query."""

    appended_terms: list[str] = []
    appended_term_keys: set[str] = set()

    def append_term_if_missing(term: str) -> None:
        normalized_term = normalize_equivalence_text(term)
        if not normalized_term:
            return
        if query_contains_equivalent_phrase(query, term):
            return
        if normalized_term in appended_term_keys:
            return
        appended_terms.append(term)
        appended_term_keys.add(normalized_term)

    for canonical_term, aliases in term_equivalences.query_aliases.items():
        if any(query_contains_equivalent_phrase(query, alias) for alias in aliases):
            append_term_if_missing(canonical_term)

    for expansion_rule in term_equivalences.query_expansion_rules:
        matches_all = all(
            query_contains_equivalent_phrase(query, phrase)
            for phrase in expansion_rule.all_of
        )
        matches_any = not expansion_rule.any_of or any(
            query_contains_equivalent_phrase(query, phrase) for phrase in expansion_rule.any_of
        )
        if not (matches_all and matches_any):
            continue
        for appended_term in expansion_rule.append_terms:
            append_term_if_missing(appended_term)

    if not appended_terms:
        return query
    return f"{query}\n\nTérminos equivalentes: {', '.join(appended_terms)}"


def get_matching_query_expansion_rules(
    query: str,
    *,
    term_equivalences: TermEquivalenceSet,
) -> list[object]:
    """Return operator-curated query-expansion rules that match the query."""

    matched_rules: list[object] = []
    for expansion_rule in term_equivalences.query_expansion_rules:
        matches_all = all(
            query_contains_equivalent_phrase(query, phrase)
            for phrase in expansion_rule.all_of
        )
        matches_any = not expansion_rule.any_of or any(
            query_contains_equivalent_phrase(query, phrase) for phrase in expansion_rule.any_of
        )
        if matches_all and matches_any:
            matched_rules.append(expansion_rule)
    return matched_rules


def tokenize_lexical_surface(value: str) -> set[str]:
    """Return normalized lexical tokens for deterministic local recall."""

    normalized_text = normalize_equivalence_text(value)
    return {
        token
        for token in re.split(r"[^a-z0-9]+", normalized_text)
        if len(token) >= 3
    }
