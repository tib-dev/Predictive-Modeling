# src/insurance_analytics/eda/exploration.py

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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

    return df


def duplicated_rows(df: pd.DataFrame):
    """
    Count duplicated rows in the dataset.
    """
    dup_count = df.duplicated().sum()
    print(f"Duplicated rows: {dup_count}")
    return dup_count


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
