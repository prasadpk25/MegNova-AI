from sqlalchemy.orm import Session

from App.repositories.report_repository import ReportRepository
from App.ai.ocr import extract_text


class ReportService:

    @staticmethod
    def create_report(
        db: Session,
        report,
        file_name,
        file_path,
        uploaded_by,
    ):
        extracted_text = ""

        try:
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                extracted_text = extract_text(file_path)
        except Exception as e:
            print(f"OCR Error: {e}")

        return ReportRepository.create_report(
            db=db,
            report=report,
            file_name=file_name,
            file_path=file_path,
            uploaded_by=uploaded_by,
            extracted_text=extracted_text,
        )

    @staticmethod
    def get_all_reports(db: Session):
        return ReportRepository.get_all_reports(db)

    @staticmethod
    def get_report_by_id(
        db: Session,
        report_id: int,
    ):
        return ReportRepository.get_report_by_id(
            db,
            report_id,
        )