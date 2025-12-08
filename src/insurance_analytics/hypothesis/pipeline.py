# src/insurance_analytics/hypothesis/pipeline.py

import pandas as pd
from pathlib import Path

from insurance_analytics.hypothesis.metrics import attach_metrics
from insurance_analytics.hypothesis.segmentation import segment_binary
from insurance_analytics.hypothesis.statistical_tests import (
    t_test_numeric,
    chi_square_frequency
)
from insurance_analytics.hypothesis.assumption_checks import evaluate_hypothesis


def run_ab_tests(df: pd.DataFrame):
    """
    Run all A/B tests for provinces, zip codes, and gender.
    Returns a dictionary of results.
    """
    try:
        df = attach_metrics(df)
        results = {}

        # ---- 1. Province ----
        provinces = df["Province"].value_counts().head(2).index.tolist()
        A, B = segment_binary(df, "Province", provinces[0], provinces[1])

        results["Province Risk"] = {
            "Claim Frequency": evaluate_hypothesis(chi_square_frequency(A, B)),
            "Claim Severity": evaluate_hypothesis(t_test_numeric(A, B, "ClaimSeverity")),
        }

        # ---- 2. ZIP risk ----
        zips = df["PostalCode"].value_counts().head(2).index.tolist()
        A, B = segment_binary(df, "PostalCode", zips[0], zips[1])

        results["ZIP Risk"] = {
            "Claim Frequency": evaluate_hypothesis(chi_square_frequency(A, B)),
            "Claim Severity": evaluate_hypothesis(t_test_numeric(A, B, "ClaimSeverity")),
        }

        # ---- 3. ZIP margin ----
        results["ZIP Margin Difference"] = evaluate_hypothesis(
            t_test_numeric(A, B, "Margin")
        )

        # ---- 4. Gender ----
        A, B = segment_binary(df, "Gender", "Male", "Female")

        results["Gender Risk"] = {
            "Claim Frequency": evaluate_hypothesis(chi_square_frequency(A, B)),
            "Claim Severity": evaluate_hypothesis(t_test_numeric(A, B, "ClaimSeverity")),
        }

        return results

    except Exception as e:
        print(f"Pipeline error: {e}")
        return {}


def save_results(results: dict, output_dir: Path):
    """
    Save A/B test results to a JSON file.
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        out_path = output_dir / "ab_test_results.json"

        import json
        with open(out_path, "w") as f:
            json.dump(results, f, indent=4)

        print(f"A/B testing results saved at: {out_path}")
        return out_path

    except Exception as e:
        print(f"Failed to save results: {e}")
        return None


