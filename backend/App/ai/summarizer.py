import ollama

MODEL_NAME = "llama3"


def summarize_report(report_text: str) -> str:
    """
    Generate a concise summary of a medical report using Ollama.
    """

    if not report_text.strip():
        return "No text found."

    prompt = f"""
You are an expert medical AI assistant.

Summarize the following medical report.

Instructions:
- Use simple and professional English.
- Keep the summary concise.
- Mention only clinically important findings.
- If the report appears normal, clearly state that.
- Do not invent or assume information that is not present.
- Do not provide diagnosis or treatment recommendations.

Medical Report:

{report_text}
"""

    try:
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
        return f"Summary generation failed: {str(e)}"