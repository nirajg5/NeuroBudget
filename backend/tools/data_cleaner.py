"""
Data Cleaning Utilities

Cleans validated transaction data.
"""

import pandas as pd

from core.logger import logger


class DataCleaner:

    # =====================================================
    # Remove duplicate rows
    # =====================================================

    @staticmethod
    def remove_duplicates(df: pd.DataFrame):

        before = len(df)

        df = df.drop_duplicates()

        after = len(df)

        logger.success(
            f"Removed {before-after} duplicate rows."
        )

        return df

    # =====================================================
    # Trim whitespace
    # =====================================================

    @staticmethod
    def trim_strings(df: pd.DataFrame):

        object_columns = df.select_dtypes(
            include="object"
        ).columns

        for column in object_columns:

            df[column] = (

                df[column]

                .astype(str)

                .str.strip()

            )

        logger.success("Whitespace removed.")

        return df

    # =====================================================
    # Standardize Merchant Names
    # =====================================================

    @staticmethod
    def standardize_merchants(df: pd.DataFrame):

        df["merchant"] = (

            df["merchant"]

            .str.title()

        )

        logger.success("Merchant names standardized.")

        return df

    # =====================================================
    # Standardize Categories
    # =====================================================

    @staticmethod
    def standardize_categories(df: pd.DataFrame):

        df["category"] = (

            df["category"]

            .str.title()

        )

        logger.success("Categories standardized.")

        return df

    # =====================================================
    # Convert Amount
    # =====================================================

    @staticmethod
    def convert_amount(df: pd.DataFrame):

        df["amount"] = (

            pd.to_numeric(

                df["amount"],

                errors="coerce"

            )

        )

        logger.success("Amount converted to float.")

        return df

    # =====================================================
    # Convert Date
    # =====================================================

    @staticmethod
    def convert_date(df: pd.DataFrame):

        df["transaction_date"] = pd.to_datetime(

            df["transaction_date"]

        )

        logger.success("Dates converted.")

        return df

    # =====================================================
    # Fill Description
    # =====================================================

    @staticmethod
    def fill_description(df: pd.DataFrame):

        df["description"] = (

            df["description"]

            .fillna("No Description")

        )

        logger.success("Descriptions filled.")

        return df

    # =====================================================
    # Sort by Date
    # =====================================================

    @staticmethod
    def sort_transactions(df: pd.DataFrame):

        df = df.sort_values(

            by="transaction_date"

        )

        logger.success("Transactions sorted.")

        return df

    # =====================================================
    # Reset Index
    # =====================================================

    @staticmethod
    def reset_index(df: pd.DataFrame):

        df = df.reset_index(drop=True)

        logger.success("Index reset.")

        return df

    # =====================================================
    # Complete Cleaning Pipeline
    # =====================================================

    @staticmethod
    def clean(df: pd.DataFrame):

        logger.info("Starting Data Cleaning...")

        df = DataCleaner.remove_duplicates(df)

        df = DataCleaner.trim_strings(df)

        df = DataCleaner.standardize_merchants(df)

        df = DataCleaner.standardize_categories(df)

        df = DataCleaner.convert_amount(df)

        df = DataCleaner.convert_date(df)

        df = DataCleaner.fill_description(df)

        df = DataCleaner.sort_transactions(df)

        df = DataCleaner.reset_index(df)

        logger.success("Data cleaning completed.")

        return df