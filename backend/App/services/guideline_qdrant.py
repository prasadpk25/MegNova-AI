from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

client = QdrantClient(path="qdrant_db")

COLLECTION_NAME = "clinical_guidelines"

# Create collection if it doesn't exist
collections = client.get_collections().collections
existing = [c.name for c in collections]

if COLLECTION_NAME not in existing:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        ),
    )
    print(f"Created collection: {COLLECTION_NAME}")


def store_guidelines(texts, embeddings):
    points = []

    for text, vector in zip(texts, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": text
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Stored {len(points)} guideline chunks.")