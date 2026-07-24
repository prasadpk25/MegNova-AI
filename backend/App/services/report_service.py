from sqlalchemy.orm import Session

from App.repositories.report_repository import ReportRepository

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
        report,
        file_name,
        file_path,
        uploaded_by,
    ):
        extracted_text = ""
        summary = ""
        embedding = None

        try:
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):

                # OCR
                extracted_text = extract_text(file_path)

                if extracted_text.strip():

                    # AI Summary
                    summary = summarize_report(extracted_text)

                    # Generate Embedding
                    embedding = generate_embedding(extracted_text)

        except Exception as e:
            print(f"AI Error: {e}")

        # Save in PostgreSQL
        saved_report = ReportRepository.create_report(
            db=db,
            report=report,
            file_name=file_name,
            file_path=file_path,
            uploaded_by=uploaded_by,
            extracted_text=extracted_text,
            summary=summary,
        )

        # Save embedding in Qdrant
        if embedding is not None:
            print("Embedding generated successfully")

            create_collection()

            print("Storing embedding in Qdrant...")

            store_embedding(
                report_id=saved_report.id,
                embedding=embedding,
                metadata={
                    "patient_id": report.patient_id,
                    "doctor_id": report.doctor_id,
                    "report_name": report.report_name,
                    "summary": summary,
                },
            )

        print("Embedding stored successfully!")

        return saved_report

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

    @staticmethod
    def delete_report(
        db: Session,
        report_id: int,
    ):
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
    ):
        report = ReportRepository.get_report_by_id(
            db,
            report_id,
        )

        if not report:
            return None

        if not report.extracted_text:
            return {
                "summary": "No extracted text available."
            }

        summary = summarize_report(
            report.extracted_text
        )

        report.summary = summary

        db.commit()
        db.refresh(report)

        return {
            "summary": summary
        }