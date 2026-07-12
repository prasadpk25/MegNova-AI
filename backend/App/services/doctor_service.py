from sqlalchemy.orm import Session

from App.repositories.doctor_repository import DoctorRepository
from App.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorService:

    @staticmethod
    def create_doctor(
        db: Session,
        doctor: DoctorCreate,
        created_by: int,
    ):
        return DoctorRepository.create_doctor(
            db=db,
            doctor=doctor,
            created_by=created_by,
        )

    @staticmethod
    def get_all_doctors(db: Session):
        return DoctorRepository.get_all_doctors(db)

    @staticmethod
    def get_doctor_by_id(
        db: Session,
        doctor_id: int,
    ):
        return DoctorRepository.get_doctor_by_id(
            db,
            doctor_id,
        )

    @staticmethod
    def update_doctor(
        db: Session,
        db_doctor,
        doctor: DoctorUpdate,
    ):
        return DoctorRepository.update_doctor(
            db,
            db_doctor,
            doctor,
        )

    @staticmethod
    def delete_doctor(
        db: Session,
        db_doctor,
    ):
        return DoctorRepository.delete_doctor(
            db,
            db_doctor,
        )