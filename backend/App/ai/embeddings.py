from sentence_transformers import SentenceTransformer

# Load embedding model once during application startup
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float] | None:
    """
    Convert text into a vector embedding.
    """

    if not text.strip():
        return None

    try:
        embedding = model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    except Exception:
        return None