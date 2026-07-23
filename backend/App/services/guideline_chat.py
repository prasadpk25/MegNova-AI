import ollama

from App.services.guideline_search import search_guidelines


def ask_guideline(question):
    contexts = search_guidelines(question)

    context = "\n\n".join(contexts)

    prompt = f"""
You are an expert clinical assistant.

Answer ONLY using the medical guideline information below.

If the answer is not present in the guideline,
reply:

"I couldn't find this information in the uploaded clinical guidelines."

Clinical Guidelines:

{context}

Question:

{question}

Answer:
"""

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]