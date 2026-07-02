"""
CRUD Operations for Forecasts
"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Forecast

def create_forecast(
    db: Session,
    forecast: Forecast
) -> Forecast:

    db.add(forecast)

    db.commit()

    db.refresh(forecast)

    return forecast

def bulk_create_forecasts(
    db: Session,
    forecasts: List[Forecast]
):

    db.bulk_save_objects(forecasts)

    db.commit()

def get_forecast_by_id(
    db: Session,
    forecast_id: int
) -> Optional[Forecast]:

    return (
        db.query(Forecast)
        .filter(
            Forecast.forecast_id == forecast_id
        )
        .first()
    )

def get_latest_forecast(
    db: Session
) -> Optional[Forecast]:

    return (
        db.query(Forecast)
        .order_by(
            Forecast.created_at.desc()
        )
        .first()
    )

def get_all_forecasts(
    db: Session
):

    return (
        db.query(Forecast)
        .order_by(
            Forecast.created_at.desc()
        )
        .all()
    )

def get_forecasts_by_model(
    db: Session,
    model_name: str
):

    return (
        db.query(Forecast)
        .filter(
            Forecast.model_name == model_name
        )
        .all()
    )

def get_best_forecast(
    db: Session
):

    return (
        db.query(Forecast)
        .order_by(
            Forecast.confidence_score.desc()
        )
        .first()
    )
def update_forecast(
    db: Session,
    forecast_id: int,
    **kwargs
):

    forecast = get_forecast_by_id(
        db,
        forecast_id
    )

    if forecast is None:

        return None

    for key, value in kwargs.items():

        if hasattr(forecast, key):

            setattr(forecast, key, value)

    db.commit()

    db.refresh(forecast)

    return forecast

def delete_forecast(
    db: Session,
    forecast_id: int
):

    forecast = get_forecast_by_id(
        db,
        forecast_id
    )

    if forecast is None:

        return False

    db.delete(forecast)

    db.commit()

    return True


def delete_all_forecasts(
    db: Session
):

    db.query(Forecast).delete()

    db.commit()


def get_forecast_count(
    db: Session
):

    return (
        db.query(
            func.count(
                Forecast.forecast_id
            )
        )
        .scalar()
    )

def get_latest_prediction(
    db: Session
):

    forecast = get_latest_forecast(db)

    if forecast is None:

        return None

    return forecast.predicted_expense

def get_average_prediction(
    db: Session
):

    return (
        db.query(
            func.avg(
                Forecast.predicted_expense
            )
        )
        .scalar()
    )

def get_highest_prediction(
    db: Session
):

    return (
        db.query(
            func.max(
                Forecast.predicted_expense
            )
        )
        .scalar()
    )

def get_lowest_prediction(
    db: Session
):

    return (
        db.query(
            func.min(
                Forecast.predicted_expense
            )
        )
        .scalar()
    )

def get_average_confidence(
    db: Session
):

    return (
        db.query(
            func.avg(
                Forecast.confidence_score
            )
        )
        .scalar()
    )

def get_recent_forecasts(
    db: Session,
    limit: int = 10
):

    return (
        db.query(Forecast)
        .order_by(
            Forecast.created_at.desc()
        )
        .limit(limit)
        .all()
    )
