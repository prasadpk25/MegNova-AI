import ollama

MODEL_NAME = "llama3"   # Change to "llama3.2" if that's the model you downloaded


def summarize_report(report_text: str):

    if not report_text.strip():
        return "No text found."

    prompt = f"""
You are an expert medical AI assistant.

Summarize the following medical report in simple English.

Keep the summary:
- Short
- Accurate
- Easy for doctors to understand
- Mention important abnormalities if present.

Medical Report:

{report_text}
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