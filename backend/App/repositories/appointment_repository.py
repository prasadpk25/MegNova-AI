from sqlalchemy.orm import Session

from App.models.appointment import Appointment
from App.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentRepository:

    @staticmethod
    def create_appointment(
        db: Session,
        appointment: AppointmentCreate,
        created_by: int,
    ):
        appointment_count = db.query(Appointment).count() + 1
        appointment_id = f"AP{appointment_count:06d}"

        new_appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time,
            reason=appointment.reason,
            notes=appointment.notes,
            created_by=created_by,
        )

        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)

        return new_appointment

    @staticmethod
    def get_all_appointments(db: Session):
        return (
            db.query(Appointment)
            .filter(Appointment.is_active == True)
            .all()
        )

    @staticmethod
    def get_appointment_by_id(
        db: Session,
        appointment_id: int,
    ):
        return (
            db.query(Appointment)
            .filter(
                Appointment.id == appointment_id,
                Appointment.is_active == True,
            )
            .first()
        )

    @staticmethod
    def update_appointment(
        db: Session,
        db_appointment: Appointment,
        appointment: AppointmentUpdate,
    ):
        update_data = appointment.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_appointment, key, value)

        db.commit()
        db.refresh(db_appointment)

        return db_appointment

    @staticmethod
    def delete_appointment(
        db: Session,
        db_appointment: Appointment,
    ):
        db_appointment.is_active = False
        db.commit()
        db.refresh(db_appointment)

        return db_appointment