from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User

from App.schemas.drug_interaction import DrugInteractionRequest
from App.services.drug_interaction_service import check_drug_interactions

router = APIRouter(
    prefix="/drug-interaction",
    tags=["AI Drug Interaction"],
)


@router.post("/")
def drug_interaction(
    request: DrugInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "result": check_drug_interactions(request.drugs)
    }