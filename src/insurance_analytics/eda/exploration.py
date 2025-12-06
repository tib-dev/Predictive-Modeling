# src/insurance_analytics/eda/exploration.py

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

# -------------------------------------------------------------
# 1) STRUCTURAL SUMMARY
# -------------------------------------------------------------
def dataset_overview(df: pd.DataFrame):
    """
    Returns basic overview: shape, column names, dtypes.
    """
    print("\n--- Dataset Shape ---")
    print(df.shape)

    print("\n--- Column Info ---")
    print(df.dtypes)

    print("\n--- Total Missing Values (%) ---")
    print((df.isna().mean() * 100).sort_values(ascending=False).head(20))
    df=df.head(5)
    return df


def duplicated_rows(df: pd.DataFrame):
    """
    Count duplicated rows in the dataset.
    """
    dup_count = df.duplicated().sum()
    print(f"Duplicated rows: {dup_count}")
    return dup_count
# -------------------------------------------------------------
# 2) MISSING DATA INSPECTION
# -------------------------------------------------------------
def summarize_missing(df: pd.DataFrame, top_n: Optional[int] = 20) -> pd.Series:
    """
    Compute the percentage of missing values per column and return the top N columns with highest missing rates.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to analyze.
    top_n : int, optional
        Number of top columns to return. Defaults to 20.

    Returns
    -------
    pd.Series
        Missing values as a fraction of total rows, sorted descending.
    """
    missing_pct = df.isna().mean().sort_values(ascending=False)
    return missing_pct.head(top_n)
# -------------------------------------------------------------
# 3) OUTLIER INSPECTION
# -------------------------------------------------------------
def detect_outliers_iqr(df: pd.DataFrame, col: str):
    """
    Use IQR rule to detect outliers for a numeric column.
    """
    if col not in df.columns:
        raise ValueError(f"{col} not found in DataFrame")

    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"{col}: {len(outliers)} outliers detected")
    return outliers
