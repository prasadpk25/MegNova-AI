
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
        Save report details during upload.
        OCR, AI summary and embedding are generated later.
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
    def get_all_reports(db: Session) -> list[Report]:
        return ReportRepository.get_all_reports(db)

    @staticmethod
    def get_report_by_id(
        db: Session,
        report_id: int,
    ) -> Report | None:
        return ReportRepository.get_report_by_id(db, report_id)

    @staticmethod
    def delete_report(
        db: Session,
        report_id: int,
    ) -> Report | None:
        report = ReportRepository.get_report_by_id(db, report_id)

        if not report:
            return None

        return ReportRepository.delete_report(db, report)

    @staticmethod
    def summarize_existing_report(
        db: Session,
        report_id: int,
    ) -> dict | None:
        """
        Extract report text and save AI summary.
        Vector indexing is performed separately so that
        an indexing failure cannot undo the saved summary.
        """

        report = ReportRepository.get_report_by_id(db, report_id)

        if not report:
            return None

        # STEP 1: OCR text extraction
        try:
            if (
                not report.extracted_text
                and report.file_path.lower().endswith(
                    (".png", ".jpg", ".jpeg", ".pdf", ".docx")
                )
            ):
                report.extracted_text = extract_text(report.file_path)

            if not (report.extracted_text or "").strip():
                return {
                    "summary": "No readable text found in the report."
                }

            # STEP 2: Generate AI summary using Groq
            report.summary = summarize_report(report.extracted_text)

            # STEP 3: Save summary and extracted text in PostgreSQL
            db.commit()
            db.refresh(report)

        except Exception as error:
            db.rollback()
            print(
                f"Report summarization error: "
                f"{type(error).__name__}: {error}"
            )
            return {
                "summary": (
                    f"Summary generation failed: {type(error).__name__}"
                )
            }

        # STEP 4: Generate and store vector embedding
        # This is optional and must not affect the saved summary.
        try:
            embedding = generate_embedding(report.extracted_text)

            if embedding:
                create_collection()

                store_embedding(
                    report_id=report.id,
                    embedding=embedding,
                    metadata={
                        "patient_id": report.patient_id,
                        "patient_name": (
                            report.patient.full_name
                            if report.patient else None
                        ),
                        "doctor_id": report.doctor_id,
                        "doctor_name": (
                            report.doctor.full_name
                            if report.doctor else None
                        ),
                        "report_name": report.report_name,
                        "report_type": report.report_type,
                        "summary": report.summary,
                    },
                )

        except Exception as error:
            print(
                f"Report embedding error: "
                f"{type(error).__name__}: {error}"
            )

        # STEP 5: Return the saved summary
        return {
            "summary": report.summary
        }
