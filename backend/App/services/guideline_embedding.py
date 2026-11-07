
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    if not chunks:
        return [], []

    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    ).tolist()

    return texts, embeddings
