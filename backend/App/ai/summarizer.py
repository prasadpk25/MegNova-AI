from pathlib import Path
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")

print("ENV FILE:", env_path)
print("API KEY FOUND:", api_key is not None)

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.5-flash")


def summarize_report(report_text: str):
    if not report_text.strip():
        return "No text found."

    prompt = f"""
You are an expert medical AI assistant.

Summarize the following medical report in simple English.

Medical Report:
{report_text}
"""

    response = model.generate_content(prompt)

    return response.text