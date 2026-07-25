from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    search_embedding,
)

import ollama

MODEL_NAME = "llama3"


def ask_doctor(question: str) -> str:
    """
    Answer a doctor's question using retrieved medical reports.
    """

    try:
        create_collection()

        embedding = generate_embedding(question)

        if embedding is None:
            return "Unable to process the question."

        results = search_embedding(embedding)

        if not results.points:
            return "No medical reports were found."

        context = ""

        for point in results.points[:5]:
            payload = point.payload or {}

            summary = payload.get("summary")

            if not summary:
                continue

            context += f"""
Patient:
{payload.get("patient_name", "Unknown")}

Doctor:
{payload.get("doctor_name", "Unknown")}

Report Name:
{payload.get("report_name", "Unknown")}

Report Type:
{payload.get("report_type", "Unknown")}

Summary:
{summary}

----------------------------------------
"""

        if not context.strip():
            return "No summarized medical reports are available."

        prompt = f"""
You are MegNova AI, an intelligent clinical decision support assistant.

Your job is to answer questions ONLY using the retrieved medical reports.

==============================
Retrieved Medical Reports
==============================

{context}

==============================
Doctor's Question
==============================

{question}

==============================
Instructions
==============================

1. Answer ONLY using the retrieved reports.
2. Never invent, infer, or assume medical information.
3. If the answer is unavailable, reply exactly:
"I could not find this information in the uploaded reports."
4. Keep answers concise and professional.
5. Use bullet points when appropriate.
6. If multiple reports are relevant, summarize all of them.
7. Do not provide diagnosis or treatment recommendations.
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

        return response["message"]["content"].strip()

    except Exception as e:
        return f"Error: {str(e)}"