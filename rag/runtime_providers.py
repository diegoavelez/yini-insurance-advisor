from __future__ import annotations

from collections.abc import Callable

from core.config import Settings


def validate_embedding_settings(
    settings: Settings,
    *,
    supported_embedding_provider: str,
) -> Settings:
    """Validate embedding configuration for offline artifact generation."""

    if settings.embedding_provider != supported_embedding_provider:
        raise RuntimeError(
            "EMBEDDING_PROVIDER must be sentence-transformers for offline embedding generation."
        )
    if not settings.embedding_model.strip():
        raise RuntimeError("EMBEDDING_MODEL must not be blank for embedding generation.")
    return settings


def embedding_backend_is_available(
    settings: Settings,
    *,
    supported_embedding_provider: str,
    find_spec_fn: Callable[[str], object | None],
) -> bool:
    """Return whether the configured embedding backend is importable."""

    if settings.embedding_provider != supported_embedding_provider:
        return False
    return find_spec_fn("sentence_transformers") is not None


def ensure_embedding_backend_available(
    settings: Settings,
    *,
    embedding_backend_is_available_fn: Callable[[Settings], bool],
) -> None:
    """Fail loudly when the configured embedding backend is unavailable."""

    if not embedding_backend_is_available_fn(settings):
        raise RuntimeError(
            "Sentence Transformers is not installed. Install project dependencies "
            "before running embedding generation."
        )


def qdrant_backend_is_available(
    *,
    find_spec_fn: Callable[[str], object | None],
) -> bool:
    """Return whether the Qdrant client is importable."""

    return find_spec_fn("qdrant_client") is not None


def ensure_qdrant_backend_available(
    *,
    qdrant_backend_is_available_fn: Callable[[], bool],
) -> None:
    """Fail loudly when the Qdrant client is unavailable."""

    if not qdrant_backend_is_available_fn():
        raise RuntimeError(
            "qdrant-client is not installed. Install project dependencies before "
            "running Qdrant indexing."
        )


def groq_backend_is_available(
    *,
    find_spec_fn: Callable[[str], object | None],
) -> bool:
    """Return whether the Groq client is importable."""

    return find_spec_fn("groq") is not None


def ensure_groq_backend_available(
    *,
    groq_backend_is_available_fn: Callable[[], bool],
) -> None:
    """Fail loudly when the Groq client is unavailable."""

    if not groq_backend_is_available_fn():
        raise RuntimeError(
            "groq is not installed. Install project dependencies before running "
            "grounded answer generation."
        )


def create_groq_client(
    settings: Settings,
    *,
    import_module_fn: Callable[[str], object],
):
    """Create a configured Groq client from validated settings."""

    groq_module = import_module_fn("groq")
    return groq_module.Groq(api_key=settings.groq_api_key.get_secret_value())


def load_sentence_transformer(
    model_name: str,
    *,
    local_files_only: bool = True,
    import_module_fn: Callable[[str], object],
    offline_huggingface_resolution_fn,
):
    """Return a SentenceTransformer instance with optional offline enforcement."""

    try:
        with offline_huggingface_resolution_fn(enabled=local_files_only):
            sentence_transformers = import_module_fn("sentence_transformers")
            return sentence_transformers.SentenceTransformer(
                model_name,
                local_files_only=local_files_only,
            )
    except TypeError:
        if local_files_only:
            raise RuntimeError(
                "Installed sentence-transformers version does not support offline "
                "local_files_only loading."
            ) from None
        return sentence_transformers.SentenceTransformer(model_name)


def ensure_embedding_model_assets_available(
    settings: Settings,
    *,
    load_sentence_transformer_fn: Callable[..., object],
) -> None:
    """Fail loudly when embedding-model assets are not cached locally."""

    try:
        load_sentence_transformer_fn(settings.embedding_model, local_files_only=True)
    except Exception as exc:
        raise RuntimeError(
            "Embedding model assets are not cached locally for "
            f"{settings.embedding_model}. Run `python -m rag.ingestion "
            "warmup-embedding-assets` once with network access, or pre-populate "
            "the Hugging Face cache before running offline embedding or retrieval commands."
        ) from exc


def generate_embedding_vector(
    text: str,
    settings: Settings,
    *,
    supported_embedding_provider: str,
    ensure_embedding_model_assets_available_fn: Callable[[Settings], None],
    load_sentence_transformer_fn: Callable[..., object],
) -> list[float]:
    """Generate one embedding vector for chunk text."""

    if settings.embedding_provider != supported_embedding_provider:
        raise RuntimeError("Unsupported embedding provider for local embedding generation.")

    ensure_embedding_model_assets_available_fn(settings)
    model = load_sentence_transformer_fn(settings.embedding_model, local_files_only=True)
    vector = model.encode([text], normalize_embeddings=True)[0]
    return [float(value) for value in vector]


def generate_grounded_completion(
    prompt: str,
    settings: Settings,
    *,
    create_groq_client_fn: Callable[[Settings], object],
) -> str:
    """Generate grounded completion text through Groq."""

    client = create_groq_client_fn(settings)
    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an internal insurance assistant. Answer only from the "
                    "provided evidence. If evidence is insufficient, say so explicitly."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    message = response.choices[0].message
    content = getattr(message, "content", None)
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Groq did not return grounded answer content.")
    return content.strip()
