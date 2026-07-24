from sqlalchemy.orm import Session, joinedload

from App.models.report import Report
from App.schemas.report import ReportCreate


class ReportRepository:

    @staticmethod
    def create_report(
        db: Session,
        report: ReportCreate,
        file_name: str,
        file_path: str,
        uploaded_by: int,
        extracted_text: str,
        summary: str,
    ):
        report_count = db.query(Report).count() + 1

        report_id = f"MR{report_count:06d}"

        new_report = Report(
            report_id=report_id,
            patient_id=report.patient_id,
            doctor_id=report.doctor_id,
            report_name=report.report_name,
            report_type=report.report_type,
            file_name=file_name,
            file_path=file_path,
            extracted_text=extracted_text,
            summary=summary,
            uploaded_by=uploaded_by,
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return new_report

    @staticmethod
    def get_all_reports(db: Session):
        return (
            db.query(Report)
            .options(
                joinedload(Report.patient),
                joinedload(Report.doctor),
            )
            .filter(Report.is_active == True)
            .all()
        )

    @staticmethod
    def get_report_by_id(
        db: Session,
        report_id: int,
    ):
        return (
            db.query(Report)
            .filter(
                Report.id == report_id,
                Report.is_active == True,
            )
            .first()
        )

    @staticmethod
    def delete_report(
        db: Session,
        report: Report,
    ):
        report.is_active = False

        db.commit()
        db.refresh(report)

        return {
            "message": "Report deleted successfully"
        }