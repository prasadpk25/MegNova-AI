
from sqlalchemy import (
    Boolean, Column, Date, DateTime, Float,
    ForeignKey, Integer, String, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from App.database.database import Base


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    recorded_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    kind = Column(String(30), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    recorded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    patient = relationship("Patient", back_populates="observations")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer, ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    chunk_index = Column(Integer, nullable=False)
    page = Column(Integer, nullable=False, default=1)
    text = Column(Text, nullable=False)
    qdrant_point_id = Column(String(64), nullable=True, unique=True)


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    event_type = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )

    patient = relationship("Patient", back_populates="timeline_events")


class Bed(Base):
    __tablename__ = "beds"
    __table_args__ = (
        UniqueConstraint("ward", "bed_number",
                         name="uq_beds_ward_bed_number"),
    )

    id = Column(Integer, primary_key=True, index=True)
    ward = Column(String(50), nullable=False, index=True)
    bed_number = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="available")
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True, index=True
    )


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String(120), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=20)
    expiry_date = Column(Date, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(
        Integer, ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    kind = Column(String(20), nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(String(300), nullable=False)
    acknowledged = Column(Boolean, nullable=False, default=False)
    acknowledged_by = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    action = Column(String(50), nullable=False, index=True)
    resource = Column(String(200), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )


class DrugInteraction(Base):
    __tablename__ = "drug_interactions"
    __table_args__ = (
        UniqueConstraint("drug_a", "drug_b",
                         name="uq_drug_interactions_pair"),
    )

    id = Column(Integer, primary_key=True, index=True)
    drug_a = Column(String(80), nullable=False)
    drug_b = Column(String(80), nullable=False)
    severity = Column(String(20), nullable=False)
    note = Column(String(300), nullable=False)
