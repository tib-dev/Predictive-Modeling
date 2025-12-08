"""
Module for insurance data segmentation and control of confounders for A/B testing.
"""

from typing import List, Optional, Tuple, Union
import pandas as pd
import numpy as np


def split_control_test(
    df: pd.DataFrame,
    feature: str,
    group_a_values: Union[List, str, int],
    group_b_values: Union[List, str, int],
    copy: bool = True
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split dataframe into Control (A) and Test (B) based on values of a feature.

    Parameters:
        df: pandas DataFrame.
        feature: column name used for segmentation.
        group_a_values: value(s) in feature for Control group.
        group_b_values: value(s) in feature for Test group.
        copy: if True, return copies; else return views.

    Returns:
        df_a, df_b: Control and Test dataframes.
    """
    if feature not in df.columns:
        raise ValueError(f"Feature '{feature}' not found in DataFrame")

    # Ensure lists
    if not isinstance(group_a_values, list):
        group_a_values = [group_a_values]
    if not isinstance(group_b_values, list):
        group_b_values = [group_b_values]

    df_a = df[df[feature].isin(group_a_values)]
    df_b = df[df[feature].isin(group_b_values)]

    if copy:
        return df_a.copy(), df_b.copy()
    else:
        return df_a, df_b


def check_balance(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    confounders: Optional[List[str]] = None,
    threshold: float = 0.05
) -> pd.DataFrame:
    """
    Check for confounders across Control and Test groups.
    Returns a summary dataframe with mean or proportion differences.

    Parameters:
        df_a, df_b: DataFrames for Control and Test.
        confounders: list of columns to check balance. If None, uses all except target.
        threshold: absolute difference threshold for flagging imbalance.

    Returns:
        pandas DataFrame with columns:
            - feature
            - type (numeric/categorical)
            - value_a
            - value_b
            - difference
            - imbalanced (bool)
    """
    if confounders is None:
        # Exclude known KPI columns if they exist
        confounders = [c for c in df_a.columns if c not in [
            "ClaimIndicator", "ClaimSeverity", "Margin", "MarginRate", "PolicyID"]]

    summary = []
    for col in confounders:
        if pd.api.types.is_numeric_dtype(df_a[col]):
            val_a = df_a[col].mean()
            val_b = df_b[col].mean()
            diff = val_b - val_a
            summary.append({
                "feature": col,
                "type": "numeric",
                "value_a": val_a,
                "value_b": val_b,
                "difference": diff,
                "imbalanced": abs(diff) > threshold
            })
        else:
            # categorical: compare proportion of each category
            prop_a = df_a[col].value_counts(normalize=True, dropna=False)
            prop_b = df_b[col].value_counts(normalize=True, dropna=False)
            all_values = set(prop_a.index).union(prop_b.index)
            for val in all_values:
                p_a = prop_a.get(val, 0)
                p_b = prop_b.get(val, 0)
                diff = p_b - p_a
                summary.append({
                    "feature": col,
                    "type": "categorical",
                    "value_a": p_a,
                    "value_b": p_b,
                    "difference": diff,
                    "imbalanced": abs(diff) > threshold
                })

    return pd.DataFrame(summary)


def filter_balanced_confounders(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    confounders: Optional[List[str]] = None,
    threshold: float = 0.05
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Returns Control and Test groups, along with a balance report for confounders.

    Parameters:
        df_a, df_b: Control and Test groups.
        confounders: columns to check balance
        threshold: maximum allowed absolute difference

    Returns:
        df_a, df_b, balance_report
    """
    balance_report = check_balance(
        df_a, df_b, confounders=confounders, threshold=threshold)
    return df_a, df_b, balance_report


def summarize_groups(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    kpi_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Compute simple summary statistics (mean, median) for Control/Test groups.

    Parameters:
        df_a, df_b: Control and Test groups.
        kpi_columns: columns to summarize; if None, use ClaimIndicator, ClaimSeverity, Margin

    Returns:
        pandas DataFrame with summary stats.
    """
    if kpi_columns is None:
        kpi_columns = ["ClaimIndicator",
                       "ClaimSeverity", "Margin", "MarginRate"]

    summary = []
    for col in kpi_columns:
        if col not in df_a.columns or col not in df_b.columns:
            continue
        summary.append({
            "kpi": col,
            "control_mean": df_a[col].mean(),
            "test_mean": df_b[col].mean(),
            "control_median": df_a[col].median(),
            "test_median": df_b[col].median(),
            "control_count": df_a[col].count(),
            "test_count": df_b[col].count()
        })
    return pd.DataFrame(summary)


# -------------------------
# Example usage (not executed)
# -------------------------
_example_usage = """
import pandas as pd
from segmentation import split_control_test, filter_balanced_confounders, summarize_groups

df = pd.read_csv("insurance_data.csv")
df = attach_metrics(df)  # from your KPI module

# Split by feature, e.g., Gender
df_a, df_b = split_control_test(df, feature="Gender", group_a_values="Male", group_b_values="Female")

# Check confounders (e.g., Age, Province)
df_a, df_b, balance_report = filter_balanced_confounders(df_a, df_b, confounders=["Province", "VehicleType"])

# Quick KPI summary by group
summary = summarize_groups(df_a, df_b)
print(summary)
print(balance_report)
"""
