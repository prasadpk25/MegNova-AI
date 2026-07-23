from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from App.database.database import SessionLocal
from App.models.patient import Patient
from App.models.doctor import Doctor
from App.models.report import Report

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    total_patients = db.query(Patient).count()
    active_patients = db.query(Patient).filter(Patient.is_active == True).count()

    total_doctors = db.query(Doctor).count()
    active_doctors = db.query(Doctor).filter(Doctor.is_active == True).count()

    total_reports = db.query(Report).count()

    departments = (
        db.query(
            Doctor.department,
            func.count(Doctor.id)
        )
        .group_by(Doctor.department)
        .all()
    )

    specializations = (
        db.query(
            Doctor.specialization,
            func.count(Doctor.id)
        )
        .group_by(Doctor.specialization)
        .all()
    )

    report_types = (
        db.query(
            Report.report_type,
            func.count(Report.id)
        )
        .group_by(Report.report_type)
        .all()
    )

    return {
        "total_patients": total_patients,
        "active_patients": active_patients,

        "total_doctors": total_doctors,
        "active_doctors": active_doctors,

        "total_reports": total_reports,

        "departments": [
            {"department": d, "count": c}
            for d, c in departments
        ],

        "specializations": [
            {"specialization": s, "count": c}
            for s, c in specializations
        ],

        "report_types": [
            {"type": t, "count": c}
            for t, c in report_types
        ],
    }