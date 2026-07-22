from sqlalchemy.orm import Session

from App.models.patient import Patient
from App.models.doctor import Doctor
from App.models.appointment import Appointment
from App.models.report import Report
from App.services.critical_patient_service import get_critical_patients


def get_dashboard_data(db: Session):

    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()
    total_appointments = db.query(Appointment).count()
    total_reports = db.query(Report).count()
    critical_patients = get_critical_patients(db)

    recent_reports = (
        db.query(Report)
        .order_by(Report.created_at.desc())
        .limit(5)
        .all()
    )

    reports = []

    for report in recent_reports:
        reports.append({
            "patient_id": report.patient_id,
            "report_name": report.report_name,
            "report_type": report.report_type,
            "created_at": report.created_at,
        })

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "total_reports": total_reports,
        "recent_reports": reports,
        "critical_patients": critical_patients
    }