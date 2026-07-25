from sqlalchemy.orm import Session

from App.models.report import Report
from App.repositories.report_repository import ReportRepository
from App.schemas.report import ReportCreate

from App.ai.ocr import extract_text
from App.ai.summarizer import summarize_report
from App.ai.embeddings import generate_embedding
from App.ai.vector_store import (
    create_collection,
    store_embedding,
)


class ReportService:

    @staticmethod
    def create_report(
        db: Session,
        report: ReportCreate,
        file_name: str,
        file_path: str,
        uploaded_by: int,
    ) -> Report:
        """
        Fast upload.
        Save report details only.
        OCR, AI Summary and Embedding are generated later.
        """

        return ReportRepository.create_report(
            db=db,
            report=report,
            file_name=file_name,
            file_path=file_path,
            uploaded_by=uploaded_by,
            extracted_text="",
            summary="",
        )

    @staticmethod
    def get_all_reports(
        db: Session,
    ) -> list[Report]:
        return ReportRepository.get_all_reports(db)

    @staticmethod
    def get_report_by_id(
        db: Session,
        report_id: int,
    ) -> Report | None:
        return ReportRepository.get_report_by_id(
            db,
            report_id,
        )

    @staticmethod
    def delete_report(
        db: Session,
        report_id: int,
    ) -> Report | None:
        report = ReportRepository.get_report_by_id(
            db,
            report_id,
        )

        if not report:
            return None

        return ReportRepository.delete_report(
            db,
            report,
        )

    @staticmethod
    def summarize_existing_report(
        db: Session,
        report_id: int,
    ) -> dict | None:
        """
        Generate OCR, AI Summary and Vector Embedding.
        """

        report = ReportRepository.get_report_by_id(
            db,
            report_id,
        )

        if not report:
            return None

        try:

            # OCR
            if (
                not report.extracted_text
                and report.file_path.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".pdf")
                )
            ):
                report.extracted_text = extract_text(
                    report.file_path
                )

            if not report.extracted_text.strip():
                return {
                    "summary": "No readable text found in the report."
                }

            # AI Summary
            report.summary = summarize_report(
                report.extracted_text
            )

            # Embedding
            embedding = generate_embedding(
                report.extracted_text
            )

            if embedding:
                create_collection()

                store_embedding(
                    report_id=report.id,
                    embedding=embedding,
                    metadata={
                        "patient_id": report.patient_id,
                        "patient_name": report.patient.full_name,
                        "doctor_id": report.doctor_id,
                        "doctor_name": report.doctor.full_name,
                        "report_name": report.report_name,
                        "report_type": report.report_type,
                        "summary": report.summary,
                    },
                )

            db.commit()
            db.refresh(report)

            return {
                "summary": report.summary
            }

        except Exception as e:
            db.rollback()

            return {
                "summary": f"Error generating summary: {str(e)}"
            }