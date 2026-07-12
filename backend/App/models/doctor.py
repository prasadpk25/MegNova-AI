from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func

from App.database.database import Base

from sqlalchemy.orm import relationship


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone = Column(
        String(20),
        nullable=False,
    )

    department = Column(
        String(100),
        nullable=False,
    )

    specialization = Column(
        String(100),
        nullable=False,
    )

    qualification = Column(
        String(100),
        nullable=False,
    )

    experience_years = Column(
        Integer,
        nullable=False,
    )

    license_number = Column(
        String(100),
        unique=True,
        nullable=False,
    )

    availability = Column(
        String(255),
        nullable=False,
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
         back_populates="doctor",
    )
    reports = relationship(
    "Report",
    back_populates="doctor",
)