from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.sql import func

from App.database.database import Base

from sqlalchemy.orm import relationship


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = Column(
        String(100),
        nullable=False,
    )

    gender = Column(
        String(20),
        nullable=False,
    )

    date_of_birth = Column(
        Date,
        nullable=False,
    )

    blood_group = Column(
        String(10),
        nullable=False,
    )

    phone = Column(
        String(20),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    address = Column(
        Text,
        nullable=False,
    )

    emergency_contact = Column(
        String(20),
        nullable=False,
    )

    allergies = Column(
        Text,
        nullable=True,
    )

    medical_history = Column(
        Text,
        nullable=True,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    appointments = relationship(
        "Appointment",
         back_populates="patient",
    )
    reports = relationship(
    "Report",
    back_populates="patient",
)