from pydantic import BaseModel, ConfigDict


class ReportBase(BaseModel):

    report_type: str

    report_json: str

    pdf_path: str


class ReportCreate(ReportBase):

    pass


class ReportResponse(ReportBase):

    report_id: int

    model_config = ConfigDict(from_attributes=True)