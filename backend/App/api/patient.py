from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.auth.dependencies import get_current_user
from App.database.database import get_db
from App.models.patient import Patient
from App.models.user import User
from App.schemas.patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
)
from App.services.patient_service import PatientService

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PatientService.create_patient(
        db=db,
        patient=patient,
        created_by=current_user.id,
    )


@router.get("/", response_model=list[PatientResponse])
def get_all_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PatientService.get_all_patients(db)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    patient = PatientService.get_patient_by_id(
        db,
        patient_id,
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_patient = PatientService.get_patient_by_id(
        db,
        patient_id,
    )

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return PatientService.update_patient(
        db,
        db_patient,
        patient,
    )


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_patient = PatientService.get_patient_by_id(
        db,
        patient_id,
    )

    if not db_patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    PatientService.delete_patient(
        db,
        db_patient,
    )

    return {
        "message": "Patient deleted successfully"
    }