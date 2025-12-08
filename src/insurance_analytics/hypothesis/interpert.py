import pandas as pd
def hypothesis_summary_generator(results_df):
    """
    Generator that yields a summary of hypothesis test results row by row.

    Parameters
    ----------
    results_df : pd.DataFrame
        DataFrame containing hypothesis test results with columns:
        ['feature', 'kpi', 'p_value', 'reject_null', 'description']

    Yields
    ------
    str
        Human-readable summary line for each hypothesis
    """
    for _, row in results_df.iterrows():
        if pd.isna(row['p_value']):
            yield f"Cannot compute test for {row['feature']} on KPI {row['kpi']} ({row.get('description','')})"
        elif row['reject_null']:
            yield f"Reject H0 for {row['feature']} on KPI {row['kpi']}: p={row['p_value']:.4f}"
        else:
            yield f"Fail to reject H0 for {row['feature']} on KPI {row['kpi']}: p={row['p_value']:.4f}"
