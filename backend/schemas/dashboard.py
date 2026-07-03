"""
Dashboard Schemas
"""

from typing import List

from pydantic import BaseModel


class SummaryItem(BaseModel):

    name: str

    total: float


class DashboardResponse(BaseModel):

    total_transactions: int

    total_income: float

    total_expense: float

    balance: float

    risk_score: int

    active_goals: int

    completed_goals: int

    forecast: float

    monthly_expense: List[SummaryItem]

    category_summary: List[SummaryItem]

    merchant_summary: List[SummaryItem]

    recent_transactions: list