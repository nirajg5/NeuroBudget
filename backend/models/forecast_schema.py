from datetime import date
from pydantic import BaseModel, ConfigDict


class ForecastBase(BaseModel):

    prediction_date: date

    predicted_expense: float

    model_name: str

    confidence_score: float


class ForecastCreate(ForecastBase):

    pass


class ForecastResponse(ForecastBase):

    forecast_id: int

    model_config = ConfigDict(from_attributes=True)

