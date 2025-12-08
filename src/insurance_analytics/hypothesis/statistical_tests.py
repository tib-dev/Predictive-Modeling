"""
hypothesis_tests.py

Run statistical tests for insurance A/B hypotheses.
"""

from typing import List, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats


def chi2_test_categorical(df: pd.DataFrame, feature: str, kpi: str = "ClaimFrequency") -> Tuple[float, float]:
    """
    Chi-square test for independence between a categorical feature and binary KPI.
    
    Returns:
        chi2_statistic, p_value
    """
    contingency = pd.crosstab(df[feature], df[kpi])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return chi2, p


def t_test_numeric(df: pd.DataFrame, feature: str, kpi: str) -> Tuple[float, float]:
    """
    Two-sample t-test for numeric KPI across two groups defined by a binary/categorical feature.
    If feature has more than 2 levels, caller should subset the groups.
    
    Returns:
        t_statistic, p_value
    """
    levels = df[feature].dropna().unique()
    if len(levels) != 2:
        raise ValueError(
            f"T-test requires exactly 2 groups; found {len(levels)} in feature '{feature}'")

    g1 = df[df[feature] == levels[0]][kpi].dropna()
    g2 = df[df[feature] == levels[1]][kpi].dropna()

    t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False)
    return t_stat, p_value


def anova_numeric(df: pd.DataFrame, feature: str, kpi: str) -> Tuple[float, float]:
    """
    One-way ANOVA for numeric KPI across multiple levels of a categorical feature.
    
    Returns:
        F_statistic, p_value
    """
    groups = [g[kpi].dropna() for name, g in df.groupby(feature)]
    F_stat, p_value = stats.f_oneway(*groups)
    return F_stat, p_value


def run_hypothesis_tests(df: pd.DataFrame, hypotheses: Optional[List[dict]] = None) -> pd.DataFrame:
    """
    Run predefined hypotheses tests.
    
    hypotheses: list of dicts, each with:
        - "feature": column to test (e.g., 'Province')
        - "kpi": which KPI to test ('ClaimFrequency', 'ClaimSeverity', 'Margin')
        - "test_type": 'chi2', 't', or 'anova'
        - "description": optional string description
    
    Returns:
        pandas DataFrame with columns:
        - feature, kpi, test_type, statistic, p_value, reject_null (bool), description
    """
    if hypotheses is None:
        # Default based on your business problem
        hypotheses = [
            {"feature": "Province", "kpi": "ClaimFrequency", "test_type": "chi2",
                "description": "Risk differences across provinces"},
            {"feature": "PostalCode", "kpi": "ClaimFrequency", "test_type": "chi2",
                "description": "Risk differences across zipcodes"},
            {"feature": "PostalCode", "kpi": "Margin", "test_type": "anova",
                "description": "Margin differences across zipcodes"},
            {"feature": "Gender", "kpi": "ClaimFrequency",
                "test_type": "chi2", "description": "Risk differences by gender"}
        ]

    results = []
    for h in hypotheses:
        try:
            if h["test_type"] == "chi2":
                stat, p = chi2_test_categorical(df, h["feature"], h["kpi"])
            elif h["test_type"] == "t":
                stat, p = t_test_numeric(df, h["feature"], h["kpi"])
            elif h["test_type"] == "anova":
                stat, p = anova_numeric(df, h["feature"], h["kpi"])
            else:
                raise ValueError(f"Unknown test_type '{h['test_type']}'")

            reject_null = p < 0.05
            results.append({
                "feature": h["feature"],
                "kpi": h["kpi"],
                "test_type": h["test_type"],
                "statistic": stat,
                "p_value": p,
                "reject_null": reject_null,
                "description": h.get("description", "")
            })
        except Exception as e:
            results.append({
                "feature": h.get("feature"),
                "kpi": h.get("kpi"),
                "test_type": h.get("test_type"),
                "statistic": np.nan,
                "p_value": np.nan,
                "reject_null": False,
                "description": str(e)
            })
    return pd.DataFrame(results)

