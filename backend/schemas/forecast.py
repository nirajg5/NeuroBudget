"""
Forecast Schemas
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class ForecastBase(BaseModel):

    prediction_date: date

    predicted_expense: float

    model_name: str

    confidence_score: float


class ForecastCreate(ForecastBase):
    pass


class ForecastUpdate(BaseModel):

    prediction_date: Optional[date] = None

    predicted_expense: Optional[float] = None

    model_name: Optional[str] = None

    confidence_score: Optional[float] = None


class ForecastResponse(ForecastBase):

    forecast_id: int

    class Config:
        from_attributes = True