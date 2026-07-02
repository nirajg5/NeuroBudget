from datetime import date
from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):

    transaction_date: date

    merchant: str

    description: str | None = None

    amount: float

    transaction_type: str

    category: str

    payment_method: str

    account_type: str

    city: str

    balance_after_transaction: float


class TransactionCreate(TransactionBase):

    pass


class TransactionResponse(TransactionBase):

    transaction_id: int

    model_config = ConfigDict(from_attributes=True)