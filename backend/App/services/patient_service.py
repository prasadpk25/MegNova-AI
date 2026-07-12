from sqlalchemy.orm import Session

from App.repositories.patient_repository import PatientRepository
from App.schemas.patient import PatientCreate, PatientUpdate


class PatientService:

    @staticmethod
    def create_patient(
        db: Session,
        patient: PatientCreate,
        created_by: int,
    ):
        return PatientRepository.create_patient(
            db=db,
            patient=patient,
            created_by=created_by,
        )

    @staticmethod
    def get_all_patients(db: Session):
        return PatientRepository.get_all_patients(db)

    @staticmethod
    def get_patient_by_id(
        db: Session,
        patient_id: int,
    ):
        return PatientRepository.get_patient_by_id(
            db,
            patient_id,
        )

    @staticmethod
    def update_patient(
        db: Session,
        db_patient,
        patient: PatientUpdate,
    ):
        return PatientRepository.update_patient(
            db,
            db_patient,
            patient,
        )

    @staticmethod
    def delete_patient(
        db: Session,
        db_patient,
    ):
        PatientRepository.delete_patient(
            db,
            db_patient,
        )