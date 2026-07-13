from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    store_embedding,
    client,
)

create_collection()

text = "Hemoglobin 13.5 Blood Sugar 95"

embedding = generate_embedding(text)

store_embedding(
    report_id=100,
    embedding=embedding,
    metadata={
        "patient_id": 1,
        "doctor_id": 1,
        "report_name": "Test Report",
        "summary": "Everything normal",
    },
)

print(client.scroll(
    collection_name="medical_reports",
    limit=10,
))