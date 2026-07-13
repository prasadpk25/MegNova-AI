from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    search_embedding,
)
from App.ai.summarizer import model


def ask_doctor(question: str):
    create_collection()
    embedding = generate_embedding(question)

    results = search_embedding(embedding)

    context = ""

    for point in results.points:
        payload = point.payload

        context += f"""
Report Name: {payload.get("report_name")}

Summary:
{payload.get("summary")}

"""

    prompt = f"""
You are an AI medical assistant.

Use ONLY the medical reports below to answer.

Medical Reports:
{context}

Doctor Question:
{question}

If the answer is not present in the reports, reply:
"I could not find this information in the uploaded reports."
"""

    response = model.generate_content(prompt)

    return response.text