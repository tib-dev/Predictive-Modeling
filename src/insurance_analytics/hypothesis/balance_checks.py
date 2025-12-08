
"""
-------------------
Check if Control and Test groups are comparable on key confounders.
Supports numeric and categorical features.
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def check_balance(df_control, df_test, confounders, plot=False):
    """
    Check balance between control and test groups on specified confounders.

    Parameters
    ----------
    df_control : pd.DataFrame
        Control group
    df_test : pd.DataFrame
        Test group
    confounders : list of str
        List of columns to check balance
    plot : bool
        If True, plot distributions for numeric features

    Returns
    -------
    pd.DataFrame
        Summary table with balance check results
    """
    balance_report = []

    for feature in confounders:
        if df_control[feature].dtype in ['int64','float64']:
            # Numeric feature
            mean_a = df_control[feature].mean()
            mean_b = df_test[feature].mean()
            t_stat, p_val = stats.ttest_ind(
                df_control[feature].dropna(),
                df_test[feature].dropna(),
                equal_var=False
            )
            balanced = p_val > 0.05
            balance_report.append({
                'feature': feature,
                'type': 'numeric',
                'mean_control': mean_a,
                'mean_test': mean_b,
                'p_value': p_val,
                'balanced': balanced
            })

            # Plot distribution if requested
            if plot:
                sns.kdeplot(df_control[feature].dropna(), label='Control')
                sns.kdeplot(df_test[feature].dropna(), label='Test')
                plt.title(f'Distribution of {feature}')
                plt.legend()
                plt.show()

        else:
            # Categorical feature
            contingency = pd.crosstab(df_control[feature], df_test[feature])
            try:
                chi2, p, dof, expected = stats.chi2_contingency(contingency)
            except ValueError:
                chi2, p = np.nan, np.nan  # Handle low counts
            balanced = p > 0.05 if not np.isnan(p) else False
            balance_report.append({
                'feature': feature,
                'type': 'categorical',
                'chi2': chi2,
                'p_value': p,
                'balanced': balanced
            })

            # Optional bar plot
            if plot:
                df_concat = pd.concat([df_control[feature].value_counts(normalize=True),
                                       df_test[feature].value_counts(normalize=True)], axis=1)
                df_concat.columns = ['Control', 'Test']
                df_concat.plot(kind='bar', figsize=(6,4), title=f'Distribution of {feature}')
                plt.show()

    return pd.DataFrame(balance_report)
