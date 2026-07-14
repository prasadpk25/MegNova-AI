from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    search_embedding,
)

import ollama

MODEL_NAME = "llama3"    # Change to llama3.2 if needed


def ask_doctor(question: str):

    create_collection()

    embedding = generate_embedding(question)

    results = search_embedding(embedding)

    if not results.points:
        return "No medical reports were found."

    context = ""

    for point in results.points:

        payload = point.payload

        context += f"""
Report Name:
{payload.get("report_name")}

Summary:
{payload.get("summary")}

"""

    prompt = f"""
You are an experienced medical AI assistant.

Answer ONLY using the information below.

Medical Reports

{context}

Doctor Question

{question}

Rules

1. Never make up information.
2. Answer only from the reports.
3. If the answer is unavailable, say:
"I could not find this information in the uploaded reports."
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]