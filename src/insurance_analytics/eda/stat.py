# src/insurance_analytics/eda/descriptive_stats.py

import pandas as pd
from typing import List, Optional


def descriptive_statistics(
    df: pd.DataFrame,
    numeric_cols: Optional[List[str]] = None,
    round_digits: int = 2
) -> pd.DataFrame:
    """
    Generate descriptive statistics (count, mean, median, std, min, max)
    for selected numeric columns in a DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset.
    numeric_cols : Optional[List[str]]
        Columns to summarize. If None, all numeric columns will be summarized.
    round_digits : int
        Number of decimal places to round the statistics.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing descriptive statistics.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()

    stats = df[numeric_cols].agg(
        ['count', 'mean', 'median', 'std', 'min', 'max'])
    stats = stats.round(round_digits).T  # Transpose for easier reading
    stats.index.name = "Column"

    return stats


def summarize_for_markdown(df: pd.DataFrame, numeric_cols: Optional[List[str]] = None) -> str:
    """
    Convert descriptive statistics to a markdown table string.

    Parameters:
    -----------
    df : pd.DataFrame
        Input dataset.
    numeric_cols : Optional[List[str]]
        Columns to summarize.

    Returns:
    --------
    str
        Markdown table of descriptive statistics.
    """
    stats_df = descriptive_statistics(df, numeric_cols=numeric_cols)
    return stats_df.to_markdown()
