# src/insurance_analytics/reports/report_generator.py

from pathlib import Path
import pandas as pd
import json
from typing import Optional
from insurance_analytics.preprocessing.feature_engineering import add_loss_ratio
from insurance_analytics.eda.exploration import duplicated_rows, detect_outliers_iqr, summarize_missing


class EDAReport:
    def __init__(self, df: pd.DataFrame, file_name: str):
        self.df = df.copy()
        self.file_name = file_name
        self.report = {}

    def run_overview(self):
        """Capture basic dataset info."""
        self.report["shape"] = self.df.shape
        self.report["columns"] = self.df.dtypes.apply(
            lambda x: str(x)).to_dict()
        self.report["missing_top20"] = summarize_missing(
            self.df, top_n=20).to_dict()
        self.report["duplicates"] = duplicated_rows(self.df)

    def detect_outliers(self, numeric_cols=None):
        """Detect outliers for numeric columns using IQR."""
        if numeric_cols is None:
            numeric_cols = self.df.select_dtypes(
                include="number").columns.tolist()

        outlier_summary = {}
        for col in numeric_cols:
            outliers = detect_outliers_iqr(self.df, col)
            outlier_summary[col] = len(outliers)
        self.report["outliers"] = outlier_summary

    def add_loss_ratio(self):
        """Add LossRatio column if missing."""
        if "LossRatio" not in self.df.columns:
            self.df = add_loss_ratio(self.df)

    def save_report(self, output_dir: Path, format: str = "json"):
        """Save the report as JSON or CSV."""
        output_dir.mkdir(parents=True, exist_ok=True)
        report_file = output_dir / f"{self.file_name}_eda_report.{format}"

        if format == "json":
            with open(report_file, "w") as f:
                json.dump(self.report, f, indent=4)
        elif format == "csv":
            # Convert report dictionary to a flat DataFrame
            flat_report = pd.json_normalize(self.report)
            flat_report.to_csv(report_file, index=False)
        else:
            raise ValueError("Unsupported format. Use 'json' or 'csv'.")

        print(f"EDA report saved to {report_file}")
        return report_file

    def generate(self, output_dir: Path, numeric_cols: Optional[list] = None, save_format: str = "json"):
        """Full EDA report generation."""
        print("Running overview...")
        self.run_overview()
        print("Adding LossRatio if missing...")
        self.add_loss_ratio()
        print("Detecting outliers...")
        self.detect_outliers(numeric_cols=numeric_cols)
        print("Saving report...")
        return self.save_report(output_dir, format=save_format)
