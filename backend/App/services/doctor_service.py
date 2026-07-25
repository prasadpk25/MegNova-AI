from sqlalchemy.orm import Session

from App.models.doctor import Doctor
from App.repositories.doctor_repository import DoctorRepository
from App.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:

    @staticmethod
    def create_doctor(
        db: Session,
        doctor: DoctorCreate,
        created_by: int,
    ) -> Doctor:
        return DoctorRepository.create_doctor(
            db=db,
            doctor=doctor,
            created_by=created_by,
        )

    @staticmethod
    def get_all_doctors(
        db: Session,
    ) -> list[Doctor]:
        return DoctorRepository.get_all_doctors(db)

    @staticmethod
    def get_doctor_by_id(
        db: Session,
        doctor_id: int,
    ) -> Doctor | None:
        return DoctorRepository.get_doctor_by_id(
            db,
            doctor_id,
        )

    @staticmethod
    def update_doctor(
        db: Session,
        db_doctor: Doctor,
        doctor: DoctorUpdate,
    ) -> Doctor:
        return DoctorRepository.update_doctor(
            db,
            db_doctor,
            doctor,
        )

    @staticmethod
    def delete_doctor(
        db: Session,
        db_doctor: Doctor,
    ) -> Doctor:
        return DoctorRepository.delete_doctor(
            db,
            db_doctor,
        )