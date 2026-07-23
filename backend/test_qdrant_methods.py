from qdrant_client import QdrantClient

client = QdrantClient(path="qdrant_db")

methods = [m for m in dir(client) if "search" in m.lower() or "query" in m.lower()]

print(methods)