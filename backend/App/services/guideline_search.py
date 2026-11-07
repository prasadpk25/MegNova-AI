from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from pathlib import Path

DB_PATH = str(Path(__file__).resolve().parents[2] / "qdrant_db")
client = QdrantClient(path=DB_PATH)
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