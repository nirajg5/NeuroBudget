"""
Feature Engineering

Creates AI-ready features from transaction data.
"""

import pandas as pd

from core.logger import logger


class FeatureEngineering:

    # ======================================================
    # Transaction Month
    # ======================================================

    @staticmethod
    def add_transaction_month(df: pd.DataFrame):

        df["transaction_month"] = (
            df["transaction_date"]
            .dt.month_name()
        )

        logger.success("transaction_month created.")

        return df

    # ======================================================
    # Month Number
    # ======================================================

    @staticmethod
    def add_month_number(df: pd.DataFrame):

        df["month_number"] = (
            df["transaction_date"]
            .dt.month
        )

        logger.success("month_number created.")

        return df

    # ======================================================
    # Day
    # ======================================================

    @staticmethod
    def add_day(df: pd.DataFrame):

        df["day"] = (
            df["transaction_date"]
            .dt.day
        )

        logger.success("day created.")

        return df

    # ======================================================
    # Weekday
    # ======================================================

    @staticmethod
    def add_weekday(df: pd.DataFrame):

        df["weekday"] = (
            df["transaction_date"]
            .dt.day_name()
        )

        logger.success("weekday created.")

        return df

    # ======================================================
    # Quarter
    # ======================================================

    @staticmethod
    def add_quarter(df: pd.DataFrame):

        df["quarter"] = (
            df["transaction_date"]
            .dt.quarter
        )

        logger.success("quarter created.")

        return df

    # ======================================================
    # Year
    # ======================================================

    @staticmethod
    def add_year(df: pd.DataFrame):

        df["year"] = (
            df["transaction_date"]
            .dt.year
        )

        logger.success("year created.")

        return df

    # ======================================================
    # Weekend
    # ======================================================

    @staticmethod
    def add_weekend(df: pd.DataFrame):

        df["is_weekend"] = (
            df["transaction_date"]
            .dt.weekday >= 5
        )

        logger.success("is_weekend created.")

        return df

    # ======================================================
    # Flow
    # ======================================================

    @staticmethod
    def add_flow(df: pd.DataFrame):

        df["flow"] = df["transaction_type"].map({

            "Credit": "Income",

            "Debit": "Expense"

        })

        logger.success("flow created.")

        return df

    # ======================================================
    # Transaction Size
    # ======================================================

    @staticmethod
    def add_transaction_size(df: pd.DataFrame):

        def classify(amount):

            if amount < 1000:
                return "Small"

            elif amount < 10000:
                return "Medium"

            return "Large"

        df["transaction_size"] = (
            df["amount"]
            .apply(classify)
        )

        logger.success("transaction_size created.")

        return df

    # ======================================================
    # Run Complete Feature Engineering
    # ======================================================

    @staticmethod
    def engineer(df: pd.DataFrame):

        logger.info("Starting Feature Engineering...")

        df = FeatureEngineering.add_transaction_month(df)

        df = FeatureEngineering.add_month_number(df)

        df = FeatureEngineering.add_day(df)

        df = FeatureEngineering.add_weekday(df)

        df = FeatureEngineering.add_quarter(df)

        df = FeatureEngineering.add_year(df)

        df = FeatureEngineering.add_weekend(df)

        df = FeatureEngineering.add_flow(df)

        df = FeatureEngineering.add_transaction_size(df)

        logger.success("Feature Engineering Completed.")

        return df