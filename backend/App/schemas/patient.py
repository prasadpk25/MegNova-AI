from datetime import date, datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr, Field


class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    gender: Literal["Male", "Female", "Other"]
    date_of_birth: date
    blood_group: str
    phone: str = Field(..., min_length=10, max_length=20)
    email: EmailStr
    address: str = Field(..., min_length=5)
    emergency_contact: str = Field(..., min_length=10, max_length=20)
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = Field(None, min_length=10, max_length=20)
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