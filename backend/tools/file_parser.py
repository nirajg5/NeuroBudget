"""
file_parser.py — Handles CSV and PDF file parsing.
Normalizes raw file data into a standard transaction DataFrame.
"""

import pandas as pd
import pdfplumber
import io
from typing import List, Dict, Optional, Tuple
from tools.categorizer import categorize_transaction


# ─── CSV Column Name Normalization ────────────────────────────────────────────
# Banks export CSVs with different column names. We normalize them.

DATE_ALIASES = ["date", "transaction date", "txn date", "value date", "trans date"]
DESC_ALIASES = ["description", "narration", "particulars", "details", "remarks",
                "merchant", "name", "transaction", "txn description"]
AMOUNT_ALIASES = ["amount", "debit", "withdrawal", "credit", "transaction amount",
                  "dr amount", "cr amount", "spent", "paid"]


def _find_column(df: pd.DataFrame, aliases: List[str]) -> Optional[str]:
    """Find the first column name that matches any alias (case-insensitive)."""
    cols_lower = {col.lower().strip(): col for col in df.columns}
    for alias in aliases:
        if alias in cols_lower:
            return cols_lower[alias]
    return None


def parse_csv(filepath: str, filename: str) -> Tuple[pd.DataFrame, str]:
    """
    Parse a bank transaction CSV file.

    Returns:
        (DataFrame with columns: date, description, amount, category, source)
        error message if parsing fails (empty string if success)
    """
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        return pd.DataFrame(), f"Failed to read CSV: {str(e)}"

    # Identify columns
    date_col = _find_column(df, DATE_ALIASES)
    desc_col = _find_column(df, DESC_ALIASES)
    amount_col = _find_column(df, AMOUNT_ALIASES)

    # If we can't find essential columns, try positional (first 3 columns)
    if not date_col:
        date_col = df.columns[0] if len(df.columns) > 0 else None
    if not desc_col:
        desc_col = df.columns[1] if len(df.columns) > 1 else None
    if not amount_col:
        amount_col = df.columns[2] if len(df.columns) > 2 else None

    if not all([date_col, desc_col, amount_col]):
        return pd.DataFrame(), "Could not detect date, description, or amount columns."

    # Build normalized DataFrame
    result = pd.DataFrame()
    result["date"] = df[date_col].astype(str).str.strip()
    result["description"] = df[desc_col].astype(str).str.strip()

    # Clean and parse amount — handle comma-separated numbers like "1,234.56"
    result["amount"] = (
        df[amount_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    result["amount"] = pd.to_numeric(result["amount"], errors="coerce").abs()

    # Drop rows where amount is null
    result = result.dropna(subset=["amount"])
    result = result[result["amount"] > 0]

    # Categorize each transaction
    result["category"] = result["description"].apply(categorize_transaction)
    result["source"] = filename

    # Reset index
    result = result.reset_index(drop=True)

    return result, ""


def parse_pdf(filepath: str, filename: str) -> Tuple[pd.DataFrame, str]:
    """
    Extract transaction table data from a PDF bank statement.
    Uses pdfplumber to find tables and parse them.
    """
    try:
        all_rows = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and len(row) >= 3:
                            all_rows.append(row[:3])  # Take first 3 columns

        if not all_rows:
            return pd.DataFrame(), "No tables found in PDF."

        # Use first row as header if it looks like a header
        headers = all_rows[0]
        data_rows = all_rows[1:]

        if not data_rows:
            return pd.DataFrame(), "No data rows found in PDF table."

        df = pd.DataFrame(data_rows, columns=[str(h).lower() for h in headers])

        # Re-use CSV parser logic by writing to temp CSV
        temp_path = filepath.replace(".pdf", "_temp.csv")
        df.to_csv(temp_path, index=False)
        result, error = parse_csv(temp_path, filename)

        # Cleanup temp file
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return result, error

    except Exception as e:
        return pd.DataFrame(), f"PDF parsing error: {str(e)}"


def dataframe_to_transactions(df: pd.DataFrame) -> List[Dict]:
    """Convert parsed DataFrame rows into list of transaction dicts."""
    transactions = []
    for _, row in df.iterrows():
        transactions.append({
            "date": str(row.get("date", "")),
            "description": str(row.get("description", "")),
            "amount": float(row.get("amount", 0)),
            "category": str(row.get("category", "Other")),
            "source": str(row.get("source", "upload")),
        })
    return transactions
