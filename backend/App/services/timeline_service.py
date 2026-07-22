from sqlalchemy.orm import Session
from App.models.report import Report


def get_patient_timeline(db: Session, patient_id: int):

    reports = (
        db.query(Report)
        .filter(Report.patient_id == patient_id)
        .order_by(Report.created_at.desc())
        .all()
    )

    return reports