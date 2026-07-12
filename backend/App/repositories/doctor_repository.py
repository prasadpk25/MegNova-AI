from sqlalchemy.orm import Session

from App.models.doctor import Doctor
from App.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorRepository:

    @staticmethod
    def create_doctor(
        db: Session,
        doctor: DoctorCreate,
        created_by: int,
    ):
        doctor_count = db.query(Doctor).count() + 1
        doctor_id = f"DR{doctor_count:06d}"

        new_doctor = Doctor(
            doctor_id=doctor_id,
            full_name=doctor.full_name,
            email=doctor.email,
            phone=doctor.phone,
            department=doctor.department,
            specialization=doctor.specialization,
            qualification=doctor.qualification,
            experience_years=doctor.experience_years,
            license_number=doctor.license_number,
            availability=doctor.availability,
            created_by=created_by,
        )

        db.add(new_doctor)
        db.commit()
        db.refresh(new_doctor)

        return new_doctor

    @staticmethod
    def get_all_doctors(db: Session):
        return (
            db.query(Doctor)
            .filter(Doctor.is_active == True)
            .all()
        )

    @staticmethod
    def get_doctor_by_id(
        db: Session,
        doctor_id: int,
    ):
        return (
            db.query(Doctor)
            .filter(
                Doctor.id == doctor_id,
                Doctor.is_active == True,
            )
            .first()
        )

    @staticmethod
    def update_doctor(
        db: Session,
        db_doctor: Doctor,
        doctor: DoctorUpdate,
    ):
        update_data = doctor.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_doctor, key, value)

        db.commit()
        db.refresh(db_doctor)

        return db_doctor

    @staticmethod
    def delete_doctor(
        db: Session,
        db_doctor: Doctor,
    ):
        db_doctor.is_active = False
        db.commit()
        db.refresh(db_doctor)

        return db_doctor