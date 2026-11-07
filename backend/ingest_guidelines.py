from App.services.guideline_loader import load_guidelines
from App.services.guideline_chunker import chunk_guidelines
from App.services.guideline_embedding import generate_embeddings
from App.services.guideline_qdrant import store_guidelines


def main():
    print("Loading medical guidelines...")
    docs = load_guidelines("App/medical_guidelines")

    print(f"Loaded {len(docs)} documents")

    print("Creating guideline chunks...")
    chunks = chunk_guidelines(docs)

    print(f"Created {len(chunks)} chunks")

    print("Generating embeddings...")
    texts, embeddings = generate_embeddings(chunks)

    print("Storing guidelines in Qdrant...")
    store_guidelines(texts, embeddings)

    print("Medical guideline ingestion completed!")


if __name__ == "__main__":
    main()