from sqlalchemy.orm import Session

from App.models.patient import Patient
from App.schemas.patient import PatientCreate, PatientUpdate


class PatientRepository:

    @staticmethod
    def create_patient(
        db: Session,
        patient: PatientCreate,
        created_by: int,
    ) -> Patient:

        patient_count = db.query(Patient).count() + 1
        generated_patient_id = f"MN{patient_count:06d}"

        new_patient = Patient(
            patient_id=generated_patient_id,
            full_name=patient.full_name,
            gender=patient.gender,
            date_of_birth=patient.date_of_birth,
            blood_group=patient.blood_group,
            phone=patient.phone,
            email=patient.email,
            address=patient.address,
            emergency_contact=patient.emergency_contact,
            allergies=patient.allergies,
            medical_history=patient.medical_history,
            created_by=created_by,
        )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        return new_patient

    @staticmethod
    def get_all_patients(
        db: Session,
    ) -> list[Patient]:

        return (
            db.query(Patient)
            .filter(Patient.is_active.is_(True))
            .all()
        )

    @staticmethod
    def get_patient_by_id(
        db: Session,
        patient_id: str,
    ) -> Patient | None:

        print(f"Patient ID = {patient_id}")

        return (
            db.query(Patient)
            .filter(
                Patient.patient_id == patient_id,
                Patient.is_active.is_(True),
            )
            .first()
        )

    @staticmethod
    def update_patient(
        db: Session,
        db_patient: Patient,
        patient: PatientUpdate,
    ) -> Patient:

        update_data = patient.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_patient, key, value)

        db.commit()
        db.refresh(db_patient)

        return db_patient

    @staticmethod
    def delete_patient(
        db: Session,
        db_patient: Patient,
    ) -> Patient:

        db_patient.is_active = False

        db.commit()
        db.refresh(db_patient)

        return db_patient