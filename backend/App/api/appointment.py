from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.user import User
from App.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from App.services.appointment_service import AppointmentService

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"],
)


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AppointmentService.create_appointment(
        db=db,
        appointment=appointment,
        created_by=current_user.id,
    )


@router.get("/", response_model=list[AppointmentResponse])
def get_all_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return AppointmentService.get_all_appointments(db)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = AppointmentService.get_appointment_by_id(
        db,
        appointment_id,
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_appointment = AppointmentService.get_appointment_by_id(
        db,
        appointment_id,
    )

    if not db_appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    return AppointmentService.update_appointment(
        db,
        db_appointment,
        appointment,
    )


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_appointment = AppointmentService.get_appointment_by_id(
        db,
        appointment_id,
    )

    if not db_appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found",
        )

    AppointmentService.delete_appointment(
        db,
        db_appointment,
    )

    return {
        "message": "Appointment deleted successfully"
    }