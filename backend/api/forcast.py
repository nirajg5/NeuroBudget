"""
Forecast APIs
"""

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Forecast

from schemas.forecast import (
    ForecastCreate,
    ForecastUpdate,
    ForecastResponse
)

from database.crud.forecast_crud import (
    create_forecast,
    get_all_forecasts,
    get_latest_forecast,
    get_best_forecast,
    get_forecast_by_id,
    update_forecast,
    delete_forecast,
    get_forecast_count
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

# ==========================================================
# All Forecasts
# ==========================================================

@router.get(
    "",
    response_model=List[ForecastResponse]
)
def read_forecasts(
    db: Session = Depends(get_db)
):
    return get_all_forecasts(db)


# ==========================================================
# Latest Forecast
# ==========================================================

@router.get(
    "/latest",
    response_model=ForecastResponse
)
def latest_forecast(
    db: Session = Depends(get_db)
):

    forecast = get_latest_forecast(db)

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="No forecast found"
        )

    return forecast


# ==========================================================
# Best Forecast
# ==========================================================

@router.get(
    "/best",
    response_model=ForecastResponse
)
def best_forecast(
    db: Session = Depends(get_db)
):

    forecast = get_best_forecast(db)

    if forecast is None:
        raise HTTPException(
            status_code=404,
            detail="No forecast found"
        )

    return forecast


# ==========================================================
# Forecast Count
# ==========================================================

@router.get("/count")
def forecast_count(
    db: Session = Depends(get_db)
):

    return {
        "count": get_forecast_count(db)
    }


# ==========================================================
# Forecast By ID
# ==========================================================

@router.get(
    "/{forecast_id}",
    response_model=ForecastResponse
)
def read_forecast(
    forecast_id: int,
    db: Session = Depends(get_db)
):

    forecast = get_forecast_by_id(
        db,
        forecast_id
    )

    if forecast is None:

        raise HTTPException(
            status_code=404,
            detail="Forecast not found"
        )

    return forecast


# ==========================================================
# Create Forecast
# ==========================================================

@router.post(
    "",
    response_model=ForecastResponse
)
def add_forecast(
    forecast: ForecastCreate,
    db: Session = Depends(get_db)
):

    db_forecast = Forecast(
        **forecast.model_dump()
    )

    return create_forecast(
        db,
        db_forecast
    )


# ==========================================================
# Update Forecast
# ==========================================================

@router.put(
    "/{forecast_id}",
    response_model=ForecastResponse
)
def edit_forecast(
    forecast_id: int,
    forecast: ForecastUpdate,
    db: Session = Depends(get_db)
):

    updated = update_forecast(
        db,
        forecast_id,
        **forecast.model_dump(
            exclude_unset=True
        )
    )

    if updated is None:

        raise HTTPException(
            status_code=404,
            detail="Forecast not found"
        )

    return updated


# ==========================================================
# Delete Forecast
# ==========================================================

@router.delete("/{forecast_id}")
def remove_forecast(
    forecast_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_forecast(
        db,
        forecast_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Forecast not found"
        )

    return {
        "message": "Forecast deleted successfully"
    }