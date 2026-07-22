from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from App.database.database import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
    )

    report_name = Column(
        String(255),
        nullable=False,
    )

    report_type = Column(
        String(50),
        nullable=False,
    )

    file_name = Column(
        String(255),
        nullable=False,
    )

    extracted_text = Column(
        Text,
        nullable=True,
    )

    summary = Column(
        Text,
        nullable=True,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    uploaded_by = Column(
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

    patient = relationship(
        "Patient",
        back_populates="reports",
    )

    doctor = relationship(
        "Doctor",
        back_populates="reports",
    )