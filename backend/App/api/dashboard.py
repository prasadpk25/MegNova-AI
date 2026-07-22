from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User

from App.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/dashboard",
    tags=["Doctor Dashboard"],
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_data(db)