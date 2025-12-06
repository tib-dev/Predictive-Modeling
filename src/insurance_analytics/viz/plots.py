# src/insurance_analytics/viz/plots.py

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

sns.set_theme(style="whitegrid")



# -------------------------------------------------------------
# 2) UNIVARIATE ANALYSIS
# -------------------------------------------------------------
def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30, save_path: Path = None):
    """
    Plot a histogram for a numeric column.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    column : str
        Column name to plot.
    bins : int
        Number of bins in histogram.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(10, 5))
    ax = sns.histplot(df[column].dropna(), bins=bins,
                      kde=True, color="skyblue")
    ax.set_title(f"Distribution of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_bar(df: pd.DataFrame, column: str, top_n: int = 20, save_path: Path = None):
    """
    Plot a bar chart for categorical columns showing top N categories.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    column : str
        Categorical column to plot.
    top_n : int
        Show top N categories only.
    save_path : Path, optional
        Path to save the plot image.
    """
    counts = df[column].value_counts().nlargest(top_n)
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=counts.index, y=counts.values, palette="pastel")
    ax.set_title(f"Top {top_n} {column} Categories")
    ax.set_xlabel(column)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def missing_data_summary(df: pd.DataFrame, top_n: int = 20):
    """
    Show top N columns with the highest percentage of missing values.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    top_n : int
        Number of top missing columns to show.

    Returns
    -------
    pd.Series
        Percentage of missing values per column.
    """
    missing_pct = df.isna().mean().sort_values(ascending=False)
    return missing_pct.head(top_n)


def boxplot_numeric(df: pd.DataFrame, column: str, save_path: Path = None):
    """
    Boxplot to detect outliers in a numeric column.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    column : str
        Column to visualize.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(10, 5))
    ax = sns.boxplot(x=df[column], color="lightcoral")
    ax.set_title(f"Boxplot of {column}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()



# -------------------------------------------------------------
# 4) BIVARIATE ANALYSIS
# -------------------------------------------------------------


def correlation_matrix(df: pd.DataFrame, numeric_cols=None, save_path: Path = None):
    """
    Compute and plot a correlation matrix heatmap for numeric columns.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    numeric_cols : list, optional
        List of numeric columns to include. If None, selects all numeric columns.
    save_path : Path, optional
        Path to save the plot image.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

    corr = df[numeric_cols].corr()

    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
    return corr


def scatter_by_group(
    df: pd.DataFrame, x_col: str, y_col: str, hue_col: str, save_path: Path = None
):
    """
    Scatter plot of two numeric variables, colored by a categorical variable.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    x_col : str
        Column for x-axis.
    y_col : str
        Column for y-axis.
    hue_col : str
        Column for color grouping.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(12, 6))
    ax = sns.scatterplot(x=x_col, y=y_col, hue=hue_col,
                         data=df, alpha=0.6, palette="tab10")
    ax.set_title(f"{y_col} vs {x_col} by {hue_col}")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def boxplot_by_category(df: pd.DataFrame, numeric_col: str, category_col: str, save_path: Path = None):
    """
    Boxplot to visualize distribution of a numeric variable across categories.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    numeric_col : str
        Column with numeric data.
    category_col : str
        Column with categorical grouping.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(12, 6))
    ax = sns.boxplot(x=category_col, y=numeric_col, data=df, palette="pastel")
    ax.set_title(f"{numeric_col} by {category_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def pairplot_numeric(df: pd.DataFrame, numeric_cols=None, hue_col=None, save_path: Path = None):
    """
    Pairplot for numeric columns to explore pairwise relationships.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset.
    numeric_cols : list, optional
        Columns to include. Defaults to all numeric columns.
    hue_col : str, optional
        Categorical column for coloring.
    save_path : Path, optional
        Path to save the plot image.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()

    pairplot = sns.pairplot(
        df[numeric_cols + ([hue_col] if hue_col else [])], hue=hue_col)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

