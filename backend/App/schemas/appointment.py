from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    status: Optional[str] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class AppointmentResponse(BaseModel):
    id: int
    appointment_id: str
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    status: str
    reason: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True