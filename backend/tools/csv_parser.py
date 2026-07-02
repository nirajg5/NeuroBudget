"""
CSV Parser

Responsible for reading transaction CSV files.
"""

from pathlib import Path

import pandas as pd

from core.logger import logger


class CSVParser:
    """
    Reads transaction CSV files.
    """

    ALLOWED_EXTENSIONS = [".csv"]

    @staticmethod
    def read_csv(file_path: str | Path) -> pd.DataFrame:
        """
        Read CSV file and return a DataFrame.

        Parameters
        ----------
        file_path : str | Path

        Returns
        -------
        pd.DataFrame
        """

        file_path = Path(file_path)

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(file_path)

        if file_path.suffix.lower() not in CSVParser.ALLOWED_EXTENSIONS:
            logger.error("Only CSV files are supported.")
            raise ValueError("Invalid file type.")

        try:

            df = pd.read_csv(file_path)

            logger.success(
                f"CSV loaded successfully ({len(df)} rows)"
            )

            return df

        except Exception as e:

            logger.exception("Failed to read CSV.")

            raise e

    @staticmethod
    def get_shape(df: pd.DataFrame):
        """
        Return rows and columns.
        """

        return df.shape

    @staticmethod
    def get_columns(df: pd.DataFrame):
        """
        Return column names.
        """

        return list(df.columns)

    @staticmethod
    def preview(df: pd.DataFrame, rows: int = 5):
        """
        Preview first N rows.
        """

        return df.head(rows)

    @staticmethod
    def dataframe_info(df: pd.DataFrame):
        """
        Return basic DataFrame statistics.
        """

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "memory_mb": round(
                df.memory_usage(deep=True).sum() / 1024 / 1024,
                2
            ),

            "column_names": list(df.columns)

        }