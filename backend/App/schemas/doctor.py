from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class DoctorCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    department: str
    specialization: str
    qualification: str
    experience_years: int
    license_number: str
    availability: str


class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    license_number: Optional[str] = None
    availability: Optional[str] = None
    is_active: Optional[bool] = None


class DoctorResponse(BaseModel):
    id: int
    doctor_id: str
    full_name: str
    email: EmailStr
    phone: str
    department: str
    specialization: str
    qualification: str
    experience_years: int
    license_number: str
    availability: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True