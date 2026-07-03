"""
Report Schemas
"""

from typing import Optional

from pydantic import BaseModel


class ReportBase(BaseModel):

    report_type: str

    report_json: str

    pdf_path: str


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):

    report_type: Optional[str] = None

    report_json: Optional[str] = None

    pdf_path: Optional[str] = None


class ReportResponse(ReportBase):

    report_id: int

    class Config:
        from_attributes = True