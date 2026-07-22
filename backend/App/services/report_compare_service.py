from sqlalchemy.orm import Session
from App.models.report import Report
import ollama

MODEL_NAME = "llama3"


def compare_latest_reports(
    db: Session,
    patient_id: int,
):

    reports = (
        db.query(Report)
        .filter(Report.patient_id == patient_id)
        .order_by(Report.created_at.desc())
        .limit(2)
        .all()
    )

    if len(reports) < 2:
        return "At least two reports are required."

    latest = reports[0]
    previous = reports[1]

    prompt = f"""
You are an experienced medical AI assistant.

Compare these two medical reports.

Previous Report

Date:
{previous.created_at}

Summary:
{previous.summary}

Latest Report

Date:
{latest.created_at}

Summary:
{latest.summary}

Please answer in this format:

1. Changes
2. Improvements
3. New abnormalities
4. Recommendation

Only use the information above.
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