def plot_loss_ratio_by_province(df: pd.DataFrame, save_path: Path = None):
    """
    Bar plot: Average LossRatio by Province.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned insurance dataset with 'Province' and 'LossRatio' columns.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        x="Province",
        y="LossRatio",
        data=df.groupby("Province")["LossRatio"].mean().reset_index(),
        palette="Blues_r"
    )
    ax.set_title("Average Loss Ratio by Province")
    ax.set_ylabel("Loss Ratio")
    ax.set_xlabel("Province")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_loss_ratio_distribution(df: pd.DataFrame, save_path: Path = None):
    """
    Histogram + KDE: Distribution of LossRatio.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned insurance dataset with 'LossRatio'.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(10, 5))
    sns.histplot(df["LossRatio"].dropna(), bins=50, kde=True, color="orange")
    plt.title("Distribution of Loss Ratio")
    plt.xlabel("Loss Ratio")
    plt.ylabel("Frequency")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_claims_vs_premium_by_vehicle(df: pd.DataFrame, save_path: Path = None):
    """
    Scatter plot: TotalClaims vs TotalPremium colored by VehicleType.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned insurance dataset with 'TotalClaims', 'TotalPremium', 'VehicleType'.
    save_path : Path, optional
        Path to save the plot image.
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        x="TotalPremium",
        y="TotalClaims",
        hue="VehicleType",
        data=df,
        alpha=0.6,
        palette="tab10"
    )
    plt.title("Total Claims vs Total Premium by Vehicle Type")
    plt.xlabel("Total Premium")
    plt.ylabel("Total Claims")
    plt.legend(title="Vehicle Type", bbox_to_anchor=(
        1.05, 1), loc="upper left")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

# src/insurance_analytics/viz/outliers.py


sns.set_theme(style="whitegrid")

# -------------------------------------------------------------
# Boxplot for Outlier Detection
# -------------------------------------------------------------


def boxplot_outliers(df: pd.DataFrame, column: str, save_path: Path = None):
    """
    Visualize outliers in a numeric column using a boxplot.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset
    column : str
        Column name to visualize
    save_path : Path, optional
        Path to save the plot image
    """
    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(x=df[column], color="lightcoral")
    ax.set_title(f"Boxplot of {column} (Outlier Detection)")
    ax.set_xlabel(column)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


# -------------------------------------------------------------
# Scatterplot to visualize outliers relative to another variable
# -------------------------------------------------------------
def scatter_outliers(df: pd.DataFrame, x_col: str, y_col: str, hue_col: str = None, save_path: Path = None):
    """
    Scatter plot highlighting potential outliers relative to another numeric variable.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset
    x_col : str
        Column for x-axis
    y_col : str
        Column for y-axis
    hue_col : str, optional
        Column to color points by category
    save_path : Path, optional
        Path to save the plot image
    """
    plt.figure(figsize=(12, 6))
    ax = sns.scatterplot(x=x_col, y=y_col, hue=hue_col,
                         data=df, palette="tab10", alpha=0.6)
    ax.set_title(f"{y_col} vs {x_col} (Outlier Inspection)")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


# -------------------------------------------------------------
# IQR-based Outlier Highlighting
# -------------------------------------------------------------
def highlight_outliers_iqr(df: pd.DataFrame, column: str, save_path: Path = None):
    """
    Highlight points outside the IQR range for a numeric column.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset
    column : str
        Column name for outlier detection
    save_path : Path, optional
        Path to save the plot
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    df['is_outlier'] = (df[column] < lower) | (df[column] > upper)

    plt.figure(figsize=(12, 6))
    ax = sns.scatterplot(x=df.index, y=df[column], hue=df['is_outlier'], palette={
                         True: 'red', False: 'blue'})
    ax.set_title(f"Outlier Highlighting for {column}")
    ax.set_xlabel("Index")
    ax.set_ylabel(column)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()

    # Remove temporary column
    df.drop(columns=['is_outlier'], inplace=True)
