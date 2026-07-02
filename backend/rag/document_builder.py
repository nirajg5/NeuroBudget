"""
Document Builder

Converts transactions into text documents
for embedding and semantic search.
"""

from typing import List

import pandas as pd

from database.models import Transaction

from core.logger import logger


class DocumentBuilder:

    """
    Build documents from transactions.
    """

    @staticmethod
    def build_document(
        transaction: Transaction
    ) -> str:

        document = f"""
Transaction ID: {transaction.transaction_id}

Date: {transaction.transaction_date}

Merchant: {transaction.merchant}

Description: {transaction.description}

Amount: ₹{transaction.amount}

Transaction Type: {transaction.transaction_type}

Category: {transaction.category}

Payment Method: {transaction.payment_method}

Account Type: {transaction.account_type}

City: {transaction.city}

Flow: {transaction.flow}

Transaction Size: {transaction.transaction_size}

Weekday: {transaction.weekday}

Month: {transaction.transaction_month}

Year: {transaction.year}
"""

        return document.strip()

    @staticmethod
    def build_documents(
        transactions: List[Transaction]
    ) -> List[str]:

        logger.info(
            f"Building {len(transactions)} documents..."
        )

        documents = [

            DocumentBuilder.build_document(transaction)

            for transaction in transactions

        ]

        logger.success(
            f"{len(documents)} documents created."
        )

        return documents

    @staticmethod
    def dataframe_to_documents(
        df: pd.DataFrame
    ) -> List[str]:

        logger.info(
            "Building documents from DataFrame..."
        )

        documents = []

        for _, row in df.iterrows():

            document = f"""
Transaction ID: {row['transaction_id']}

Date: {row['transaction_date']}

Merchant: {row['merchant']}

Description: {row['description']}

Amount: ₹{row['amount']}

Transaction Type: {row['transaction_type']}

Category: {row['category']}

Payment Method: {row['payment_method']}

Account Type: {row['account_type']}

City: {row['city']}

Flow: {row['flow']}

Transaction Size: {row['transaction_size']}

Weekday: {row['weekday']}

Month: {row['transaction_month']}

Year: {row['year']}
"""

            documents.append(document.strip())

        logger.success(
            f"{len(documents)} DataFrame documents created."
        )

        return documents

    @staticmethod
    def build_metadata(
        transaction: Transaction
    ) -> dict:

        return {

            "transaction_id": transaction.transaction_id,

            "merchant": transaction.merchant,

            "category": transaction.category,

            "amount": float(transaction.amount),

            "city": transaction.city,

            "payment_method": transaction.payment_method,

            "transaction_type": transaction.transaction_type,

            "flow": transaction.flow,

            "transaction_size": transaction.transaction_size,

            "month": transaction.transaction_month,

            "year": transaction.year

        }

    @staticmethod
    def build_metadatas(
        transactions: List[Transaction]
    ) -> List[dict]:

        return [

            DocumentBuilder.build_metadata(transaction)

            for transaction in transactions

        ]