# insurance_analytics/visualization/plots.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


# ---------------------------------------------------------
# 1. Claim Frequency by Feature
# ---------------------------------------------------------
def plot_claim_frequency_by_feature(df: pd.DataFrame, feature: str, top_n: int = None):
    """
    Bar plot of Claim Frequency across categories.
    ClaimFrequency must already exist (0/1 indicator).
    """

    data = df.copy()

    # Limit to top N categories (for large PostalCode sets)
    if top_n:
        top_vals = data[feature].value_counts().nlargest(top_n).index
        data = data[data[feature].isin(top_vals)]

    freq = data.groupby(feature)["ClaimFrequency"].mean().reset_index()
    freq.rename(columns={"ClaimFrequency": "Frequency"}, inplace=True)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=freq, x=feature, y="Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Claim Frequency by {feature}")
    plt.ylabel("Claim Frequency")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 2. Claim Severity Boxplot
# ---------------------------------------------------------
def plot_claim_severity_box_by_feature(df: pd.DataFrame, feature: str, top_n: int = None, log_scale: bool = False):
    """
    Boxplot of Claim Severity (only where TotalClaims > 0).
    """

    data = df[df["TotalClaims"] > 0].copy()

    if data.empty:
        print(f"No severity data available for feature '{feature}'.")
        return

    if top_n:
        top_vals = data[feature].value_counts().nlargest(top_n).index
        data = data[data[feature].isin(top_vals)]

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=feature, y="ClaimSeverity")
    plt.xticks(rotation=45, ha="right")

    if log_scale:
        plt.yscale("log")
        plt.ylabel("Claim Severity (log scale)")
    else:
        plt.ylabel("Claim Severity")

    plt.title(f"Claim Severity by {feature}")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 3. Margin Boxplot
# ---------------------------------------------------------
def plot_margin_box_by_feature(df: pd.DataFrame, feature: str, top_n: int = None):
    """
    Boxplot of profit margin (TotalPremium - TotalClaims).
    """

    data = df.copy()
    data["Margin"] = data["TotalPremium"] - data["TotalClaims"]

    if top_n:
        top_vals = data[feature].value_counts().nlargest(top_n).index
        data = data[data[feature].isin(top_vals)]

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x=feature, y="Margin")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Margin by {feature}")
    plt.ylabel("Margin")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 4. Top Zip Codes by Claim Frequency
# ---------------------------------------------------------
def plot_top_zipcode_frequency(df: pd.DataFrame, top_n: int = 20):
    """
    Shows the top N postal codes ranked by claim frequency.
    Useful when PostalCode has many categories.
    """

    if "PostalCode" not in df.columns:
        print("PostalCode column not found.")
        return

    freq = (
        df.groupby("PostalCode")["ClaimFrequency"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(data=freq, x="PostalCode", y="ClaimFrequency")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top {top_n} Zip Codes by Claim Frequency")
    plt.ylabel("Claim Frequency")
    plt.tight_layout()
    plt.show()
