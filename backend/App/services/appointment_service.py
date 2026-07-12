from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException

from App.repositories.appointment_repository import AppointmentRepository
from App.schemas.appointment import AppointmentCreate, AppointmentUpdate
from App.models.patient import Patient
from App.models.doctor import Doctor


class AppointmentService:

    @staticmethod
    def create_appointment(
        db: Session,
        appointment: AppointmentCreate,
        created_by: int,
    ):
        # Check if patient exists
        patient = (
            db.query(Patient)
            .filter(
                Patient.id == appointment.patient_id,
                Patient.is_active == True,
            )
            .first()
        )

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            )

        # Check if doctor exists
        doctor = (
            db.query(Doctor)
            .filter(
                Doctor.id == appointment.doctor_id,
                Doctor.is_active == True,
            )
            .first()
        )

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found",
            )

        # Appointment date cannot be in the past
        if appointment.appointment_date < date.today():
            raise HTTPException(
                status_code=400,
                detail="Appointment date cannot be in the past",
            )

        return AppointmentRepository.create_appointment(
            db=db,
            appointment=appointment,
            created_by=created_by,
        )

    @staticmethod
    def get_all_appointments(db: Session):
        return AppointmentRepository.get_all_appointments(db)

    @staticmethod
    def get_appointment_by_id(
        db: Session,
        appointment_id: int,
    ):
        return AppointmentRepository.get_appointment_by_id(
            db,
            appointment_id,
        )

    @staticmethod
    def update_appointment(
        db: Session,
        db_appointment,
        appointment: AppointmentUpdate,
    ):
        return AppointmentRepository.update_appointment(
            db,
            db_appointment,
            appointment,
        )

    @staticmethod
    def delete_appointment(
        db: Session,
        db_appointment,
    ):
        return AppointmentRepository.delete_appointment(
            db,
            db_appointment,
        )