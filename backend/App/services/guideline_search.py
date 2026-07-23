from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(path="qdrant_db")
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "clinical_guidelines"


def search_guidelines(query, limit=5):
    query_vector = model.encode(query).tolist()

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    )

    return [point.payload["text"] for point in response.points]