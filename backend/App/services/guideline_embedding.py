from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    texts = [chunk.page_content for chunk in chunks]
    embeddings = model.encode(texts).tolist()
    return texts, embeddings