"""
Upload Service

Coordinates the complete CSV upload pipeline.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from core.logger import logger

from tools.csv_parser import CSVParser
from tools.validator import DataValidator
from tools.data_cleaner import DataCleaner
from tools.feature_engineering import FeatureEngineering

from database.models import Transaction
from database.crud.transaction_crud import create_transaction

class UploadService:

    """
    Complete Upload Pipeline
    """

    def __init__(self, db: Session):

        self.db = db

    def read_file(self, file_path: str | Path):

        logger.info("Reading CSV...")

        return CSVParser.read_csv(file_path)

    def validate(self, df: pd.DataFrame):

        logger.info("Validating CSV...")

        DataValidator.validate(df)

        return df

    def clean(self, df: pd.DataFrame):

        logger.info("Cleaning Data...")

        return DataCleaner.clean(df)

    def engineer(self, df: pd.DataFrame):

        logger.info("Generating Features...")

        return FeatureEngineering.engineer(df)
    
    def save_transactions(
        self,
        df: pd.DataFrame
    ):

        logger.info("Saving Transactions...")

        inserted = 0

        for _, row in df.iterrows():

            transaction = Transaction(

                transaction_date=row["transaction_date"],

                merchant=row["merchant"],

                description=row["description"],

                amount=float(row["amount"]),

                transaction_type=row["transaction_type"],

                category=row["category"],

                payment_method=row["payment_method"],

                account_type=row["account_type"],

                city=row["city"],

                balance_after_transaction=float(
                    row["balance_after_transaction"]
                ),

                transaction_month=row["transaction_month"],

                month_number=int(row["month_number"]),

                day=int(row["day"]),

                weekday=row["weekday"],

                quarter=int(row["quarter"]),

                year=int(row["year"]),

                is_weekend=bool(row["is_weekend"]),

                flow=row["flow"],

                transaction_size=row["transaction_size"]

            )

            create_transaction(
                self.db,
                transaction
            )

            inserted += 1

        logger.success(
            f"{inserted} transactions inserted."
        )

        return inserted

    def process_upload(
        self,
        file_path: str | Path
    ):

        df = self.read_file(file_path)

        self.validate(df)

        df = self.clean(df)

        df = self.engineer(df)

        inserted = self.save_transactions(df)

        return {

            "status": "success",

            "rows_processed": len(df),

            "rows_inserted": inserted,

            "columns": list(df.columns)

        }


    
    