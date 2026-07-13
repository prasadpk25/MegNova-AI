from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Convert text into a vector embedding.
    """
    if not text.strip():
        return None

    embedding = model.encode(text)

    return embedding.tolist()