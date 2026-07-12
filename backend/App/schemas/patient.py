from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


class PatientCreate(BaseModel):
    full_name: str
    gender: str
    date_of_birth: date
    blood_group: str
    phone: str
    email: EmailStr
    address: str
    emergency_contact: str
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    is_active: Optional[bool] = None


class PatientResponse(BaseModel):
    id: int
    patient_id: str
    full_name: str
    gender: str
    date_of_birth: date
    blood_group: str
    phone: str
    email: EmailStr
    address: str
    emergency_contact: str
    allergies: Optional[str]
    medical_history: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True