"""
Database CRUD Operations
"""

from sqlalchemy.orm import Session

from database.models import Transaction


def insert_transactions(

    db: Session,

    transactions: list

):

    db.bulk_save_objects(transactions)

    db.commit()


def get_all_transactions(

    db: Session

):

    return db.query(Transaction).all()


def total_income(

    db: Session

):

    return (

        db.query(Transaction)

        .filter(

            Transaction.transaction_type == "Credit"

        )

        .all()

    )


def total_expense(

    db: Session

):

    return (

        db.query(Transaction)

        .filter(

            Transaction.transaction_type == "Debit"

        )

        .all()

    )


def get_transaction(

    db: Session,

    transaction_id: int

):

    return (

        db.query(Transaction)

        .filter(

            Transaction.transaction_id == transaction_id

        )

        .first()

    )