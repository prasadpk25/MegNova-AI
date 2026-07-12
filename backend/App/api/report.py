from pathlib import Path
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

UPLOAD_DIR = "App/static/uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


@router.post("/upload")
def upload_report(
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    report_name: str = Form(...),
    report_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    allowed = [".pdf", ".png", ".jpg", ".jpeg", ".docx"]

    extension = Path(file.filename).suffix.lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type",
        )

    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    report = ReportCreate(
        patient_id=patient_id,
        doctor_id=doctor_id,
        report_name=report_name,
        report_type=report_type,
    )

    return ReportService.create_report(
        db=db,
        report=report,
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id,
    )