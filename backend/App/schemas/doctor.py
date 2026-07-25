from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class DoctorCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=20)
    department: str = Field(..., min_length=2, max_length=100)
    specialization: str = Field(..., min_length=2, max_length=100)
    qualification: str = Field(..., min_length=2, max_length=100)
    experience_years: int = Field(..., ge=0)
    license_number: str = Field(..., min_length=3, max_length=100)
    availability: str = Field(..., min_length=2, max_length=255)


class DoctorUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=20)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    specialization: Optional[str] = Field(None, min_length=2, max_length=100)
    qualification: Optional[str] = Field(None, min_length=2, max_length=100)
    experience_years: Optional[int] = Field(None, ge=0)
    license_number: Optional[str] = Field(None, min_length=3, max_length=100)
    availability: Optional[str] = Field(None, min_length=2, max_length=255)
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