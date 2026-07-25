from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

client = QdrantClient(path="App/qdrant_db")

COLLECTION_NAME = "medical_reports"
VECTOR_SIZE = 384


def create_collection() -> None:
    """Create the Qdrant collection if it does not already exist."""

    collections = client.get_collections().collections
    names = [collection.name for collection in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_embedding(
    report_id: int,
    embedding: list[float],
    metadata: dict,
) -> None:
    """Store or update a report embedding."""

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=report_id,
                vector=embedding,
                payload=metadata,
            )
        ],
    )


def search_embedding(
    embedding: list[float],
    limit: int = 3,
):
    """Search similar reports."""

    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit,
    )