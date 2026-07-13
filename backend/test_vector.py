from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    store_embedding,
    search_embedding,
)

create_collection()

text = """
Hemoglobin: 13.5
Blood Sugar: 95
"""

embedding = generate_embedding(text)

store_embedding(
    report_id=1,
    embedding=embedding,
    metadata={
        "patient": "Prasad",
        "report": text,
    },
)

results = search_embedding(embedding)

print(results)