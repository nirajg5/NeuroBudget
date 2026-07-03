"""
Transaction APIs
"""

from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Transaction

from schemas.transaction import TransactionResponse

from database.crud.transaction_crud import (
    get_transaction_by_id,
    get_transactions_by_category,
    get_transactions_by_merchant,
    get_recent_transactions,
    get_transaction_count,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# ==========================================================
# Get All Transactions (Paginated)
# ==========================================================

@router.get(
    "",
    response_model=List[TransactionResponse]
)
def read_transactions(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Returns transactions using pagination.

    Example:
        /transactions
        /transactions?limit=20
        /transactions?skip=20&limit=20
    """

    return (
        db.query(Transaction)
        .order_by(Transaction.transaction_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# ==========================================================
# Get Transactions By Category
# ==========================================================

@router.get(
    "/category/{category}",
    response_model=List[TransactionResponse]
)
def transactions_category(
    category: str,
    db: Session = Depends(get_db)
):

    return get_transactions_by_category(
        db,
        category
    )


# ==========================================================
# Get Transactions By Merchant
# ==========================================================

@router.get(
    "/merchant/{merchant}",
    response_model=List[TransactionResponse]
)
def transactions_merchant(
    merchant: str,
    db: Session = Depends(get_db)
):

    return get_transactions_by_merchant(
        db,
        merchant
    )


# ==========================================================
# Recent Transactions
# ==========================================================

@router.get(
    "/recent",
    response_model=List[TransactionResponse]
)
def recent_transactions_api(
    limit: int = 10,
    db: Session = Depends(get_db)
):

    return get_recent_transactions(
        db,
        limit
    )


# ==========================================================
# Transaction Count
# ==========================================================

@router.get("/count")
def transaction_count(
    db: Session = Depends(get_db)
):

    return {
        "count": get_transaction_count(db)
    }


# ==========================================================
# Get Transaction By ID
# Keep this route LAST
# ==========================================================

@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse
)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    transaction = get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction