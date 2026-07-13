from App.ai.vector_store import client

result = client.scroll(
    collection_name="medical_reports",
    limit=10,
)

print(result)