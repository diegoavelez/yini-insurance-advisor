from __future__ import annotations

import importlib
import time
import uuid

from contracts import EmbeddingBundle, EmbeddingRecord, RetrievalQuery, RetrievedChunk
from core.config import Settings

QDRANT_POINT_ID_NAMESPACE = uuid.UUID("8c39ce79-53d7-47e5-baad-95c5f1548599")
QDRANT_FILTERABLE_PAYLOAD_FIELDS = (
    "document_type",
    "product",
    "document_name",
    "source_pdf_id",
)


def get_qdrant_models():
    """Return the installed Qdrant models module."""

    return importlib.import_module("qdrant_client.http.models")


def create_qdrant_client(settings: Settings):
    """Instantiate the configured Qdrant client."""

    qdrant_client_module = importlib.import_module("qdrant_client")
    return qdrant_client_module.QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key.get_secret_value() if settings.qdrant_api_key else None,
    )


def build_qdrant_point_id(embedding_record: EmbeddingRecord) -> str:
    """Return the deterministic Qdrant point id for one embedding record."""

    return str(uuid.uuid5(QDRANT_POINT_ID_NAMESPACE, embedding_record.chunk_id))


def build_qdrant_point_payload(embedding_record: EmbeddingRecord) -> dict[str, object]:
    """Map a typed embedding record into a Qdrant payload."""

    return {
        "chunk_id": embedding_record.chunk_id,
        "source_pdf_id": embedding_record.source_pdf_id,
        "source_pdf_relative_path": embedding_record.payload.source_pdf_relative_path,
        "chunk_schema_version": embedding_record.chunk_schema_version,
        "embedding_provider": embedding_record.embedding_provider,
        "embedding_model": embedding_record.embedding_model,
        "document_name": embedding_record.payload.document_name,
        "document_version": embedding_record.payload.document_version,
        "document_type": embedding_record.payload.document_type,
        "product": embedding_record.payload.product,
        "chunk_index": embedding_record.payload.chunk_index,
        "section": embedding_record.payload.section,
        "section_path": embedding_record.payload.section_path,
        "text": embedding_record.payload.text,
    }


def build_qdrant_query_filter(filters: object) -> object | None:
    """Map typed retrieval filters into a Qdrant filter object."""

    filter_mappings = {
        "document_type": "document_type",
        "product": "product",
        "document_name": "document_name",
        "version": "document_version",
    }
    filter_values = {
        field_name: getattr(filters, field_name, None) for field_name in filter_mappings
    }
    if all(value is None for value in filter_values.values()):
        return None

    conditions: list[object] = []
    qdrant_models = get_qdrant_models()

    for field_name, payload_key in filter_mappings.items():
        value = filter_values[field_name]
        if value is None:
            continue
        conditions.append(
            qdrant_models.FieldCondition(
                key=payload_key,
                match=qdrant_models.MatchValue(value=value),
            )
        )

    if not conditions:
        return None

    return qdrant_models.Filter(must=conditions)


def build_qdrant_source_pdf_filter(source_pdf_id: str) -> object:
    """Build a narrow Qdrant filter that matches one source document family."""

    qdrant_models = get_qdrant_models()
    return qdrant_models.Filter(
        must=[
            qdrant_models.FieldCondition(
                key="source_pdf_id",
                match=qdrant_models.MatchValue(value=source_pdf_id),
            )
        ]
    )


def build_qdrant_points(embedding_bundle: EmbeddingBundle) -> list[object]:
    """Map one embedding bundle into deterministic Qdrant points."""

    qdrant_models = get_qdrant_models()
    return [
        qdrant_models.PointStruct(
            id=build_qdrant_point_id(embedding_record),
            vector=embedding_record.vector,
            payload=build_qdrant_point_payload(embedding_record),
        )
        for embedding_record in embedding_bundle.embeddings
    ]


def map_search_hit_to_retrieved_chunk(hit: object) -> RetrievedChunk:
    """Map one Qdrant search hit into a typed retrieval result."""

    payload = getattr(hit, "payload", None)
    if not isinstance(payload, dict):
        raise RuntimeError("Qdrant search hit payload is missing or invalid.")

    chunk_id = payload.get("chunk_id")
    text = payload.get("text")
    document_name = payload.get("document_name")
    if (
        not isinstance(chunk_id, str)
        or not isinstance(text, str)
        or not isinstance(document_name, str)
    ):
        raise RuntimeError("Qdrant search hit payload is missing required retrieval fields.")

    score = getattr(hit, "score", None)
    if score is None:
        score = 0.0

    source_pdf_id = payload.get("source_pdf_id")
    if not isinstance(source_pdf_id, str):
        source_pdf_id = None
    source_pdf_relative_path = payload.get("source_pdf_relative_path")
    if not isinstance(source_pdf_relative_path, str):
        source_pdf_relative_path = None
    chunk_schema_version = payload.get("chunk_schema_version")
    if not isinstance(chunk_schema_version, str):
        chunk_schema_version = None
    chunk_index = payload.get("chunk_index")
    if not isinstance(chunk_index, int):
        chunk_index = None
    document_version = payload.get("document_version")
    if not isinstance(document_version, str):
        document_version = None
    document_type = payload.get("document_type")
    if not isinstance(document_type, str):
        document_type = None
    product = payload.get("product")
    if not isinstance(product, str):
        product = None
    page = payload.get("page")
    if not isinstance(page, int):
        page = None
    section = payload.get("section")
    if not isinstance(section, str):
        section = None
    section_path = payload.get("section_path")
    if not isinstance(section_path, list) or not all(
        isinstance(value, str) for value in section_path
    ):
        section_path = []
    clause_id = payload.get("clause_id")
    if not isinstance(clause_id, str):
        clause_id = None

    return RetrievedChunk(
        chunk_id=chunk_id,
        source_pdf_id=source_pdf_id,
        source_pdf_relative_path=source_pdf_relative_path,
        chunk_schema_version=chunk_schema_version,
        chunk_index=chunk_index,
        text=text,
        document_name=document_name,
        document_version=document_version,
        document_type=document_type,
        product=product,
        page=page,
        section=section,
        section_path=section_path,
        clause_id=clause_id,
        score=float(score),
    )


