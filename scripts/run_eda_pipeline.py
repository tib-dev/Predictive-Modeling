# run_eda_pipeline.py

from pathlib import Path
import pandas as pd

from insurance_analytics.core.registry import settings
from insurance_analytics.preprocessing.cleaner import cleaning
from insurance_analytics.data.load_data import load_data
from insurance_analytics.preprocessing.feature_engineering import add_loss_ratio
from insurance_analytics.eda.exploration import (
    dataset_overview, duplicated_rows, detect_outliers_iqr
)
from insurance_analytics.viz.plots import (
    plot_histogram,
    plot_bar,
    correlation_matrix,
    boxplot_outliers,
    highlight_outliers_iqr,
    scatter_by_group
)


def run_eda_pipeline(file_name: str):
    """
    Full EDA pipeline: load, clean, feature engineer, explore, visualize.
    """
    # -----------------------------
    # Paths
    # -----------------------------
    raw_path = settings.DATA["raw_dir"] / file_name
    report_path = Path(settings.REPORTS["reports_dir"])
    plots_dir = Path(settings.REPORTS["plots_dir"])
    processed_dir = Path(settings.DATA["processed_dir"])

    # Ensure directories exist
    report_path.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Load data
    # -----------------------------
    print(f"Loading data from {raw_path}...")
    df = load_data(raw_path)

    # -----------------------------
    # Cleaning
    # -----------------------------
    print("Cleaning data...")
    df = cleaning(df, report_missing=True)

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    print("Adding LossRatio feature...")
    df = add_loss_ratio(df)

    # -----------------------------
    # Dataset Overview
    # -----------------------------
    print("\nDataset Overview:")
    dataset_overview(df)

    # Check for duplicates
    print("\nChecking for duplicates...")
    dup_count = duplicated_rows(df)

    # -----------------------------
    # Univariate Analysis
    # -----------------------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()

    # Plot numeric distributions
    for col in numeric_cols[:5]:  # limit first 5 for speed
        plot_histogram(df, col, save_path=plots_dir / f"{col}_hist.png")
        boxplot_outliers(df, col, save_path=plots_dir / f"{col}_box.png")

    # Plot categorical distributions
    for col in cat_cols[:5]:
        plot_bar(df, col, top_n=15, save_path=plots_dir / f"{col}_bar.png")

    # -----------------------------
    # Outlier Detection
    # -----------------------------
    for col in numeric_cols[:5]:
        detect_outliers_iqr(df, col)
        highlight_outliers_iqr(
            df, col, save_path=plots_dir / f"{col}_outliers.png")

    # -----------------------------
    # Bivariate / Multivariate Analysis
    # -----------------------------
    correlation_matrix(df, save_path=plots_dir / "correlation_matrix.png")

    if "TotalPremium" in df.columns and "TotalClaims" in df.columns:
        scatter_by_group(df, x_col="TotalPremium", y_col="TotalClaims",
                         hue_col="VehicleType",
                         save_path=plots_dir / "claims_vs_premium_vehicle.png")

    # -----------------------------
    # Save cleaned & processed dataset
    # -----------------------------
    processed_file = processed_dir / \
        f"{file_name.replace('.txt', '_cleaned.csv')}"
    df.to_csv(processed_file, index=False)
    print(f"\nProcessed dataset saved to {processed_file}")


if __name__ == "__main__":
    run_eda_pipeline("MachineLearningRating_v3.txt")
