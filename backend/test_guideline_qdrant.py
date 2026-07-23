from App.services.guideline_loader import load_guidelines
from App.services.guideline_chunker import chunk_guidelines
from App.services.guideline_embedding import generate_embeddings
from App.services.guideline_qdrant import store_guidelines

docs = load_guidelines("App/medical_guidelines")

chunks = chunk_guidelines(docs)

texts, embeddings = generate_embeddings(chunks)

store_guidelines(texts, embeddings)

print("Done!")