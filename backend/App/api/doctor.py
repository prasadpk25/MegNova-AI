from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User
from App.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse,
)
from App.services.doctor_service import DoctorService

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


# ----------------------------------------------------
# Create Doctor
# ----------------------------------------------------
@router.post(
    "/",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DoctorService.create_doctor(
        db=db,
        doctor=doctor,
        created_by=current_user.id,
    )


# ----------------------------------------------------
# Get All Doctors
# ----------------------------------------------------
@router.get(
    "/",
    response_model=list[DoctorResponse],
)
def get_all_doctors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return DoctorService.get_all_doctors(db)


# ----------------------------------------------------
# Get Doctor By ID
# ----------------------------------------------------
@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doctor = DoctorService.get_doctor_by_id(
        db,
        doctor_id,
    )

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    return doctor


# ----------------------------------------------------
# Update Doctor
# ----------------------------------------------------
@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_doctor = DoctorService.get_doctor_by_id(
        db,
        doctor_id,
    )

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    return DoctorService.update_doctor(
        db,
        db_doctor,
        doctor,
    )


# ----------------------------------------------------
# Delete Doctor
# ----------------------------------------------------
@router.delete(
    "/{doctor_id}",
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_doctor = DoctorService.get_doctor_by_id(
        db,
        doctor_id,
    )

    if not db_doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found",
        )

    DoctorService.delete_doctor(
        db,
        db_doctor,
    )

    return {
        "message": "Doctor deleted successfully"
    }