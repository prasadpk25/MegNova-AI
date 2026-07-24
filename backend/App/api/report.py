from pathlib import Path
from uuid import uuid4
import shutil

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from sqlalchemy.orm import Session

from App.database.database import get_db
from App.services.report_service import ReportService
from App.schemas.report import ReportCreate
from App.auth.dependencies import get_current_user
from App.models.user import User

router = APIRouter(
    prefix="/reports",
    tags=["Medical Reports"],
)

UPLOAD_DIR = Path("App/static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ======================================================
# Upload Report
# ======================================================
@router.post("/upload", status_code=201)
def upload_report(
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    report_name: str = Form(...),
    report_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    allowed_extensions = {
        ".pdf",
        ".png",
        ".jpg",
        ".jpeg",
        ".docx",
    }

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type.",
        )

    unique_filename = f"{uuid4().hex}{extension}"

    file_path = UPLOAD_DIR / unique_filename

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        report = ReportCreate(
            patient_id=patient_id,
            doctor_id=doctor_id,
            report_name=report_name,
            report_type=report_type,
        )

        created_report = ReportService.create_report(
            db=db,
            report=report,
            file_name=file.filename,
            file_path=str(file_path),
            uploaded_by=current_user.id,
        )

        return {
            "message": "Report uploaded successfully.",
            "report": created_report,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ======================================================
# Get All Reports
# ======================================================
@router.get("/")
def get_all_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ReportService.get_all_reports(db)


# ======================================================
# Get Report By ID
# ======================================================
@router.get("/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    report = ReportService.get_report_by_id(
        db,
        report_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return report


# ======================================================
# Generate AI Summary
# ======================================================
@router.post("/summarize/{report_id}")
def summarize_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    report = ReportService.summarize_existing_report(
        db,
        report_id,
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return {
        "message": "Summary generated successfully.",
        "summary": report.summary,
    }


# ======================================================
# Delete Report
# ======================================================
@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    deleted = ReportService.delete_report(
        db,
        report_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    return {
        "message": "Report deleted successfully."
    }