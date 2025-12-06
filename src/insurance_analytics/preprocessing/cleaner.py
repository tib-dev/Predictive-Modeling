# src/insurance_analytics/data/cleaner.py

import pandas as pd
import numpy as np
from typing import List, Optional
import re

# -------------------------------------------------------------
# 1) STRING CLEANING
# -------------------------------------------------------------
def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim whitespace, normalize empty values, and clean string anomalies.
    """
    str_cols = df.select_dtypes(include="object").columns

    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    df.replace({"": np.nan, " ": np.nan}, inplace=True)

    # Replace weird zero strings (your custom rule)
    df.replace({".000000000000": 0}, inplace=True)

    return df


# -------------------------------------------------------------
# 2) DATE FIXING
# -------------------------------------------------------------
def fix_dates(df: pd.DataFrame, date_cols=None) -> pd.DataFrame:
    """
    Convert date columns using pandas. Handles both string dates and numeric epoch timestamps.
    """
    if date_cols is None:
        date_cols = ["TransactionMonth"]

    for col in date_cols:
        if col in df.columns:
            # If the column is integer-like (large numbers), treat as epoch in ns
            if pd.api.types.is_integer_dtype(df[col]):
                df[col] = pd.to_datetime(df[col], errors="coerce", unit="ns")
            else:
                df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


# -------------------------------------------------------------
# 3) NUMERIC FIXING
# -------------------------------------------------------------
def fix_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric-like columns to numeric when possible.
    """
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df


# -------------------------------------------------------------
# 4) MISSING DATA INSPECTION
# -------------------------------------------------------------
def summarize_missing(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Return the top N columns with the highest missing percentage.
    """
    missing_pct = df.isna().mean().sort_values(ascending=False)
    return missing_pct.head(top_n)


# -------------------------------------------------------------
# 5) MISSING DATA CLEANUP
# -------------------------------------------------------------
def clean_missing(df: pd.DataFrame, drop_threshold: float = 0.85) -> pd.DataFrame:
    """
    Drop columns where more than `drop_threshold` fraction is missing.
    """
    missing_pct = df.isna().mean()
    cols_to_drop = missing_pct[missing_pct > drop_threshold].index.tolist()

    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)

    return df



# -------------------------------------------------------------
# 6) FULL CLEANING PIPELINE
# -------------------------------------------------------------
def cleaning(
    df: pd.DataFrame,
    date_cols: Optional[List[str]] = None,
    drop_threshold: float = 0.85,
    report_missing: bool = True
) -> pd.DataFrame:
    """
    Apply the standard cleaning pipeline: strings → dates → numeric → missing.
    Optionally print or return the top missing-value columns.
    """

    # 1. clean string columns
    df = clean_strings(df)

    # 2. parse dates
    df = fix_dates(df, date_cols=date_cols)

    # 3. convert numeric-looking fields
    df = fix_numeric(df)

    # 5. drop excessively missing columns
    df = clean_missing(df, drop_threshold=drop_threshold)

    return df