def search_qdrant_chunks(
    *,
    client: object,
    settings: Settings,
    retrieval_query: RetrievalQuery,
    query_vector: list[float],
    candidate_limit: int | None = None,
) -> list[object]:
    """Execute one Qdrant search for retrieval."""

    query_filter = build_qdrant_query_filter(retrieval_query.filters)
    resolved_limit = candidate_limit or retrieval_query.top_k
    if hasattr(client, "search"):
        return client.search(
            collection_name=settings.qdrant_collection,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=resolved_limit,
            with_payload=True,
        )
    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_vector,
            query_filter=query_filter,
            limit=resolved_limit,
            with_payload=True,
        )
        points = getattr(response, "points", None)
        if not isinstance(points, list):
            raise RuntimeError("Qdrant query_points response did not include ranked points.")
        return points
    raise RuntimeError("Installed Qdrant client does not expose a supported retrieval method.")


def get_collection_vector_size(collection_info: object) -> int | None:
    """Extract collection vector size from a Qdrant collection descriptor."""

    config = getattr(collection_info, "config", None)
    params = getattr(config, "params", None)
    vectors = getattr(params, "vectors", None)
    if vectors is None:
        return None
    size = getattr(vectors, "size", None)
    if isinstance(size, int):
        return size
    if isinstance(vectors, dict):
        first_vector = next(iter(vectors.values()), None)
        nested_size = getattr(first_vector, "size", None)
        if isinstance(nested_size, int):
            return nested_size
    return None


def ensure_qdrant_collection(client: object, settings: Settings, vector_size: int) -> None:
    """Create or validate the target Qdrant collection."""

    qdrant_models = get_qdrant_models()

    try:
        collection_info = client.get_collection(settings.qdrant_collection)
    except Exception:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=qdrant_models.VectorParams(
                size=vector_size,
                distance=qdrant_models.Distance.COSINE,
            ),
        )
        collection_info = client.get_collection(settings.qdrant_collection)

    configured_size = get_collection_vector_size(collection_info)
    if configured_size != vector_size:
        raise RuntimeError(
            "Configured Qdrant collection is incompatible with the embedding vector dimension."
        )

    ensure_qdrant_payload_indexes(client, settings)


def ensure_qdrant_payload_indexes(client: object, settings: Settings) -> None:
    """Ensure payload indexes exist for retrieval-facing metadata filters."""

    create_payload_index = getattr(client, "create_payload_index", None)
    if not callable(create_payload_index):
        return

    qdrant_models = get_qdrant_models()
    field_schema_keyword = getattr(qdrant_models, "PayloadSchemaType", None)
    keyword_value = getattr(field_schema_keyword, "KEYWORD", "keyword")

    for field_name in QDRANT_FILTERABLE_PAYLOAD_FIELDS:
        create_payload_index(
            collection_name=settings.qdrant_collection,
            field_name=field_name,
            field_schema=keyword_value,
            wait=True,
        )


def is_transient_qdrant_error(exc: Exception) -> bool:
    """Return whether an indexing exception is retryable."""

    return bool(
        getattr(exc, "transient", False)
        or isinstance(exc, TimeoutError)
        or isinstance(exc, ConnectionError)
    )


def sleep_with_backoff(delay_seconds: float) -> None:
    """Sleep for the configured retry backoff duration."""

    time.sleep(delay_seconds)


def upsert_points_with_retry(
    *,
    client: object,
    settings: Settings,
    points: list[object],
    max_retries: int,
    retry_backoff_seconds: float,
) -> None:
    """Upsert Qdrant points with deterministic retry behavior."""

    attempt = 0
    while True:
        try:
            client.upsert(collection_name=settings.qdrant_collection, points=points, wait=True)
            return
        except Exception as exc:
            if attempt >= max_retries or not is_transient_qdrant_error(exc):
                raise
            sleep_with_backoff(retry_backoff_seconds * (2**attempt))
            attempt += 1


def prune_existing_source_points(
    *,
    client: object,
    settings: Settings,
    source_pdf_id: str,
) -> None:
    """Delete existing points for one source PDF before reindexing that bundle."""

    delete_points = getattr(client, "delete", None)
    if not callable(delete_points):
        return
    delete_points(
        collection_name=settings.qdrant_collection,
        points_selector=build_qdrant_source_pdf_filter(source_pdf_id),
        wait=True,
    )


def smoke_validate_indexing(client: object, settings: Settings, expected_points: int) -> None:
    """Run a narrow operational smoke check after indexing."""

    count_response = client.count(collection_name=settings.qdrant_collection, exact=True)
    count_value = getattr(count_response, "count", None)
    if not isinstance(count_value, int) or count_value < min(expected_points, 1):
        raise RuntimeError("Qdrant smoke validation did not confirm indexed points.")
