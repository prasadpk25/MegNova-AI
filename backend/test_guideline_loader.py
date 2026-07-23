from App.services.guideline_loader import load_guidelines
from App.services.guideline_chunker import chunk_guidelines

docs = load_guidelines("App/medical_guidelines")

print(f"\nLoaded {len(docs)} PDFs\n")

chunks = chunk_guidelines(docs)

print(f"Created {len(chunks)} chunks\n")

for chunk in chunks[:3]:
    print("=" * 80)
    print(chunk.metadata)
    print(chunk.page_content[:300])