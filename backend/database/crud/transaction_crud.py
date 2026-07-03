"""
CRUD Operations for Transactions
"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import Transaction

def create_transaction(
    db: Session,
    transaction: Transaction
) -> Transaction:
    """
    Insert a single transaction.
    """

    db.add(transaction)

    db.commit()

    db.refresh(transaction)

    return transaction


def bulk_create_transactions(
    db: Session,
    transactions: List[Transaction]
):
    """
    Insert multiple transactions.
    """

    db.bulk_save_objects(transactions)

    db.commit()


def get_all_transactions(
    db: Session
):
    """
    Return all transactions.
    """

    return (
        db.query(Transaction)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

def get_transaction_by_id(
    db: Session,
    transaction_id: int
) -> Optional[Transaction]:

    return (
        db.query(Transaction)
        .filter(
            Transaction.transaction_id == transaction_id
        )
        .first()
    )

def update_transaction(
    db: Session,
    transaction_id: int,
    **kwargs
):
    """
    Update transaction fields.
    """

    transaction = get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:

        return None

    for key, value in kwargs.items():

        if hasattr(transaction, key):

            setattr(transaction, key, value)

    db.commit()

    db.refresh(transaction)

    return transaction


def delete_transaction(
    db: Session,
    transaction_id: int
):

    transaction = get_transaction_by_id(
        db,
        transaction_id
    )

    if transaction is None:

        return False

    db.delete(transaction)

    db.commit()

    return True


def get_total_income(
    db: Session
):

    return (

        db.query(

            func.coalesce(

                func.sum(Transaction.amount),

                0

            )

        )

        .filter(

            Transaction.transaction_type == "Credit"

        )

        .scalar()

    )

def get_total_expense(
    db: Session
):

    return (

        db.query(

            func.coalesce(

                func.sum(Transaction.amount),

                0

            )

        )

        .filter(

            Transaction.transaction_type == "Debit"

        )

        .scalar()

    )

def get_category_summary(
    db: Session
):

    return (

        db.query(

            Transaction.category,

            func.sum(Transaction.amount).label("total")

        )

        .filter(

            Transaction.transaction_type == "Debit"

        )

        .group_by(Transaction.category)

        .order_by(

            func.sum(Transaction.amount).desc()

        )

        .all()

    )

def get_merchant_summary(
    db: Session
):

    return (

        db.query(

            Transaction.merchant,

            func.sum(Transaction.amount).label("total")

        )

        .filter(

            Transaction.transaction_type == "Debit"

        )

        .group_by(Transaction.merchant)

        .order_by(

            func.sum(Transaction.amount).desc()

        )

        .all()

    )

def get_monthly_summary(
    db: Session
):

    return (

        db.query(

            Transaction.transaction_month,

            Transaction.month_number,

            func.sum(Transaction.amount).label("total")

        )

        .filter(

            Transaction.transaction_type == "Debit"

        )

        .group_by(

            Transaction.transaction_month,

            Transaction.month_number

        )

        .order_by(

            Transaction.month_number.asc()

        )

        .all()

    )

def get_transactions_by_category(
    db: Session,
    category: str
):

    return (

        db.query(Transaction)

        .filter(

            Transaction.category == category

        )

        .all()

    )

def get_transactions_by_merchant(
    db: Session,
    merchant: str
):

    return (

        db.query(Transaction)

        .filter(

            Transaction.merchant == merchant

        )

        .all()

    )

def get_recent_transactions(
    db: Session,
    limit: int = 10
):

    return (

        db.query(Transaction)

        .order_by(

            Transaction.transaction_date.desc()

        )

        .limit(limit)

        .all()

    )

def get_transaction_count(
    db: Session
):

    return (

        db.query(

            func.count(Transaction.transaction_id)

        )

        .scalar()

    )

