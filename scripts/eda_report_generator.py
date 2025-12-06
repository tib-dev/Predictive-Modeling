# src/insurance_analytics/reports/report_generator.py

import argparse
from pathlib import Path
import pandas as pd
from typing import Optional
from insurance_analytics.preprocessing.feature_engineering import add_loss_ratio
from insurance_analytics.eda.exploration import duplicated_rows, detect_outliers_iqr, summarize_missing
from insurance_analytics.data.load_data import load_data


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

    def save_report(self, output_dir: Path, format: str = "md"):
        """Save the report as Markdown."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            report_file = output_dir / f"{self.file_name}_eda_report.{format}"

            if format == "md":
                lines = ["# EDA Report\n"]
                lines.append(f"## Dataset Shape\n{self.report.get('shape')}\n")

                lines.append("## Columns and Types\n")
                for col, dtype in self.report.get("columns", {}).items():
                    lines.append(f"- **{col}**: {dtype}")

                lines.append("\n## Top 20 Missing Values\n")
                lines.append("| Column | % Missing |")
                lines.append("|--------|-----------|")
                for col, pct in self.report.get("missing_top20", {}).items():
                    lines.append(f"| {col} | {pct*100:.2f}% |")

                lines.append(
                    f"\n## Duplicates\n{self.report.get('duplicates')}\n")

                lines.append("\n## Outliers\n")
                lines.append("| Column | Outlier Count |")
                lines.append("|--------|---------------|")
                for col, count in self.report.get("outliers", {}).items():
                    lines.append(f"| {col} | {count} |")

                with open(report_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))

            else:
                raise ValueError("Unsupported format. Only 'md' is supported.")

            print(f"EDA report saved to {report_file}")
            return report_file

        except Exception as e:
            print(f"[ERROR] Failed to save report: {e}")
            raise

    def generate(self, output_dir: Path, numeric_cols: Optional[list] = None, save_format: str = "md"):
        """Full EDA report generation."""
        print("Running overview...")
        self.run_overview()
        print("Adding LossRatio if missing...")
        self.add_loss_ratio()
        print("Detecting outliers...")
        self.detect_outliers(numeric_cols=numeric_cols)
        print("Saving report...")
        return self.save_report(output_dir, format=save_format)


def main():
    parser = argparse.ArgumentParser(
        description="Generate EDA Markdown report.")
    parser.add_argument("--input", type=str, required=True,
                        help="Path to raw data file")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="Directory to save the report")
    parser.add_argument("--format", type=str, default="md",
                        help="Output format (default: md)")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        print(f"[ERROR] Input file does not exist: {input_path}")
        return

    try:
        df = load_data(input_path)
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        return

    report_name = input_path.stem
    report = EDAReport(df, report_name)
    try:
        report.generate(output_dir=output_dir, save_format=args.format)
    except Exception as e:
        print(f"[ERROR] Failed to generate report: {e}")


if __name__ == "__main__":
    main()
