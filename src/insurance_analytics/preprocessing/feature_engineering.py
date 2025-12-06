# src/insurance_analytics/features/feature_engineering.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# -------------------------------------------------------------
# 1) DATE FEATURES
# -------------------------------------------------------------
def add_date_features(df: pd.DataFrame, date_col: str = "TransactionMonth"):
    """
    Extract useful features from a datetime column.
    """
    if date_col not in df.columns:
        return df

    if not np.issubdtype(df[date_col].dtype, np.datetime64):
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["quarter"] = df[date_col].dt.quarter
    df["is_month_start"] = df[date_col].dt.is_month_start.astype(int)
    df["is_month_end"] = df[date_col].dt.is_month_end.astype(int)

    return df


# -------------------------------------------------------------
# 2) NUMERIC BINNING (OPTIONAL)
# -------------------------------------------------------------
def bin_numeric(df: pd.DataFrame, col: str, bins: int = 5):
    """
    Create quantile-based bins for a numeric column.

    Example: Age → Age_bin (5 bins)
    """
    if col not in df.columns:
        return df

    if not np.issubdtype(df[col].dtype, np.number):
        return df

    df[f"{col}_bin"] = pd.qcut(df[col], q=bins, duplicates="drop")
    return df


# -------------------------------------------------------------
# 3) TARGET ENCODING (SAFE VERSION)
# -------------------------------------------------------------
def target_encode(df: pd.DataFrame, col: str, target: str):
    """
    Encode categorical column by mean of target.

    Example: Bank → avg premium
    """
    if col not in df.columns or target not in df.columns:
        return df

    if np.issubdtype(df[target].dtype, np.number) is False:
        return df

    means = df.groupby(col)[target].mean()
    df[f"{col}_te"] = df[col].map(means)
    return df


# -------------------------------------------------------------
# 4) ONE-HOT ENCODING PIPELINE (for modeling)
# -------------------------------------------------------------
def prepare_preprocessor(df: pd.DataFrame):
    """
    Automatically build a ColumnTransformer:
    - OneHotEncoder for categorical
    - StandardScaler for numeric
    """

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]).columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    return preprocessor, numeric_cols, categorical_cols


# -------------------------------------------------------------
# 5) INTERACTION FEATURES
# -------------------------------------------------------------
def add_interactions(df: pd.DataFrame, pairs: list[tuple]):
    """
    Create interaction features through multiplication.

    Example:
        pairs = [
            ("EngineCapacity", "VehicleAge"),
            ("TotalPremium", "TotalClaims")
        ]
    """
    for col1, col2 in pairs:
        if col1 in df.columns and col2 in df.columns:
            name = f"{col1}_x_{col2}"
            df[name] = df[col1] * df[col2]

    return df


# -------------------------------------------------------------
# 6) FEATURE SELECTION HOOK (for task 2 modeling)
# -------------------------------------------------------------
def remove_low_variance(df: pd.DataFrame, threshold: float = 0.0):
    """
    Drop columns that have zero or near-zero variance.
    """

    low_var_cols = [
        col for col in df.columns
        if df[col].nunique() <= 1
    ]

    df = df.drop(columns=low_var_cols)

    return df

# -------------------------------------------------------------
# 7) LOSS RATIO
# -------------------------------------------------------------


def add_loss_ratio(df: pd.DataFrame, claims_col: str = "TotalClaims", premium_col: str = "TotalPremium"):
    """
    Add Loss Ratio column: LossRatio = TotalClaims / TotalPremium.
    Handles zero or missing premiums safely.
    """
    if claims_col not in df.columns or premium_col not in df.columns:
        return df

    df["LossRatio"] = df[claims_col] / df[premium_col].replace({0: np.nan})
    return df
