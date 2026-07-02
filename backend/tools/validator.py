"""
Data Validator

Validates uploaded transaction CSV.
"""

import pandas as pd

from core.logger import logger


class DataValidator:

    REQUIRED_COLUMNS = [

        "transaction_id",

        "transaction_date",

        "merchant",

        "description",

        "amount",

        "transaction_type",

        "category",

        "payment_method",

        "account_type",

        "city",

        "balance_after_transaction"

    ]

    VALID_TRANSACTION_TYPES = [

        "Credit",

        "Debit"

    ]

    # =====================================================
    # Validate Required Columns
    # =====================================================

    @staticmethod
    def validate_columns(df: pd.DataFrame):

        missing = [

            column

            for column in DataValidator.REQUIRED_COLUMNS

            if column not in df.columns

        ]

        if missing:

            raise ValueError(

                f"Missing columns: {missing}"

            )

        logger.success("Required columns validated.")

    # =====================================================
    # Empty DataFrame
    # =====================================================

    @staticmethod
    def validate_empty(df: pd.DataFrame):

        if df.empty:

            raise ValueError(

                "Uploaded CSV is empty."

            )

        logger.success("CSV is not empty.")

    # =====================================================
    # Missing Values
    # =====================================================

    @staticmethod
    def validate_missing_values(df: pd.DataFrame):

        missing = df.isnull().sum()

        missing = missing[missing > 0]

        if len(missing) > 0:

            raise ValueError(

                f"Missing values found:\n{missing}"

            )

        logger.success("No missing values.")

    # =====================================================
    # Duplicate Transaction IDs
    # =====================================================

    @staticmethod
    def validate_duplicates(df: pd.DataFrame):

        duplicates = df.duplicated(

            subset=["transaction_id"]

        )

        if duplicates.any():

            raise ValueError(

                "Duplicate transaction IDs found."

            )

        logger.success("No duplicate transaction IDs.")

    # =====================================================
    # Amount Validation
    # =====================================================

    @staticmethod
    def validate_amount(df: pd.DataFrame):

        invalid = df[df["amount"] <= 0]

        if len(invalid) > 0:

            raise ValueError(

                "Invalid transaction amounts detected."

            )

        logger.success("Amounts validated.")

    # =====================================================
    # Transaction Type
    # =====================================================

    @staticmethod
    def validate_transaction_type(df: pd.DataFrame):

        invalid = df[

            ~df["transaction_type"].isin(

                DataValidator.VALID_TRANSACTION_TYPES

            )

        ]

        if len(invalid) > 0:

            raise ValueError(

                "Invalid transaction types detected."

            )

        logger.success("Transaction types validated.")

    # =====================================================
    # Date Validation
    # =====================================================

    @staticmethod
    def validate_dates(df: pd.DataFrame):

        try:

            pd.to_datetime(

                df["transaction_date"]

            )

        except Exception:

            raise ValueError(

                "Invalid transaction dates."

            )

        logger.success("Dates validated.")

    # =====================================================
    # Run All Validation
    # =====================================================

    @staticmethod
    def validate(df: pd.DataFrame):

        logger.info("Starting Data Validation...")

        DataValidator.validate_empty(df)

        DataValidator.validate_columns(df)

        DataValidator.validate_missing_values(df)

        DataValidator.validate_duplicates(df)

        DataValidator.validate_amount(df)

        DataValidator.validate_transaction_type(df)

        DataValidator.validate_dates(df)

        logger.success("All validations passed.")

        return True