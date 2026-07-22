from sqlalchemy.orm import Session
from App.models.report import Report


def get_critical_patients(db: Session):

    reports = (
        db.query(Report)
        .order_by(Report.created_at.desc())
        .all()
    )

    critical = []

    critical_keywords = [
        "critical",
        "emergency",
        "stroke",
        "heart attack",
        "myocardial infarction",
        "sepsis",
        "cancer",
        "malignant",
        "tumor",
        "organ failure",
        "severe",
        "life threatening",
        "urgent",
    ]

    for report in reports:

        if not report.summary:
            continue

        summary = report.summary.lower()

        if any(keyword in summary for keyword in critical_keywords):
            critical.append({
                "patient_id": report.patient_id,
                "report_name": report.report_name,
                "report_type": report.report_type,
                "created_at": report.created_at,
                "summary": report.summary,
            })

    return critical