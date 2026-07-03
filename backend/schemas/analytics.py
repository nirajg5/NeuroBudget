"""
Analytics Schemas
"""

from typing import List

from pydantic import BaseModel


class AnalyticsItem(BaseModel):

    name: str

    total: float


class AnalyticsResponse(BaseModel):

    category_summary: List[AnalyticsItem]

    merchant_summary: List[AnalyticsItem]

    monthly_summary: List[AnalyticsItem]

    total_income: float

    total_expense: float

    balance: float