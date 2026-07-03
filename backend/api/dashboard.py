"""
Dashboard API
"""

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.db import get_db

from database.crud.transaction_crud import (
    get_total_income,
    get_total_expense,
    get_transaction_count,
    get_category_summary,
    get_merchant_summary,
    get_monthly_summary,
    get_recent_transactions,
)

from database.crud.goal_crud import (
    get_active_goals,
    get_completed_goals,
)

from database.crud.forecast_crud import (
    get_latest_prediction,
)

from agents.risk_agent import risk_agent

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db)
):

    income = get_total_income(db)

    expense = get_total_expense(db)

    forecast = get_latest_prediction(db)

    category = get_category_summary(db)

    merchant = get_merchant_summary(db)

    monthly = get_monthly_summary(db)

    recent = get_recent_transactions(db, limit=10)

    return {

        "total_transactions": get_transaction_count(db),

        "total_income": income,

        "total_expense": expense,

        "balance": income - expense,

        "risk_score": risk_agent.calculate_risk_score(),

        "active_goals": len(get_active_goals(db)),

        "completed_goals": len(get_completed_goals(db)),

        "forecast": forecast,

        "monthly_expense": [

            {

                "name": m.transaction_month,

                "total": float(m.total)

            }

            for m in monthly

        ],

        "category_summary": [

            {

                "name": c.category,

                "total": float(c.total)

            }

            for c in category

        ],

        "merchant_summary": [

            {

                "name": m.merchant,

                "total": float(m.total)

            }

            for m in merchant

        ],

        "recent_transactions": recent

    }