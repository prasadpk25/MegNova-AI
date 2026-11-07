
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "openai/gpt-oss-20b"

MAX_INPUT_CHARS = 16000
MAX_COMPLETION_TOKENS = 2400


# --------------------------------------------------
# MEDICAL REPORT SUMMARIZER
# --------------------------------------------------

def summarize_report(report_text: str) -> str:
    """
    Generate a concise, evidence-based medical report summary
    using Groq Cloud.

    Important:
    - Uses only information present in the source report.
    - Does not invent clinical findings.
    - Does not provide diagnoses or treatment recommendations.
    """

    # Validate input
    if not report_text or not report_text.strip():
        return "No readable text found in the medical report."

    if not GROQ_API_KEY:
        return "Groq API key is missing. Check backend/.env."

    # Clean input
    cleaned_text = report_text.strip()

    # Limit input size
    was_truncated = len(cleaned_text) > MAX_INPUT_CHARS

    if was_truncated:
        cleaned_text = cleaned_text[:MAX_INPUT_CHARS]

    truncation_note = ""

    if was_truncated:
        truncation_note = (
            "\nIMPORTANT: The original report exceeded the input "
            "limit. This summary covers only the supplied excerpt. "
            "Do not imply that the entire report was reviewed."
        )

    # Construct prompt
    prompt = f"""
You are summarizing a medical laboratory report.

STRICT INSTRUCTIONS:

1. Use ONLY information explicitly present in the source.
2. Never invent patient age, gender, dates or medical history.
3. Preserve laboratory measurements and units accurately.
4. Use reference ranges only when explicitly provided.
5. Identify values outside provided reference ranges without
   independently diagnosing a disease.
6. Do not invent symptoms, clinical findings or test results.
7. Do not recommend medicines or treatment.
8. Clearly mention missing clinical information.
9. If only three laboratory values are supplied, discuss
   only those three values.
10. Keep the response concise and under 500 words.

OUTPUT FORMAT:

## Report Overview
Brief description of the available report information.

## Laboratory Findings
List each available test, its exact result and unit.

## Important Observations
Mention values outside explicitly supplied reference ranges.
If no reference ranges are provided, state that interpretation
is limited.

## Limitations
Mention missing clinical information, symptoms or tests.

This is clinical decision support, not a diagnostic system.
{truncation_note}

SOURCE MEDICAL REPORT:
{cleaned_text}
"""

    try:
        # Initialize Groq
        client = Groq(api_key=GROQ_API_KEY)

        # Request summary
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are MegNova AI, a medical report "
                        "summarization assistant. Be accurate, "
                        "concise and evidence-based. Never invent "
                        "clinical information or provide diagnoses."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            max_completion_tokens=MAX_COMPLETION_TOKENS,
            reasoning_effort="low",
        )

        # Extract response
        choice = response.choices[0]
        summary = choice.message.content

        # Handle empty response
        if not summary or not summary.strip():
            print("Groq returned empty content.")
            print("Finish reason:", choice.finish_reason)
            print("Usage:", response.usage)

            return (
                "AI returned an empty summary. "
                "Please try again."
            )

        # Handle incomplete response
        if choice.finish_reason == "length":
            print(
                "Warning: Summary reached the completion-token limit."
            )

            return (
                summary.strip()
                + "\n\n[Notice: This summary may be incomplete "
                  "because the AI response reached its token limit.]"
            )

        return summary.strip()

    except Exception as error:

        print(
            f"Report summarization error: "
            f"{type(error).__name__}: {error}"
        )

        return (
            f"Summary generation failed: "
            f"{type(error).__name__}"
        )
