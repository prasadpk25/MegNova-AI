from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User
from App.services.patient_history_service import ask_patient_history

router = APIRouter(
    prefix="/patient-history",
    tags=["Patient History AI"],
)


@router.post("/{patient_id}")
def patient_history_ai(
    patient_id: int,
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "answer": ask_patient_history(
            db=db,
            patient_id=patient_id,
            question=question,
        )
    }