"""
Transaction Schemas
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel


class TransactionResponse(BaseModel):

    transaction_id: int

    transaction_date: date

    merchant: str

    description: Optional[str] = None

    amount: float

    transaction_type: str

    category: str

    payment_method: str

    account_type: str

    city: str

    balance_after_transaction: float

    transaction_month: Optional[str] = None

    month_number: Optional[int] = None

    day: Optional[int] = None

    weekday: Optional[str] = None

    quarter: Optional[int] = None

    year: Optional[int] = None

    is_weekend: Optional[bool] = None

    flow: Optional[str] = None

    transaction_size: Optional[str] = None

    class Config:
        from_attributes = True