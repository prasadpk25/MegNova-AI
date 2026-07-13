from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
)

client = QdrantClient(path="App/qdrant_db")

COLLECTION_NAME = "medical_reports"


def create_collection():
    collections = client.get_collections().collections

    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def store_embedding(
    report_id: int,
    embedding: list,
    metadata: dict,
):
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
    embedding: list,
    limit: int = 3,
):
    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=limit,
    )