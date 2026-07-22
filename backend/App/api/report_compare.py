from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User
from App.services.report_compare_service import compare_latest_reports

router = APIRouter(
    prefix="/report-compare",
    tags=["AI Report Comparison"],
)


@router.get("/{patient_id}")
def compare_reports(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "comparison": compare_latest_reports(
            db=db,
            patient_id=patient_id,
        )
    }