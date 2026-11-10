from pathlib import Path
from qdrant_client import QdrantClient

DB_PATH = Path(__file__).resolve().parent / "qdrant_db"

client = QdrantClient(path=str(DB_PATH))