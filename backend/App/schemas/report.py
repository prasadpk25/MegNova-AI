from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReportCreate(BaseModel):
    patient_id: int
    doctor_id: int
    report_name: str
    report_type: str


class ReportResponse(BaseModel):
    id: int
    report_id: str
    patient_id: int
    doctor_id: int
    report_name: str
    report_type: str
    file_name: str
    file_path: str
    uploaded_by: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True