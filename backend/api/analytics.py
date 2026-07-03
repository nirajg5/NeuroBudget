"""
Analytics API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import get_db

from database.crud.transaction_crud import (
    get_category_summary,
    get_merchant_summary,
    get_monthly_summary,
    get_total_income,
    get_total_expense,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# ==========================================================
# Complete Analytics
# ==========================================================

@router.get("")
def analytics(
    db: Session = Depends(get_db)
):

    income = get_total_income(db)

    expense = get_total_expense(db)

    category = get_category_summary(db)

    merchant = get_merchant_summary(db)

    monthly = get_monthly_summary(db)

    return {

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

        "monthly_summary": [

            {

                "name": m.transaction_month,

                "total": float(m.total)

            }

            for m in monthly

        ],

        "total_income": income,

        "total_expense": expense,

        "balance": income - expense

    }


# ==========================================================
# Category Analytics
# ==========================================================

@router.get("/category")
def category_analytics(
    db: Session = Depends(get_db)
):

    return get_category_summary(db)


# ==========================================================
# Merchant Analytics
# ==========================================================

@router.get("/merchant")
def merchant_analytics(
    db: Session = Depends(get_db)
):

    return get_merchant_summary(db)


# ==========================================================
# Monthly Analytics
# ==========================================================

@router.get("/monthly")
def monthly_analytics(
    db: Session = Depends(get_db)
):

    return get_monthly_summary(db)


# ==========================================================
# Income vs Expense
# ==========================================================

@router.get("/income-expense")
def income_expense(
    db: Session = Depends(get_db)
):

    income = get_total_income(db)

    expense = get_total_expense(db)

    return {

        "income": income,

        "expense": expense,

        "balance": income - expense

    }