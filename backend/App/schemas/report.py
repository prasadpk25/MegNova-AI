from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)
    report_name: str = Field(..., min_length=2, max_length=255)
    report_type: Literal[
        "Blood Test",
        "X-Ray",
        "MRI",
        "CT Scan",
        "ECG",
        "Prescription",
        "Discharge Summary",
        "Other",
    ]


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