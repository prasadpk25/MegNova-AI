from sqlalchemy.orm import Session
from App.models.report import Report
import ollama

MODEL_NAME = "llama3"


def ask_patient_history(
    db: Session,
    patient_id: int,
    question: str,
):

    reports = (
        db.query(Report)
        .filter(Report.patient_id == patient_id)
        .order_by(Report.created_at.asc())
        .all()
    )

    if not reports:
        return "No medical reports found for this patient."

    history = ""

    for report in reports:

        history += f"""
Date: {report.created_at}

Report Name: {report.report_name}

Report Type: {report.report_type}

Summary:
{report.summary}

------------------------
"""

    prompt = f"""
You are an experienced medical AI assistant.

Below is the patient's complete medical history.

{history}

Doctor's Question:
{question}

Rules:
1. Answer only using the patient's history.
2. Never make up information.
3. If the answer is unavailable, say so clearly.
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